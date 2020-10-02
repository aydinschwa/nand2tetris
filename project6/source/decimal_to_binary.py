

def decimal_to_binary(num):
    num = int(num)
    new_num = ""
    for item in range(14, -1, -1):
        if num - 2**item >= 0:
            new_num += "1"
            num -= 2**item
        else:
            new_num += "0"
    return new_num




