import re, unicodedata

RE_URL = re.compile(r"http\S+")

def clean_text(txt):
    txt = unicodedata.normalize("NFC", txt)
    txt = RE_URL.sub("", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt
