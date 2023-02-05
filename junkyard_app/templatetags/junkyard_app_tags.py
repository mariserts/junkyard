# -*- coding: utf-8 -*-
from django import template
from django.urls import resolve, reverse

from ..conf import settings

register = template.Library()


@register.filter(name='extend_field_css_classes')
def extend_field_css_classes(field, classes):
    cls = field.field.widget.attrs.get('class', '')
    field.field.widget.attrs['class'] = cls + ' ' + classes
    return field


@register.inclusion_tag('signer/components/footer.html', takes_context=True)
def footer(context):
    return {}


@register.inclusion_tag('signer/components/menu.html', takes_context=True)
def mainmenu(context):

    request = context['request']
    current_urlname = resolve(request.path_info).url_name

    return {
        'links': [
            {
                'active': current_urlname == settings.URLNAME_SIGN,
                'text': 'Sign',
                'url': reverse(settings.URLNAME_SIGN),
            },
            {
                'active': current_urlname == settings.URLNAME_UNSIGN,
                'text': 'Unsign',
                'url': reverse(settings.URLNAME_UNSIGN),
            }
        ],
        'request': request,
        'project': {
            'title': settings.PROJECT_TITLE,
            'url': '/'
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
