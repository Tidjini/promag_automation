import os
import requests
from helpers import formelize

API = os.environ.get("PROCOM_API", "https://procom-tracker.herokuapp.com/api/")


def update(product):
    """Update in remote services

    references must be lower case and no slashes
    """
    reference = formelize(product["reference"])

    json = {
        "qte_stock": product["qte_stock"],
        "value": product["value"],
        "reference": product["reference"],
        "designation": product["designation"],
    }
    files = {
        "qte_picture": open(f"output/{reference}.qte.png", "rb"),
        "value_picture": open(f"output/{reference}.mtn.png", "rb"),
    }
    # since the product (reference) exist in Remote API,
    # otherwise make sure to have references saved in remote data
    response = requests.put(f"{API}products/{reference}/", files=files, data=json)

    print(response)
