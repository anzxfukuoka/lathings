import sys
import numpy as np

#велик
class Logger:
    def __init__(self):
        self._log = ""

    def log(self, s):
        self._log += str(s) + "\n"

    def get(self):
        return self._log


def from_str(strmatr):
    matr = []
    for sm in strmatr:
        sm = sm.strip().split(" ")
        matr.append(sm)
    matr = np.array(matr)
    matr = matr.astype(np.int)
    return matr

# djpdhfodtn rjjabwbtyn
def _devieble(a, b):
    if b == 0 or abs(a) > abs(b):
        return None  # err
    else:
        return b // a


def stairs(n, m, matr):

    log = Logger()

    log.log(matr)

    collum = 0
    line = 0

    out = 0

    while collum < m and line < n:  # for collum in range(m):

        while (out < 100):
            out += 1

            # массив столбец (диогональ)
            c = matr[line:, collum]

            # максимальный в столбце
            # не равный 0
            nzc = np.setdiff1d(c, [0])
            if nzc.any():  # count_nonzero != 0
                min_ = np.absolute(nzc).min()  # -0
            else:
                # нулевой столбец
                collum += 1
                continue

            # list(m).index(c.min())
            min_i = list(np.absolute(c)).index(min_) + line

            # на первое место
            matr[[min_i, line]] = matr[[line, min_i]]  # swap

            # log
            #print("меняем мнстами " + str(min_i + 1) + "ю и " + str(line + 1) + "ю стороку")
            #print("L" + str(min_i + 1) + " <--> " + "L" + str(line + 1))

            log.log("меняем мнстами " + str(min_i + 1) + "ю и " + str(line + 1) + "ю стороку")
            log.log("L" + str(min_i + 1) + " <--> " + "L" + str(line + 1))

            #print(matr)
            #print("---------")

            log.log(matr)
            log.log("---------")

            # стравниваем 1 со всеми остальными:
            for io in range(line + 1, n):
                a = matr[line][collum]  # ведущий
                b = matr[io][collum]  # остальные

                k = _devieble(a, b)

                if (k):
                    # отнимаем из строчки первую
                    matr[io] -= matr[line] * k

                    # log
                    #print("отнимает от " + str(io + 1) + "й строки " + str(line + 1) + "ю, умноженную на" + str(k))
                    #print("L" + str(io + 1) + " - " + str(k) + " * L" + str(line + 1))

                    log.log("отнимает от " + str(io + 1) + "й строки " + str(line + 1) + "ю, умноженную на" + str(k))
                    log.log("L" + str(io + 1) + " - " + str(k) + " * L" + str(line + 1))

                #print(matr)
                #print("---------")

                log.log(matr)
                log.log("---------")


            # если стольбик 0
            nc = matr[line + 1:, collum]
            if np.count_nonzero(nc) == 0:
                break

        collum += 1
        line += 1

    return log.get()


# debug
if __name__ == "__main__":
    n = 3
    m = 2

    matr = [[2, 2],[3, 4]]
    matr = np.array(matr)

    print(stairs(n, m, matr))
