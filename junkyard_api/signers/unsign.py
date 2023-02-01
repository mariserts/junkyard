# -*- coding: utf-8 -*-
from typing import Any, Union

from django.core.signing import Signer, TimestampSigner

from .exceptions import BadMaxAgeException


def unsign_object(
    data: Any,
    salt: str = '',
    max_age: Union[None, int] = None
) -> dict:

    if max_age is not None:
        if isinstance(max_age, int) is False:
            raise BadMaxAgeException('Max age must be of type int')

    if max_age is not None:
        signer = TimestampSigner(salt)
        unsigned_data = signer.unsign_object(data, max_age=max_age)
    else:
        signer = Signer(salt)
        unsigned_data = signer.unsign_object(data)

    return {
        'data': unsigned_data,
        'max_age': max_age,
        'salt': salt,
    }
