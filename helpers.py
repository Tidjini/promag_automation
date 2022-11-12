"""Formelize/Unformelize References


to store images with correct forme: 1_0.png
and set reference in server
ex: 
    - formelize('1/0')      => 1_0
    - unformelize('1_0')    => 1/0
"""


def formelize(ref):
    return ref.replace("/", "_").lower()


def unformelize(ref):
    return ref.replace("_", "/").upper()
