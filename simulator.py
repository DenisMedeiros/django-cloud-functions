import os
import sys

# Include src folder to Python path.
project_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(project_dir, "src")
sys.path.insert(0, src_dir)

from src import awsentrypoint  # noqa E402


def awx_function() -> dict:
    """Calls the AWX entrypoint.

    Returns:
        dict: The AWX Lambda response.
    """
    # Define a dummy event dict.
    event = {
        "headers": {
            "content-length": "31",
            "x-forwarded-proto": "https",
            "x-forwarded-port": "443",
            "content-type": r"application\/json",
            "accept": r"*\/*"
        },
        "isBase64Encoded": False,
        "rawPath": r"\/html\/",
        "requestContext": {
            "http": {
                "path": r"\/json\/",
                "protocol": r"HTTP\/1.1",
                "method": "POST",
            },
        },
        "queryStringParameters": {
            "options": "123"
        },
        "body": "{\n\t\"data\": {\n\t\t\"key1\": 123\n\t}\n}",
        "version": "2.0",
        "rawQueryString": "options=123"
    }

    return awsentrypoint.main(event=event, context=None)


def main():
    response = awx_function()
    print(response)


if __name__ == "__main__":
    main()
