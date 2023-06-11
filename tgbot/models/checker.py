class Checker:
    def __init__(self, id='', quest_list=[], ready_list=[]):
        self.id = id
        self.quest_list = quest_list
        self.ready_list = ready_list

    def add_quest(self, quest):
        self.quest_list.append(quest)

    def remove_quest(self, quest):
        self.quest_list.remove(quest)

    def get_quest_list(self):
        return self.quest_list

    def add_ready(self, ready):
        self.ready_list.append(ready)

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
