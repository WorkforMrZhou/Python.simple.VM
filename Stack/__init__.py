from collections import deque


class Stack(deque):
    push = deque.append

    def top(self):
        return self[-1]