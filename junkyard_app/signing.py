# -*- coding: utf-8 -*-
from django.core.signing import BadSignature, Signer, TimestampSigner


def sign(
    token: str,
    max_age: int,
) -> str:
    signed_max_age = Signer().sign_object(max_age)
    signature = TimestampSigner().sign_object(token)
    return f'{signed_max_age}::{signature}'


def unsign(
    signature: str,
) -> str:

    signature_parts = signature.split('::')

    if len(signature_parts) != 2:
        raise BadSignature()

    max_age = Signer().unsign_object(signature_parts[0])

    return TimestampSigner().unsign_object(
        signature_parts[1],
        max_age=max_age
    )
