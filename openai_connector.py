import os
import openai
from dotenv import load_dotenv


def call_openai_assistant(tasks):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_KEY")

    print("Calling ChatGPT. This can take a while...")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "assistant",
                "content": build_message(tasks)
            }
        ]
    )

    answer = completion.choices[0].message.content
    return answer


def build_message(tasks):
    message = "Using few words, please help me to prioritize " + \
        "the following tasks. Answer in portuguese.Explain the " + \
        "importance of each one of the tasks." + \
        "\nInstructions:" + \
        "\n- Be brief and explain the prioritization." + \
        "\n- Tasks are in portuguese." + \
        "\n- Answer with the format: #. <task_description> " + \
        "- (<explanation_about_importance>)" + \
        "\nTasks: "

    for task in tasks:
        message += "\n - " + task["name"]

    return message
