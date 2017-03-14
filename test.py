#coding: utf-8

from ringtimer import RingBuffer


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


if __name__ == "__main__":
    test()
