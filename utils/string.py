from utils import install_python_lib

try:
    from fontTools import unicodedata
except ModuleNotFoundError:
    install_python_lib('fontTools')
    from fontTools import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
