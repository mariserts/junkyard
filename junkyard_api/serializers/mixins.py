# -*- coding: utf-8 -*-
class SerializerContextShortcutsMixin:

    @property
    def request_user(self):
        request = self.context.get('request', None)
        if request is None:
            return None
        return request.user


class ItemShortcutsMixin(SerializerContextShortcutsMixin):

    @property
    def instance_item_type(self):
        if self.instance is None:
            return None
        return self.instance.item_type

    @property
    def instance_tenant_pk(self):
        if self.instance is None:
            return None
        return self.instance.tenant_id

    @property
    def raw_item_type(self):
        return self._kwargs.get('data', {}).get('item_type', None)

    @property
    def raw_tenant_pk(self):
        return self._kwargs.get('data', {}).get('tenant', None)
