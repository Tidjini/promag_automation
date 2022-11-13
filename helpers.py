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
