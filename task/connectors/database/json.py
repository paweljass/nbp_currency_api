import json

from config import JSON_DATABASE_NAME


class JsonFileDatabaseConnector:
    def __init__(self) -> None:
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DATABASE_NAME, "r") as file:
            return json.load(file)
        
    def write_data(self, data):
        with open(JSON_DATABASE_NAME, 'w') as file:
            json.dump(data, file, indent=4)

    def add_data(self, new_data):
        new_data = json.loads(new_data)
        data = self._read_data()
        max_key = max(map(int, data.keys())) if data else 0
        new_data["id"] = max_key+1
        data[max_key+1] = new_data
        self.write_data(data)
        

    def get_all(self) -> list:
        raise NotImplementedError()

    def get_by_id(self) -> ...:
        raise NotImplementedError()