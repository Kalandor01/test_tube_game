import math
import random
import os

r = random


# kémcsöves mobil játék
# variables

SCRAMBLE:bool = False
SCRAMBLE_NUM_MULTI:int = 1
TUBE_BOTTOM_SYMBOL:str = '█'
TUBE_WALL:str = '|'
TUBE_SEP:str = ' '
TUBES_SEP:str = "  "


moves:int = 0


def imput(sz:str):
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


def write(tube:list[list[int]]):
    print()
    # top numbers
    tube_len = int(math.log10(len(tube[0]))) + 1
    for xx in range(len(tube[0])):
        if len(tube[0]) >= 100 and (xx + 1) < 10:
            print(f"{TUBES_SEP}  {xx + 1}. ", end="")
        elif len(tube[0]) >= 100 and (xx + 1) < 100:
            print(f"{TUBES_SEP} {xx + 1}. ", end="")
        elif len(tube[0]) >= 10 and (xx + 1) < 10:
            print(f"{TUBES_SEP}  {xx + 1}.", end="")
        else:
            num_len = int(math.log10(xx + 1)) + 1
            len_diff = tube_len - num_len
            pre_len = math.floor(len_diff/2) + 1
            post_len = math.ceil(len_diff/2)
            # print(pre_len, post_len, len_diff)
            print(f"{TUBES_SEP}{TUBE_SEP * pre_len}{xx + 1}.{TUBE_SEP * post_len}", end="")
    print("\n")
    # tubes
    for xx in range(len(tube)):
        for yy in range(len(tube[0])):
            if tube[xx][yy] == 0:
                tube_content = TUBE_SEP * tube_len
            else:
                tube_content = TUBE_SEP * (tube_len - int(math.log10(tube[xx][yy]) + 1)) + str(tube[xx][yy])
            print(f"{TUBES_SEP}{TUBE_WALL}{tube_content}{TUBE_WALL}", end="")
        print()
    # tube bottom
    for _ in range(len(tube[0])):
        print(f"{TUBES_SEP}{TUBE_WALL}{TUBE_BOTTOM_SYMBOL * tube_len}{TUBE_WALL}", end="")
    print()


def modify(tube:list[list[int]], scramble=False):
    global moves
    good = False
    while not good:
        if not scramble:
            mod1 = imput("Kérem a kémcső számát amiből át akarja helyezni(0 = ujrakezdés): ") - 1
            if mod1 == -1:
                return -1
            mod2 = imput("Kérem a kémcső számát amibe át akarja helyezni: ") - 1
        else:
            mod1 = r.randint(0, len(tube[0]) - 1)
            mod2 = r.randint(0, len(tube[0]) - 1)
        if scramble or (0 <= mod1 < len(tube[0]) and 0 <= mod2 < len(tube[0])):
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
                if not scramble:
                    moves += 1
                # move to empty
                if mod2_i == -1:
                    tube[len(tube) - 1][mod2] = tube[mod1_i][mod1]
                    tube[mod1_i][mod1] = 0
                # move to not empty
                else:
                    re = tube[mod2_i - 1][mod2]
                    tube[mod2_i - 1][mod2] = tube[mod1_i][mod1]
                    tube[mod1_i][mod1] = re
            else:
                if not scramble:
                    print("\nNem jó számok!")
                    return tube
                else:
                    return -1
        else:
            if not scramble:
                print("\nNem jó számok!")
                return tube
            else:
                return -1
    return tube


def check(tube:list[list[int]]):
    for xx in range(len(tube)):
        for yy in range(len(tube[0])):
            if xx != len(tube) - 1 and yy != len(tube[0]) - 1 and tube[xx][yy] != tube[xx + 1][yy]:
                return False
    return True


def main():
    global moves

    width = imput("Szélesség: ")
    height = imput("Magasság: ")
    size:tuple[int, int] = (width, height)

    reset = True
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

        if not SCRAMBLE:
            # tube numbers
            nums = []
            for _ in range(size[0] - 1):
                nums.append(size[1])

            # populate tubes
            for x in range(size[1]):
                tubes.append([])
                for _ in range(size[0] - 1):
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
            for _ in range(round(SCRAMBLE_NUM_MULTI * size[0] * size[1])):
                result = -1
                while result == -1:
                    result = modify(tubes, True)
                write(tubes)

        while not reset and not check(tubes):
            write(tubes)
            response = modify(tubes)
            if response == -1:
                reset = True
                pass
            else:
                tubes = response
        if not reset:
            write(tubes)
            print(os.path.join(os.getcwd(), "scores.txt"))
            with open(os.path.join(os.getcwd(), "scores.txt"), "a") as f:
                f.write(f"[{size[0]}, {size[1]}]: {moves}\n")
            new = input(f"\nNyertél.\nLépések: {moves}\nÚjra?(Y/N):")
            if new.upper() == "Y":
                reset = True


if __name__ == "__main__":
    main()
