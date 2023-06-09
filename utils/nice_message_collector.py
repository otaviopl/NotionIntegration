import requests
import random


def get_motivational_message(project_logger):
    project_logger.info("Getting nice message...")
    all_messages = requests.get("https://type.fit/api/quotes")
    return random.choice(all_messages.json())
