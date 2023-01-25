from typing import List, Union

from rest_framework.serializers import Serializer


class ItemTypeRegistry:

    types = {}

    def register(self, name: str, serializer: Serializer) -> None:
        if name in self.types:
            raise ItemTypeDuplicationException(
                f'Item type "{name}" already registered'
            )
        self.types[name] = serializer

    def find(self, name:str) -> Union[None, Serializer]:
        try:
            return self.types[name]
        except KeyError:
            return None

    def get_types_as_choices(self) -> List[List[str]]:
        types = []
        for key in self.types.keys():
            types.append([key, key])
        return types
