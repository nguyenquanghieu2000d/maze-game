import numpy as np




def minkey(Key, Set, V):
    INF = 99999
    min2 = INF
    for i in range(1, V + 1):
        if Key[i][1] < min2 and Set[i] == False:
            min1 = Key[i][0]
            min2 = Key[i][1]
            min3 = i
    return min3, min1, min2


def prim(v, adjMatrix):
    # [-1 - 1]
    # [1  0]
    # [1 66]
    # [2 58]
    # [1 60]
    # [2 55]
    # [3 53]
    # [4 31]
    # [9 18]
    # [6 56] 1 2 4 3 5 7 6
    INF = 999999
    Set = np.ones(v + 1, dtype=int)
    Key = np.ones((v + 1, 2), dtype=int)
    result = np.zeros((v + 1, v + 1), dtype=int)
    for i in range(0, v + 1):
        Set[i] = False
        Key[i][0] = -1
        Key[i][1] = INF
        # result[i][0] = -1
        # result[i][1] = -1
    start = 1
    Key[1][1] = 1

    count = -1
    # result[start][0] = start
    # result[start][1] = 0
    while start <= v:
        # print("---------------------------")
        # print(Set)
        # print(Key)
        # print(result)
        # print("---------------------------")
        ur = minkey(Key, Set, v)
        # display_sulf.blit()
        # print(ur)
        Set[ur[0]] = True
        if ur[0] == -1 or ur[1] == -1 or ur[2] == -1:
            pass
        else:
            result[ur[0]][ur[1]] = 1
            result[ur[1]][ur[0]] = 1
        print(result)
        # result[ur[0]][0] = ur[1]
        # result[ur[0]][1] = ur[2]
        for i in range(1, v + 1):
            if adjMatrix[ur[0]][i] and Set[i] == False and adjMatrix[ur[0]][i] < Key[i][1]:
                Key[i][0] = ur[0]
                Key[i][1] = adjMatrix[ur[0], i]
        start += 1
    return result


a = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 2, 1, 0, 0],
              [0, 2, 0, 9, 6, 0],
              [0, 1, 9, 0, 4, 8],
              [0, 0, 6, 4, 0, 5],
              [0, 0, 0, 8, 5, 0]])

print(prim(5, a))
#
# [[0 0 0 0 0 0]
#  [0 1 1 1 0 0]
#  [0 1 0 0 0 0]
#  [0 1 0 0 1 0]
#  [0 0 0 1 0 1]
#  [0 0 0 0 1 0]]

# [[0 0 0 0 0 0]
#  [0 1 1 1 0 0]
#  [0 1 0 0 0 0]
#  [0 1 0 0 1 0]
#  [0 0 0 1 0 1]
#  [0 0 0 0 1 0]]
