import os
import json
import typing


class Database:
    class Backend:
        def __init__(self, json_data: dict[str, typing.Any]) -> None:
            self._json_data: dict = {}
            self._data_keys = list(self._json_data.keys())
            self._index = 0
            if json_data:
                self._json_data = json_data

        def __iter__(self):
            self._data_keys = list(self._json_data.keys())
            self._index = 0
            return self

        def __next__(self):
            if self._index < len(self._data_keys):
                next_val = self._data_keys[self._index]
                self._index += 1
                return next_val
            raise StopIteration

        def get_data(self) -> dict[str, typing.Any]:
            return self._json_data

        def set_data(self, json_data: dict[str, typing.Any]) -> None:
            self._json_data = json_data
            
    class BackendFile(Backend):
        def __init__(self, name: str) -> None:
            self._file = f"data/{name}.json"
            super().__init__(self._read())

        def __del__(self) -> None:
            self._save()

        def _read(self) -> dict[str, typing.Any]:
            if not os.path.isfile(self._file):
                return {}
            with open(self._file, "r", encoding="utf-8") as json_file:
                return json.load(json_file)

        def _save(self) -> None:
            with open(self._file, "w", encoding="utf-8") as json_file:
                json.dump(self._json_data, json_file, indent=4)

    def __init__(self, backend: Backend) -> None:
        self._backend: Database.Backend = backend

    def __iter__(self):
        self._backend.__iter__()
        return self

    def __next__(self):
        return self._backend.__next__()

    def get_user(self, user):
        return self._backend._json_data[user]

    def get_user_data(self, user: int) -> typing.Any:
        data = self._backend.get_data()
        if str(user) in data:
            return data[str(user)]
        return None

    def update_user_data(self, user: int, user_data: typing.Any) -> None:
        data = self._backend.get_data()
        data[str(user)] = user_data
        self._backend.set_data(data)

    def remove(self, element):
        self._backend._json_data.pop(str(element))
