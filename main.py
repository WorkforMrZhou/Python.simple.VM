from Machine import Machine


if __name__ == "__main__":
    Machine([
        '"Enter a number: "', "print", "read", "cast_int",
        '"The number "', "print", "dup", "print", '" is "', "print",
        2, "%", 0, "==", '"even."', '"odd."', "if", "println",
        0, "jmp",
    ]).run()

    # Machine([
    #     '"Enter a number: "', "print", "read", "cast_int",
    #     '"Enter another number: "', "print", "read", "cast_int",
    #     "over", "over",
    #     '"Their sum is: "', "print", "+", "println",
    #     '"Their product is: "', "print", "*", "println"
    # ]).run()
