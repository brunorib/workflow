import json

def to_json(obj):
    return json.dumps(obj.__dict__, default=lambda o: o.__dict__, indent=4)