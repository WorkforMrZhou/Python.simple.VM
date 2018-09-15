from __future__ import print_function
from collections import deque

import sys


class Stack(deque):
    push = deque.append

    def top(self):
        return self[-1]


class Machine:
    def __init__(self, code):
        self.data_stack = Stack()
        self.return_addr_stack = Stack()
        self.instruction_pointer = 0
        # code 是一个 list，是一系列的 token
        self.code = code

    def pop(self):
        return self.data_stack.pop()

    def push(self, value):
        self.data_stack.push(value)

    def top(self):
        return self.data_stack.top()

    def run(self):
        while self.instruction_pointer < len(self.code):
            opcode = self.code[self.instruction_pointer]
            self.instruction_pointer += 1
            self.dispatch(opcode)

    def dispatch(self, op):
        dispatch_map = {
            # "%":                self.mod,
            "*":                self.mul,
            "+":                self.plus,
            "-":                self.minus,
            "/":                self.div,
            # "==":               self.eq,
            "cast_int":         self.cast_int,
            "cast_str":         self.cast_str,
            # "drop":             self.drop,
            # "dup":              self.dup,
            "if":               self.if_stmt,
            "jmp":              self.jmp,
            "over":             self.over,
            "print":            self.print_,
            "println":          self.println,
            "read":             self.read,
            # "stack":            self.dump_stack,
            # "swap":             self.swap,
        }

        if op in dispatch_map:
            dispatch_map[op]()
        elif isinstance(op, int):
            self.push(op)
        elif isinstance(op, str) and op[0] == op[-1] == '"':
            self.push(op[1:-1])
        else:
            raise RuntimeError("unknown opcode: {}".format(op))

    def mul(self):
        self.push(self.pop() * self.pop())

    def plus(self):
        self.push(self.pop() + self.pop())

    def minus(self):
        last = self.pop()
        self.push(self.pop() - last)

    def div(self):
        last = self.pop()
        self.push(self.pop() / last)

    def print_(self):
        sys.stdout.write(str(self.pop()))
        sys.stdout.flush()

    def println(self):
        sys.stdout.write("{}\n".format(self.pop()))
        sys.stdout.flush()

    def jmp(self):
        addr = self.pop()
        if isinstance(addr, int) and 0 <= addr < len(self.code):
            self.instruction_pointer = addr
        else:
            raise RuntimeError("Jump address must be a valid integer.")

    def if_stmt(self):
        false_clause = self.pop()
        true_clause = self.pop()
        condition = self.pop()
        self.push(true_clause if condition else false_clause)

    def cast_int(self):
        self.push(int(self.pop()))

    def cast_str(self):
        self.push(str(self.pop()))

    def read(self):
        token = input()
        self.push(token)

    def over(self):
        b = self.pop()
        a = self.pop()
        self.push(a)
        self.push(b)
        self.push(a)


Machine([
    '"Enter a number: "', "print", "read", "cast_int",
    '"Enter another number: "', "print", "read", "cast_int",
    "over", "over",
    '"Their sum is: "', "print", "+", "println",
    '"Their product is: "', "print", "*", "println"
]).run()