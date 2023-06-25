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


def json_add_worker(file_name, key, id):
    data = json_read(file_name)
    data[key]["worker_list"].append(id)
    json_write(file_name, data)


def remove_json(file_name, key, value):
    data = json_read(file_name)
    data[key].remove(value)
    json_write(file_name, data)


def append_json(file_name, key, value):
    data = json_read(file_name)
    data[key].append(value)
    json_write(file_name, data)


def output_all(file_name):
    data = json_read(file_name)
    text = ''
    for task_id, task_data in data.items():
        text += f'Task ID: {task_id}\n'
        text += f'Task name: {task_data["name"]}\n'
    return text


def task_create(task):
    data = json_read('tasks.json')
    key = task.quest_name
    data[key] = {}
    data[key] = {}
    data[key]["name"] = task.quest_name
    data[key]["description"] = task.quest_description
    data[key]["files"] = task.files
    data[key]["status"] = task.quest_status
    data[key]["time"] = task.time_limit
    data[key]["checker_id"] = task.checker_id
    data[key]["worker_list"] = task.workers_list
    json_write('tasks.json', data)


def task_output(file_name, task_name):
    data = json_read(file_name)
    text = f'Task ID: {task_name}\n'
    text += f'Task name: {data[task_name]["name"]}\n'
    text += f'Task description: {data[task_name]["description"]}\n'
    text += f'Task status: {data[task_name]["status"]}\n'
    text += f'Task files: {data[task_name]["files"]}\n'
    text += f'Task time limit: {data[task_name]["time"]}\n'
    text += f'Task checker: {data[task_name]["checker_id"]}\n'
    text += f'Task workers: {data[task_name]["worker_list"]}\n'
    return text

def json_add_photo(file_name, key, photo_id):
    data = json_read(file_name)
    data[key]["files"].append(photo_id)
    json_write(file_name, data)

def json_keys(file_name):
    data = json_read(file_name)
    return data.keys()