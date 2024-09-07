from io import BytesIO
import json
import shutil
from fastapi import  HTTPException
from pathlib import Path
import os
from docx import Document
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


from common.aimodels import raw_llm


def convert_docx_to_text(blob_content):
    """Converts DOCX blob content to text."""
    doc = Document(BytesIO(blob_content))
    readed_text = ""
    for para in doc.paragraphs:
        readed_text += para.text
    return readed_text


def save_blob_to_temp_file(blob_content, extension):
    """Saves blob content to a temporary file and returns the path."""
    temp_file_path = f"/tmp/temp_file{extension}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(blob_content)
    return temp_file_path


def convert_doc_to_docx(doc_path):
    """Converts .doc file to .docx."""
    temp_docx_path = doc_path.replace(".doc", ".docx")
    # Assume conversion is done (e.g., using subprocess or an external tool)
    os.rename(doc_path, temp_docx_path)
    return temp_docx_path


def read_uploaded_file(file_path: Path):
    try:
        # Check for file extension and handle accordingly
        file_extension = file_path.suffix.lower()

        if file_extension in [".txt", ".docx"]:
            with file_path.open("rb") as file: 
                file_content = file.read()

            if file_extension == ".txt":
                return file_content.decode("utf-8")  
            elif file_extension == ".docx":
                return convert_docx_to_text(file_content)

        elif file_extension == ".doc":
            temp_docx_path = convert_doc_to_docx(
                str(file_path)
            )
            return convert_docx_to_text(Path(temp_docx_path).read_bytes())

        else:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file type: {file_extension}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while reading the file: {e}"
        )


def generate_prompt_for_identifying_questions(filedata):
    try:
        prompt = f"""
    Analyze the provided text, which contains a resume which has details of a candidate. From the data, extract his details in a json format.
    
    Output format:

    ...
    It should contain keywords like name, address, phone, skills, careeer details, from the resume, if not found return empty string.

    ...


    Text:
    {filedata}
    """
        return prompt
    except Exception as error:
        logger.error(f"error in generating prompt {error}")


async def extract_transcriptions_using_model(prompt, retry_count=0):
    try:
        rlm = raw_llm()
        response = rlm.chat.completions.create(
            model="text-gen", messages=[{"role": "system", "content": prompt}]
        )

        data = json.loads(response.model_dump_json(indent=2))

        return data

    except Exception as error:
        logger.error(f"error in generating output {error}")

        raise HTTPException(status_code=500, detail=str(error))