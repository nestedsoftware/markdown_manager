import os
import json


class ArticlesDatabase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.db = self.load_from_file()

    def load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def add_record(self, key, value):
        self.db.update({key: value})

    def get_record(self, key):
        return self.db[key]

    def delete_record(self, name):
        found_key = self.find_key(name)
        if found_key:
            value = self.db.pop(found_key)

    def write_to_file(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        if self.db:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.db, f, ensure_ascii=False, indent=4)

    def find_key(self, name):
        for key in self.db:
            if name in key:
                return key

        return None
