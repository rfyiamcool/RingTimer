# coding:utf-8

import time
import threading


class RingBuffer(object):

    def __init__(self, timeout):
        self.timeout = timeout
        self.slot_tasks = {}
        for i in range(1, timeout+1):
            self.slot_tasks[i] = {}
        '''
        slot0: {id: value}
        slot1: {id: value}
        '''

        self.task_slot_index = {}
        self.cursor = 1

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


def execute(rb):
    import copy
    while 1:
        print 'tip'
        time.sleep(1)
        cur = rb.next()
        res = rb.slot_tasks.get(cur)
        res = copy.deepcopy(res)
        rb.slot_tasks[cur] = {}
        print res
        for i in res:
            print 'alert: ', i


def feed(rb):
    time.sleep(1)
    for i in range(300):
        ts = int(time.time())
        rb.del_slot_task(i)
        slot = rb.add_slot_task(i, ts)
        rb.set_task_slot(i, slot)
        time.sleep(0.1)


def test():
    rb = RingBuffer(30)
    rb.next()

    # add
    rb.del_slot_task('nima')
    slot = rb.add_slot_task('nima')
    rb.set_task_slot('nima', slot)
    print 'add result:'
    print rb.slot_tasks
    print rb.task_slot_index
    rb.next()

    # add again
    rb.del_slot_task('wocao')
    slot = rb.add_slot_task('wocao')
    rb.set_task_slot('wocao', slot)
    print 'add result:'
    print rb.slot_tasks
    print rb.task_slot_index


def main():
    dis = []
    rb = RingBuffer(30)

    thread_1 = threading.Thread(target=execute, args=(rb,))
    thread_1.setDaemon(True)
    thread_1.start()

    thread_2 = threading.Thread(target=feed, args=(rb,))
    thread_2.setDaemon(True)
    thread_2.start()

    dis.append(thread_1)
    dis.append(thread_2)

    for t in dis:
        t.join()


if __name__ == "__main__":
    # test()
    main()
