from fastapi import HTTPException, Header
from typing import Optional
import base64
import random
import string


def generate_random_string(length):
    characters = string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))


def encode_email(str):
    encoded_bytes = base64.b64encode(str.encode('utf-8'))
    return encoded_bytes.decode('utf-8')


def decode_base64(str):
    decoded_bytes = base64.b64decode(str)
    return decoded_bytes.decode('utf-8')


def get_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token not provided")
    token = authorization
    print(token)
    return decode_base64(token)  # decode_token(token)
