from dotenv import load_dotenv
import os

def load_config():
    # Load environment variables from .env file
    load_dotenv()
    # database_url = os.getenv("database_url")
    app_host = os.getenv("app_host")
    app_port = int(os.getenv("app_port"))
    openai_api_key = os.getenv("openai_api_key")
    openai_deployment_endpoint = os.getenv("openai_deployment_endpoint")
    openai_deployment_name = os.getenv("openai_deployment_name")
    openai_model_name = os.getenv("openai_model_name")
    openai_deployment_version = os.getenv("openai_deployment_version")
    # container_name = os.getenv("container_name")
    # blob_service_connection_string = os.getenv("blob_service_connection_string")
    # service_bus_url = os.getenv("azure_service_bus_url")
    # queue_name = os.getenv("queue_name")
    # que_lock_period_in_seconds = int(os.getenv("que_lock_period_in_seconds"))
    # mailgun_domain = os.getenv("mailgun_domain")
    # mailgun_api_key = os.getenv("mailgun_api_key")
    
    config = {
        # "database_url": database_url,
        "app_host": app_host,
        "app_port": app_port,
        "openai_api_key": openai_api_key,
        "openai_deployment_endpoint": openai_deployment_endpoint,
        "openai_deployment_name": openai_deployment_name,
        "openai_model_name": openai_model_name,
        "openai_deployment_version": openai_deployment_version,
        # "container_name": container_name,
        # "blob_service_connection_string":blob_service_connection_string,
        # "service_bus_url": service_bus_url,
        # "queue_name":queue_name,
        # "que_lock_period_in_seconds":que_lock_period_in_seconds,
        # "mailgun_domain":mailgun_domain,
        # "mailgun_api_key":mailgun_api_key,
    }
    
    return config
# Usage
config = load_config()