
import json
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
import logging
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from services.resume_extraction_service import extract_transcriptions_using_model, generate_prompt_for_identifying_questions, read_uploaded_file

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = FastAPI()


@app.post("/upload")
async def upload_file(
    resume: UploadFile = File(...),
):
    # Save the file temporarily
    try:
        suffix = Path(resume.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(resume.file, tmp)
            tmp_path = Path(tmp.name)

        readed_text = read_uploaded_file(tmp_path)
        prompt = generate_prompt_for_identifying_questions(readed_text)
        data = await extract_transcriptions_using_model(
            prompt
        )  
        
        content_field = data['choices'][0]['message']['content']

        # Since the 'content' string starts and ends with triple backticks (```), we want to remove those.
        # We also remove any leading or trailing whitespace and newline characters that might be there
        content_json_str = content_field.replace('"json\n', '')

        # Step 2: Replace escape sequences like '\n' with actual line breaks or simply strip them
        content_json_str = content_json_str.replace('\n', '').replace('\"', '"')


        # Now, we can convert the string to an actual JSON (dictionary) object
        try:
            content_json = json.loads(content_json_str)
        except json.JSONDecodeError as e:
            content_json = content_json_str
            print(f"JSON decode error: {e}")
        else:
            content_json = content_json_str
            # Use the JSON data as needed
            print(content_json)
            # Example of accessing the name field
            print(content_json['name'])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up the temporary file
        if tmp_path.exists():
            tmp_path.unlink()

    return JSONResponse(
        content={
            "message": "Resume uploaded successfully",
            "file_name": resume.filename,
            "data": content_json,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
