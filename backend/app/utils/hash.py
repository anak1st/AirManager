import hashlib

def hash(str):
    str = str + "notreallyhashed"
    str = hashlib.md5(str.encode()).hexdigest()
    return str