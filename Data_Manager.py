import json
class Data_Manager:

    def serialize_json(self, dict):
        json_object = json.dumps(dict, indent=4)
