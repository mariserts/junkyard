# -*- coding: utf-8 -*-
from typing import Union

from django.core.signing import Signer, TimestampSigner

from .exceptions import BadMaxAgeException


def sign_object(
    data: dict,
    salt: str = '',
    max_age: Union[None, int] = None
) -> dict:

    if max_age is not None:
        if isinstance(max_age, int) is False:
            raise BadMaxAgeException('Max age must be of type int')

    if max_age is not None:
        signer = TimestampSigner(salt)
    else:
        signer = Signer(salt)

    signed_data = signer.sign_object(data)

    return {
        'data': signed_data,
        'max_age': max_age,
        'salt': salt,
    }
