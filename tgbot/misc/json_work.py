import json

def json_create(file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

def json_read(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def json_write(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def json_add(file_name, key):
    data = json_read(file_name)
    data[key] = []
    json_write(file_name, data)

def remove_json(file_name, key, value):
    data = json_read(file_name)
    data[key].remove(value)
    json_write(file_name, data)

def append_json(file_name, key, value):
    data = json_read(file_name)
    data[key].append(value)
    json_write(file_name, data)


