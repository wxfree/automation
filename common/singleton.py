class Singleton:
    _instance = None

    # @classmethod
    def __new__(self, *args, **kwargs):
        if Singleton._instance is None:
            Singleton._instance = object.__new__(self)
        return Singleton._instance