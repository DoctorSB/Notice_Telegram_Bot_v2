class Worker:
    def __init__(self, id, work_list, ready_list):
        self.id = ''
        self.work_list = []
        self.ready_list = []

    def add_work(self, work):
        self.work_list.append(work)

    def remove_work(self, work):
        self.work_list.remove(work)

    def get_work_list(self):
        return self.work_list
    
    def add_ready(self, ready):
        self.ready_list.append(ready)

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
