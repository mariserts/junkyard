# -*- coding: utf-8 -*-
from django.core.signing import Signer, TimestampSigner

from .exceptions import BadMaxAgeException


def sign_object(
    data: dict,
    salt: str = '',
    max_age: int = 0,
    separator: str = '::'
) -> dict:

    if isinstance(max_age, int) is False:
        raise BadMaxAgeException('Max age must be of type int')

    prop_signer = Signer()
    signed_max_age = prop_signer.sign_object(max_age)

    if max_age == 0:
        signer = Signer(salt=salt)
    else:
        signer = TimestampSigner(salt=salt)

    signed_data = signer.sign_object(data)

    signature = f'{signed_max_age}{separator}'
    signature += f'{signed_data}'

    return {
        'data': signed_data,
        'max_age': max_age,
        'salt': salt,
        'signature': signature,
    }
