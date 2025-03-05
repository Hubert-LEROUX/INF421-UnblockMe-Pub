"""
This document contains the implementation of a heap.
"""

class My_heap:
    def __init__(self):
        self.heap = []
        self.size = 0


    def find_id_father(self, id_child):
        return (id_child - 1) // 2

    def find_id_left_son(self, id_father):
        return 2 * id_father + 1

    def find_id_right_son(self, id_father):
        return 2 * id_father + 2


    def is_empty(self):
        return self.size == 0

    def push(self, x):
        self.heap.append(x)
        self.size += 1

        id_child = self.size - 1
        while id_child >= 1: # while not root
            id_father = self.find_id_father(id_child)
            if self.heap[id_child] < self.heap[id_father]:
                self.heap[id_child], self.heap[id_father] = self.heap[id_father], self.heap[id_child]
                id_child = id_father
            else:
                break


    def pop(self):
        if self.size == 0:
            return None

        # swap root with last element and delete last element
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        self.size -= 1

        id_father = 0
        while True:
            id_left_son = self.find_id_left_son(id_father)
            id_right_son = self.find_id_right_son(id_father)

            if id_left_son >= self.size:
                break

            if id_right_son >= self.size:
                id_son = id_left_son
            else:
                id_son = id_left_son if self.heap[id_left_son] < self.heap[id_right_son] else id_right_son

            if self.heap[id_son] < self.heap[id_father]:
                self.heap[id_son], self.heap[id_father] = self.heap[id_father], self.heap[id_son]
                id_father = id_son
            else:
                break

        return  self.heap.pop()
    
def heapify(l):
    tas = My_heap()
    for x in l:
        tas.push(x)
    return tas

