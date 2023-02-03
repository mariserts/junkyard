# -*- coding: utf-8 -*-
from django.core.signing import Signer, TimestampSigner

from .exceptions import BadMaxAgeException, BadSignatureFormatException


def unsign_object(
    signature: str,
    salt: str = '',
    separator: str = '::',
) -> dict:

    signature_parts = signature.split(separator)

    if len(signature_parts) != 2:
        raise BadSignatureFormatException('Bad signature format')

    prop_signer = Signer()
    data = signature_parts[1]
    max_age = prop_signer.unsign_object(signature_parts[0])

    print(data)
    print(max_age)

    if isinstance(max_age, int) is False:
        raise BadMaxAgeException('Max age must be of type int')

    if max_age == 0:
        signer = Signer(salt=salt)
        unsigned_data = signer.unsign_object(data)
    else:
        signer = TimestampSigner(salt=salt)
        unsigned_data = signer.unsign_object(data, max_age=max_age)

    return {
        'data': unsigned_data,
        'max_age': max_age,
        'salt': salt,
        'signature': signature
    }
