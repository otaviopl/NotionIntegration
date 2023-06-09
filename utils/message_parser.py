import json


def parse_chatgpt_message(message, project_logger):

    # Break original message in lines.
    message_lines = message.splitlines()

    if ('' in message_lines):
        message_lines.remove('')

    project_logger.debug(message_lines)

    # Get the last line general comment.
    general_message = message_lines[-1]
    general_message = general_message.replace('/', '')

    json_as_str = ""

    for single_line in message_lines[:-1]:
        json_as_str += single_line

    # Discard the last 2 lines, and get the JSON from answer.
    json_as_str = json_as_str.replace('\t', '')
    json_as_str = json_as_str.replace('\n', '')
    json_as_str = json_as_str.replace('\'', '\"')

    try:
        json_obj = json.loads(json_as_str)
        return json_obj, general_message
    except Exception:
        project_logger.error("Failed to parse ChatGPT answer.")
        # Implement retry for ChatGPT (?).

    return None, None
