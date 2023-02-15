from typing import Type, Union

from rest_framework.reverse import reverse

from ..conf import settings


def get_projects_tenants_items_url(
    request: Type,
    project_pk: Union[int, str],
    tenant_pk: Union[int, str],
    item_pk: Union[None, str, int] = None
) -> str:

    detail = item_pk is not None

    view_type = 'detail'
    if detail is False:
        view_type = 'list'

    return reverse(
        f'{settings.BASENAME_PROJECTS_TENANTS_ITEMS}-{view_type}',
        args=[project_pk, tenant_pk, item_pk],
        request=request,
    )
