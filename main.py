from Machine import Machine
import tokenize
from io import StringIO


# 可迭代，一次生成一个 token
def parse(text):
    tokens = tokenize.generate_tokens(StringIO(text).readline)
    for token_num, token_val, _, _, _ in tokens:
        if token_num == tokenize.NUMBER:
            yield int(token_val)
        elif token_num in [tokenize.OP, tokenize.STRING, tokenize.NAME]:
            yield token_val
        elif token_num == tokenize.ENDMARKER:
            break
        else:
            raise RuntimeError("Unknown token {}: {}".format(tokenize.tok_name[token_num], token_val))


# 可以做一个常亮折叠，即预先计算出四则运算的结果，但会导致 jump 的地址改变
# 所以需要只允许jump 到带有名字的 label 上，而不是具体的地址，这样才能够在进行常量折叠后解析出真正的地址


def repl():
    print('Press CTRL + D or type "exit" to quit')

    while True:
        try:
            source = input("> ")
            # 将生成器转为列表
            code = list(parse(source))
            Machine(code).run()
        except(RuntimeError, IndexError) as e:
            print("IndexError: {}".format(e))
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break


if __name__ == "__main__":
    # Machine([
    #     '"Enter a number: "', "print", "read", "cast_int",
    #     '"The number "', "print", "dup", "print", '" is "', "print",
    #     2, "%", 0, "==", '"even."', '"odd."', "if", "println",
    #     0, "jmp",
    # ]).run()

    # Machine([
    #     '"Enter a number: "', "print", "read", "cast_int",
    #     '"Enter another number: "', "print", "read", "cast_int",
    #     "over", "over",
    #     '"Their sum is: "', "print", "+", "println",
    #     '"Their product is: "', "print", "*", "println"
    # ]).run()

    repl()
