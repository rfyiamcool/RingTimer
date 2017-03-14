#coding:utf-8


class RingBuffer(object):

    def __init__(self, timeout):
        self.timeout = timeout
        self.slot_tasks = {}
        '''
        slot0: {id: value}
        slot1: {id: value}
        '''
        self.init_slot_tasks()
        self.task_slot_index = {}
        self.cursor = 1

    def init_slot_tasks(self):
        for i in range(1, self.timeout + 1):
            self.slot_tasks[i] = {}

    def set_task_slot(self, d, slot):
        if self.task_slot_index.get(d, None):
            del self.task_slot_index[d]
        self.task_slot_index[d] = slot

    def add_slot_task(self, k, ts):
        slot = self.before_cursor
        _dict = self.slot_tasks.get(slot, {})
        _dict[k] = ts
        return slot

    def del_slot_task(self, k):
        slot_index = self.task_slot_index.get(k)
        _dict = self.slot_tasks.get(slot_index, {})
        if _dict.get(k):
            del _dict[k]

    def next(self):
        if self.cursor == self.timeout:
            self.cursor = 1
            return self.cursor
        self.cursor += 1
        return self.cursor

    @property
    def before_cursor(self):
        if self.cursor == 1:
            return self.timeout
        return self.cursor - 1

    @property
    def now_cursor(self):
        return self.cursor
