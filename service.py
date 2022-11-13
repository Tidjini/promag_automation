import os
import requests
from helpers import formalize

API = os.environ.get("PROCOM_API", "https://procom-tracker.herokuapp.com/api/")


def serialize(product: dict) -> tuple:
    """Serialize product object

    references must be lower case and no slashes
    """
    reference = formalize(product["reference"])

    data = {
        "qte_stock": product["qte_stock"],
        "value": product["value"],
        "reference": reference,
        "designation": product["designation"],
    }

    return reference, data


def save(ref: str, data: dict):
    """Save to remote host

    If product reference exist then update with put request,
    else create a new product object
    """

    url = f"{API}products/"

    files = {
        "qte_picture": open(f"output/{ref}.qte.png", "rb"),
        "value_picture": open(f"output/{ref}.mtn.png", "rb"),
    }

    response = requests.put(f"{url}{ref}/", data=data, files=files)
    if response.status_code == 200:
        return response

    response = requests.post(url, data=data)
    if response.status_code == 201:
        return response

    error_message = "Save Exception, something went wrong in your remote server"
    raise Exception(error_message, f"caused by: {response.json()}")


def update(product):
    ref, data = serialize(product)
    try:
        save(ref, data)
    except Exception as e:
        print("Exception due to:", e)
