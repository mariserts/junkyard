class ItemTypeRegistry:

    _get_types_as_choices = None
    types = {}

    def register(self, name, serializer):
        self.types[name] = serializer

    def find(self, name):
        try:
            return self.types[name]
        except KeyError:
            return None

    def get_types_as_choices(self):
        types = []
        for key in self.types.keys():
            types.append([key, key])
        return types
