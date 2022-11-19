"""Formalize/Unformalize References
to store images with correct forme: 1_0.png
and set reference in server
ex: 
    - formalize('1/0')      => 1_0
    - unformalize('1_0')    => 1/0
"""


def formalize(ref):
    return ref.replace("/", "_").lower()


def unformalize(ref):
    return ref.replace("_", "/").upper()


def raise_requests_exception(response):

    error_message = "Save Exception, something went wrong in your remote server"
    print(error_message, f"caused by: {response.json()}")
    raise Exception(error_message, f"caused by: {response.json()}")


def has_number_or_dot(word: str) -> bool:
    """Check if is number (look like number)

    accept : 100.50, problem with 14.140.50, todo review this
    """
    if word is None:
        return False

    for char in word:
        if not char.isdigit() and not char == ".":
            return False
    return True
