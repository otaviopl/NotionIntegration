import os


def load_notion_credentials(project_logger):
    project_logger.debug("Getting Notion credentials from .env...")

    notion_keys = {}
    notion_keys['database_id'] = os.getenv("NOTION_DATABASE_ID")
    notion_keys['api_key'] = os.getenv("NOTION_API_KEY")

    project_logger.debug("Finished getting Notion credentials.")

    return notion_keys


def load_email_config(project_logger):
    project_logger.debug("Getting EMAIL credentials from .env...")

    email_config = {}
    email_config['email_from'] = os.getenv("EMAIL_FROM")
    email_config['email_to'] = os.getenv("EMAIL_TO")
    email_config['display_name'] = os.getenv("DISPLAY_NAME")

    project_logger.debug("Finished getting EMAIL credentials.")

    return email_config