class Quest:
    def __init__(self, checker_id='', workers_list=[], quest_name='', quest_description='', quest_id='', quest_status='', time_limit=''):
        self.checker_id = checker_id
        self.workers_list = workers_list
        self.quest_name = quest_name
        self.quest_description = quest_description
        self.quest_id = quest_id
        self.quest_status = quest_status
        self.time_limit = time_limit

    def get_checker_id(self):
        return self.checker_id

    def set_checker_id(self, checker_id):
        self.checker_id = checker_id

    def get_workers_list(self):
        return self.workers_list

    def add_worker_id(self, worker_id):
        self.workers_list.append(worker_id)

    def remove_worker_id(self, worker_id):
        self.workers_list.remove(worker_id)

    def get_quest_name(self):
        return self.quest_name

    def set_quest_name(self, quest_name):
        self.quest_name = quest_name

    def get_quest_description(self):
        return self.quest_description

    def set_quest_description(self, quest_description):
        self.quest_description = quest_description

    def get_quest_id(self):
        return self.quest_id

    def set_quest_id(self, quest_id):
        self.quest_id = quest_id

    def get_quest_status(self):
        return self.quest_status

    def set_quest_status(self, quest_status):
        self.quest_status = quest_status

    def get_time_limit(self):
        return self.time_limit

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit
