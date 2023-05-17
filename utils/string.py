from utils.install_lib import install_python_lib

try:
    from fontTools import unicodedata
except ModuleNotFoundError:
    install_python_lib('fontTools')


def remove_accents(input_str):
    from fontTools import unicodedata
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
