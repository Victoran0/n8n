from dotenv import load_dotenv
import os
import requests
import json
import os
from langchain_core.tools import tool

load_dotenv()

N8N_BEARER_TOKEN = os.environ["N8N_BEARER_TOKEN"]
UPLOAD_GOOGLE_DOC_WEBHOOK = os.environ["UPLOAD_GOOGLE_DOC_WEBHOOK"]


def invoke_n8n_webhook(method, url, function_name, payload=None):
    """
    Helper function to make a GET or POST request to the n8n webhook.

    Args:
        method (str): The HTTP method to use ('GET' or 'POST').
        url (str): The API endpoint.
        function_name (str): The name of the tool the AI agent invoked.
        payload (dict, optional): The payload to send in the request body for POST requests.

    Returns:
        str: the API response in JSON format or an error message.
    """

    headers = {
        "Authorization": f"{N8N_BEARER_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=payload)
        else:
            return f"Unsupported method: {method}"

        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Exception when calling {function_name}: {e}"


@tool
def create_google_doc(document_title: str, document_text: str):
    """
    Creates a Google Doc in Google Drive with the text specified.

    Example call:

    create_google_doc("9/20 Meeting Notes", "Meeting notes for 9/20...")
    Args:
        document_title (str): The name of the Google Doc
        document_text (str): The text to put in the new Google Doc
    Returns:
        str: The API response with the result of creating the Google Doc or an error if there was an issue
    """
    return invoke_n8n_webhook(
        "POST",
        UPLOAD_GOOGLE_DOC_WEBHOOK,
        "create_google_doc",
        {"document_title": document_title, "document_text": document_text}
    )


# Maps the function names to the actual function object in the script
# This mapping will also be used to create the list of tools to bind to the agent
available_functions = {
    "create_google_doc": create_google_doc
}
