from typing import Union
import os
import hashlib
import base64
from dotenv import load_dotenv

def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29

    :return: bytes representation of the CSCI salt
    """
    load_dotenv()
    salt = bytes.fromhex(os.environ["CSCI_SALT"])
    return salt

def get_csci_pepper() -> bytes:
    """Returns the appropriate pepper for CSCI E-29

    This is similar to the salt, but defined as the UUID of the Canvas course,
    available from the Canvas API.

    This value should never be recorded or printed.

    :return: bytes representation of the pepper
    """

    # Hint: Use base64.b64decode to decode a UUID string to bytes
    from ..canvas.canvas import login, courseNameToID
    load_dotenv()
    canvas = login()
    pepper = courseNameToID(canvas, 'advanced python')
    return base64.b64decode(pepper)

# print(get_csci_pepper())

def hash_str(some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash, can be str or bytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    """
    # encode inputs
    if isinstance(some_val,str):
        some_val = some_val.encode('ascii')
    if isinstance(salt,str):
        salt = salt.encode('ascii')
    val_salt = salt + some_val
    m = hashlib.sha256()
    m.update(val_salt)
    return m.digest()

def get_user_id(username: str) -> str:
    salt = get_csci_salt() + get_csci_pepper()
    return hash_str(username.lower(), salt=salt).hex()[:8]

if __name__ == '__main__': # pragma: no cover
    'Testing for directly answering the quiz'
    print(get_user_id('gorlins'))
    print(get_user_id('torvalds'))
    print(get_user_id('wesm'))
