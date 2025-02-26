import time as t


class _Cache():
    def __init__(self, **kwargs):
        self._cache = {}
        self.lifespan = 15

    def get(self, key):
        value = self._cache.get(key, None)
        date = t.time()
        if value:
            if value["time"] + self.lifespan < date and not value["save"]:
                if value["callback"]:
                    value["callback"](value["cached"])
                del self._cache[key]
                return None

            self._cache[key]["time"] = date

            return value["cached"]

        else:
            return None

    def set(self, key, value, **kwargs):
        dict = {"time":t.time(), "cached":value, "save":kwargs.get("save", False), "callback":kwargs.get("callback",None)}
        self._cache[key] = dict
