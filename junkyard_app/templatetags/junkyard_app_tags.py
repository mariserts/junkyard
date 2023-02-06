# -*- coding: utf-8 -*-
from django import template
from django.urls import reverse

from ..conf import settings

register = template.Library()


@register.filter(name='extend_field_css_classes')
def extend_field_css_classes(field, classes):
    cls = field.field.widget.attrs.get('class', '')
    field.field.widget.attrs['class'] = cls + ' ' + classes
    return field


@register.inclusion_tag(
    'junkyard_app/components/footer.html',
    takes_context=True
)
def footer(context):
    return {}


@register.inclusion_tag(
    'junkyard_app/components/menu.html',
    takes_context=True
)
def mainmenu(context):

    request = context['request']
    token_data = getattr(
        request,
        settings.REQUEST_TOKEN_ATTR_NAME,
        {}
    )
    user = token_data.get('user', None)
    is_authenticated = user is not None

    links = [
        {
            'text': 'Home',
            'url': reverse(settings.URLNAME_PUBLIC_HOMEPAGE),
        }
    ]

    if is_authenticated is False:
        links += [
            {
                'text': 'Sign in',
                'url': reverse(settings.URLNAME_SIGN_IN)
            },
        ]

    else:
        links += [
            {
                'text': 'CMS',
                'url': reverse(settings.URLNAME_CMS_HOMEPAGE),
            },
            {
                'text': user['email'],
                'links': [{
                    'text': 'Sign out',
                    'url': reverse(settings.URLNAME_SIGN_OUT),
                }],
            },
        ]

    return {
        'links': links,
        'request': request,
        'project': {
            'title': settings.TEXT_PROJECT_TITLE,
            'url': reverse(settings.URLNAME_PUBLIC_HOMEPAGE),
        }
    }


@register.filter(name='override_disabled_state')
def override_disabled_state(field, disabled):
    field.field.widget.attrs['disabled'] = disabled
    return field


@register.filter(name='override_field_attr')
def override_field_attr(field, value):
    attr_name, attr_value = value.split('|')
    field.field.widget.attrs[attr_name] = attr_value
    return field
