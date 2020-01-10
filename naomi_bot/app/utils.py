import base64

def text_from_base64(b64_text):
    return(bytes.decode(base64.b64decode(b64_text)))

def text_to_base64(plain_text):
    return(str(base64.b64encode(plain_text.encode()), "utf-8"))