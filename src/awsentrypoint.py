import os
import django
import logging

from django.template.loader import render_to_string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from core.models import Product  # noqa E402


def build_json_response() -> dict:
    """Builds a JSON response with a list of products.

    Returns:
        dict: The AWS Lambda response.
    """
    logging.info("Building JSON response...")
    products = [product.as_dict() for product in Product.objects.all()]
    return {
        "statusCode": "200",
        "body": products,
        "headers": {
            "Content-Type": "application/json",
        }
    }


def build_html_response() -> dict:
    """Builds a HTML response with a list of products and using Django template system.

    Returns:
        dict: The AWS Lambda response.
    """
    template = "example.html"
    context = {
        "products": Product.objects.all()
    }
    html = render_to_string(template, context)
    logging.info("Building HTML response...")
    return {
        "statusCode": "200",
        "body": html,
        "headers": {
            "Content-Type": "text/html",
        }
    }


def build_error_response(status_code: int, message: str) -> dict:
    """Builds an error message.

    Args:
        status_code (int): The HTTP response error code (should be >= 400).
        message (str): The error message.

    Returns:
        dict: The AWS Lambda response.
    """
    return {
        "statusCode": status_code,
        "body": {"error": message},
        "headers": {
            "Content-Type": "application/json",
        }
    }


def main(event: dict, context: object) -> dict:
    """Main function.

    Args:
        event (dict): A dict with the event payload.
        context (object): The AWX Lambda context object.

    Returns:
        dict: The AWS Lambda response.
    """
    logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    rawPath = event.get("rawPath")
    if not rawPath:
        error_message = "rawPath not found in request - probably a manual run."
        logging.error(error_message)
        return build_error_response(error_message)
    path = event.get("rawPath").replace(r"\/", "/")
    if "/json/".startswith(path):
        return build_json_response()
    elif "/html/".startswith(path):
        logging.info("Building HTML response...")
        return build_html_response()
    else:
        error_message = f"Invalid path '{path}'."
        logging.error(error_message)
        return build_error_response(error_message)
