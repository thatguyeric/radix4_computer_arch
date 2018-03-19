#
# Eric Marcondes & Jared Curry Simulator for custom instruction set for Radix 4.
#
#


def open_file(f):
    file = open(f, 'r').read().lower().split('\n')
    for i in file:
        if i:
            instructions.append(i.split()) 


def print_error(inst, line):
    error = inst + " on line " + str(line) + " is not a valid instruction"
    print(error)
    exit(1)


def store_to_reg(reg, value):
    global r1, r2, r3, r4, r5
    if reg == "r1":
        r1 = value
    elif reg == "r2":
        r2 = value
    elif reg == "r3":
        r3 = value
    elif reg == "r4":
        r4 = value
    elif reg == "r5":
        r5 = value
    else:
        print("register " + reg + " does not exist")
        exit(1)


def lw(inst):
    number = inst[1]
    one = format(1, "016b")
    inverted_number = ''
    if number[0] == '-':
        number = number[1:]
        number = format(int(number), "016b")
        for b in number:
            if b == '0':
                inverted_number += '1'
            else:
                inverted_number += '0'
        number = bit_add(inverted_number, one)
    else:
        number = format(int(number), "016b")
    store_to_reg(inst[2], number)


def ext():
    global r1, r2
    r1 = format(int(r1, 2), "032b")
    r1 += '0'
    r2 = format(int(r2, 2), "016b")
    r2 += '00000000000000000'


def bit_add(a, b):
    c = format(0, "033b")
    c = list(c)
    bit_add_summ = ''
    for i in range(len(b)):
        if int(a[len(a)-1-i]) + int(b[len(b)-1-i]) + int(c[len(c)-1-i]) == 2:
            c[len(c)-2-i] = '1'
            bit_add_summ += '0'
        elif int(a[len(a)-1-i]) + int(b[len(b)-1-i]) + int(c[len(c)-1-i]) == 3:
            c[len(c) - 2 - i] = '1'
            bit_add_summ += '1'
        else:
            bit_add_summ += str(int(a[len(a)-1-i]) + int(b[len(b)-1-i]) + int(c[len(c)-1-i]))
    return bit_add_summ[::-1]


def twc(inst, index):
    global r2, r3, r4, r5
    inverted_reg = ''
    one = format(1, "033b")
    if inst[1] == "r2" and inst[2] == "r3":
        for b in r2:
            if b == '0':
                inverted_reg += '1'
            else:
                inverted_reg += '0'
        r3 = bit_add(inverted_reg, one)

    elif inst[1] == "r4" and inst[2] == "r5":
        for b in r4:
            if b == '0':
                inverted_reg += '1'
            else:
                inverted_reg += '0'
        r5 = bit_add(inverted_reg, one)
    else:
        print("Error on line " + str(index))
        exit(1)


def add(inst, index):
    global r1, r2, r3, r4, r5
    if inst[3] == "r4":
        if inst[1] == inst[2] == "r2":
            r4 = bit_add(r2, r2)
        else:
            print("Error on line " + str(index))
            exit(1)
    elif inst[1] == "r1" and inst[3] == "r1":
        if inst[2] == "r2":
            r1 = bit_add(r1, r2)
        elif inst[2] == "r3":
            r1 = bit_add(r1, r3)
        elif inst[2] == "r4":
            r1 = bit_add(r1, r4)
        elif inst[2] == "r5":
            r1 = bit_add(r1, r5)
        else:
            print("Error on line " + str(index))
            exit(1)
    else:
        print("Error on line " + str(index))
        exit(1)


def sh(inst, index):
    global r1
    # removes the last two bits and shifts in 2 bits for the final product
    if inst[1] == "r1":
        if r1[0] == '1':
            r1 = r1[::-1]
            r1 += '11'
            r1 = r1[::-1]
            r1 = r1[:-2]
        else:
            r1 = r1[::-1]
            r1 += '00'
            r1 = r1[::-1]
            r1 = r1[:-2]
    else:
        print("Error on line " + str(index))
        exit(1)


def pop(inst, index):
    global r1
    if inst[1] == "r1":
        r1 = r1[:-1]
    else:
        print("Error on line " + str(index))
        exit(1)


def lut(inst, index):
    global r1, r2, r3, r4, r5
    for n in range(8):
        if r1[-3:] == '000' or r1[-3:] == '111':
            sh(inst, index)
        elif r1[-3:] == '001' or r1[-3:] == '010':
            r1 = bit_add(r1, r2)
            sh(inst, index)
        elif r1[-3:] == '011':
            r1 = bit_add(r1, r4)
            sh(inst, index)
        elif r1[-3:] == '100':
            r1 = bit_add(r1, r5)
            sh(inst, index)
        elif r1[-3:] == '101' or r1[-3:] == '110':
            r1 = bit_add(r1, r3)
            sh(inst, index)
        else:
            print("How did you get this far without running into an error already??")
            exit(1)


def instruction_handler():
    for index, i in enumerate(instructions):
        if i[0] == "add":
            add(i, index+1)
        elif i[0] == "twc":
            twc(i, index+1)
        elif i[0] == "pop":
            pop(i, index+1)
        elif i[0] == "lw":
            lw(i)
        elif i[0] == "ext":
            ext()
        elif i[0] == "lut":
            lut(i, index+1)
        else:
            print_error(i[0], index+1)
            exit(1)


if __name__ == "__main__":
    instructions = []
    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0
    r5 = 0
    filename = "booths.txt"
    open_file(filename)
    instruction_handler()
    print(r1)

