import hashlib
from django.conf import settings


def sha256(string):
    """ SHA256加密 """
    hash_object = hashlib.sha256(settings.SECRET_KEY.encode('utf-8'))
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()
