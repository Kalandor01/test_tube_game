import random
import os
import sys
r = random


# kémcsöves mobil játék
# variables
size = [5, 5]
scramble = False
scramble_num_multi = 1
reset = True
moves = 0


def imput(sz):
    good = False
    xx = -1
    while not good:
        good = True
        try:
            xx = int(input(sz))
        except ValueError:
            print("Nem szám!")
            good = False
    return xx


def write(tube):
    print()
    for xx in range(len(tube[0])):
        if len(tube[0]) >= 100 and (xx + 1) < 10:
            print(f"    {xx + 1}. ", end="")
        elif len(tube[0]) >= 100 and (xx + 1) < 100:
            print(f"   {xx + 1}. ", end="")
        elif len(tube[0]) >= 10 and (xx + 1) < 10:
            print(f"    {xx + 1}.", end="")
        else:
            print(f"   {xx + 1}.", end="")
    print("\n")
    for xx in range(len(tube)):
        for yy in range(len(tube[0])):
            if tube[xx][yy] == 0:
                if len(tube[0]) >= 100:
                    print("  |   |", end="")
                elif len(tube[0]) >= 10:
                    print("  |  |", end="")
                else:
                    print("  | |", end="")
            else:
                if len(tube[0]) >= 100 and tube[xx][yy] < 10:
                    print(f"  |  {tube[xx][yy]}|", end="")
                elif len(tube[0]) >= 100 and tube[xx][yy] < 100:
                    print(f"  | {tube[xx][yy]}|", end="")
                elif len(tube[0]) >= 10 and tube[xx][yy] < 10:
                    print(f"  | {tube[xx][yy]}|", end="")
                else:
                    print(f"  |{tube[xx][yy]}|", end="")
        print()
    for _ in range(len(tube[0])):
        if len(tube[0]) >= 100:
            print("  |███|", end="")
        elif len(tube[0]) >= 10:
            print("  |██|", end="")
        else:
            print("  |█|", end="")
    print()


def modify(tube, scram=False):
    global moves
    good = False
    while not good:
        if not scram:
            mod1 = imput("Kérem a kémcső számát amiből át akarja helyezni(0 = ujrakezdés): ") - 1
            if mod1 == -1:
                return -1
            mod2 = imput("Kérem a kémcső számát amibe át akarja helyezni: ") - 1
        else:
            mod1 = r.randint(0, len(tube[0]) - 1)
            mod2 = r.randint(0, len(tube[0]) - 1)
        if scram or (0 <= mod1 < len(tube[0]) and 0 <= mod2 < len(tube[0])):
            mod1_i = -1
            mod2_i = -1
            for xx in range(len(tube)):
                if tube[xx][mod1] != 0:
                    mod1_i = xx
                    break
            for xx in range(len(tube)):
                if tube[xx][mod2] != 0:
                    mod2_i = xx
                    break
            # print(mod1, mod2, mod1_i, mod2_i, tube[mod1_i][mod1], tube[mod2_i][mod2])
            if mod1_i != -1 and mod2_i != 0 and (mod2_i == -1 or tube[mod2_i][mod2] == tube[mod1_i][mod1]) and mod1 != mod2:
                good = True
                moves += 1
                if mod2_i == -1:
                    re = tube[mod2_i][mod2]
                    tube[mod2_i][mod2] = tube[mod1_i][mod1]
                    tube[mod1_i][mod1] = re
                else:
                    re = tube[mod2_i - 1][mod2]
                    tube[mod2_i - 1][mod2] = tube[mod1_i][mod1]
                    tube[mod1_i][mod1] = re
            else:
                print("\nNem jó számok!")
                return tube
        else:
            print("\nNem jó számok!")
            return tube
    return tube


def check(tube):
    for xx in range(len(tube)):
        for yy in range(len(tube[0])):
            if xx != len(tube) - 1 and yy != len(tube[0]) - 1 and tube[xx][yy] != tube[xx + 1][yy]:
                return False
    return True


size[0] = imput("Szélesség: ")
size[1] = imput("Magasság: ")
while reset:
    moves = 0
    try:
        seed = int(input("\nSeed?: "))
    except ValueError:
        seed = r.randint(-1000000, 1000000)
        print(f"Seed: {seed}\n")
    r.seed(seed)
    reset = False
    tubes:list[list[int]] = []

    if not scramble:
        # tube numbers
        nums = []
        for _ in range(size[0] - 1):
            nums.append(size[1])

        # populate tubes
        for x in range(size[1]):
            tubes.append([])
            for y in range(size[0] - 1):
                num = r.randint(1, size[0] - 1)
                while nums[num - 1] <= 0:
                    num = r.randint(1, size[0] - 1)
                nums[num - 1] -= 1
                tubes[x].append(num)
            tubes[x].append(0)
    else:
        # populate tube
        tube_row = []
        for x in range(size[0] - 1):
            tube_row.append(x + 1)
        tube_row.append(0)
        for x in range(size[1]):
            tubes.append(tube_row)
        # scramble
        for _ in range(round(scramble_num_multi * size[0] * size[1])):
            modify(tubes, True)
            write(tubes)

    while not reset and not check(tubes):
        write(tubes)
        tubes = modify(tubes)
        if tubes == -1:
            reset = True
    if not reset:
        write(tubes)
        print(os.path.join(os.getcwd(), "scores.txt"))
        with open(os.path.join(os.getcwd(), "scores.txt"), "a") as f:
            f.write(f"[{size[0]}, {size[1]}]: {moves}\n")
        new = input(f"\nNyertél.\nLépések: {moves}\nÚjra?(Y/N):")
        if new.upper() == "Y":
            reset = True
