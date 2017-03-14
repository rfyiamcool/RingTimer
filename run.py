# coding:utf-8

import time
import threading

from ringtimer import RingBuffer


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
        # for i in res:
            # print 'alert: ', i


def feed(rb):
    time.sleep(1)
    for i in range(100000):
        ts = int(time.time())
        rb.del_slot_task(i)
        slot = rb.add_slot_task(i, ts)
        rb.set_task_slot(i, slot)
        time.sleep(0.1)


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
    main()
