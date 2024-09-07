import logging
from config.config import config 
from openai import AzureOpenAI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = config


def raw_llm():
    try:
        # Configure OpenAI LLM API
        llm = AzureOpenAI(
            azure_endpoint=settings['openai_deployment_endpoint'],
            api_version='2023-09-01-preview',
            api_key=settings['openai_api_key']
        )
        logger.info("LLM function executed successfully")
        return llm
    
    except Exception as error:
        logger.error("Error in LLM function: %s", error)