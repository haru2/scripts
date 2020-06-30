##

'''Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.'''





def validparenth(input):
    result = []
    chars = {}
    chars['('] = ')'
    chars['{'] = '}'
    chars['['] = ']'

    for char in input:
        if "(" in char or "{" in char or "[" in char:
            result.append(char)
        else:
            print("char is {}" .format(char))

            if chars[result[-1]] == char:
                last = result.pop()
                print("last is {}" .format(last))
                continue

    if len(result) > 0:
        print(result)
        return("False")
    else:
        print(result)
        return("True")

print(validparenth('({})[]'))
