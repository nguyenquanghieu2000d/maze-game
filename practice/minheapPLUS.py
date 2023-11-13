import numpy as np


class MinHeap:
    def __init__(self, capacity):
        self.heap = []
        self.pos = []

        # for i in range(0, capacity):
        #     self.heap.append([i, i, 99999999])
        #     self.pos.append(i)

        self.heapSize = -1
        self.capacity = capacity

    def printheap(self):
        print(self.heap[0:self.heapSize + 1])

    def getParent(self, idx):
        return int(idx / 2)

    def getLeft(self, idx):
        return int(idx * 2)

    def getRight(self, idx):
        return int(idx * 2 + 1)

    def swapPos(self, a, b):
        temp = self.pos[a]
        self.pos[a] = self.pos[b]
        self.pos[b] = temp

    def swapMinHeapNode(self, a, b):
        temp = self.heap[a]
        self.heap[a] = self.heap[b]
        self.heap[b] = temp

    def insertKey(self, src, dest, weight):
        self.heapSize += 1
        if self.heapSize == self.capacity:
            print("Overflow")
            return
        else:
            self.heap[self.heapSize][0] = src
            self.heap[self.heapSize][1] = dest
            self.heap[self.heapSize][2] = weight
            self.pos[self.heapSize] = self.heapSize

            i = self.heapSize
            while i > 1 and self.heap[self.getParent(i)][2] > self.heap[i][2]:
                self.swapPos(self.heap[self.getParent(i)][0], self.heap[i][0])
                self.swapMinHeapNode(self.getParent(i), i)
                i = self.getParent(i)
                # print("PKOK")

    def minHeapify(self, idx):
        smallest = idx

        # print("okok: " + str(smallest))
        # print("OKOKO"+str(self.heap))
        if self.getLeft(idx) <= self.heapSize and self.heap[smallest][2] > self.heap[self.getLeft(idx)][2]:
            # print("IJIJIJ")
            smallest = self.getLeft(idx)
        if self.getRight(idx) <= self.heapSize and self.heap[smallest][2] > self.heap[self.getRight(idx)][2]:
            smallest = self.getRight(idx)
        if smallest != idx:
            self.swapPos(self.heap[smallest][0], self.heap[idx][0])
            self.swapMinHeapNode(smallest, idx)
            self.minHeapify(smallest)

    def extractMin(self):
        # print("Heap:::" + str(self.heap))
        if self.heapSize <= 0:
            return None
        elif self.heapSize == 1:
            self.heapSize -= 1
            return self.heap[1]
        else:
            result = self.heap[1]
            # print(result)
            lastNode = self.heap[self.heapSize]
            self.heap[1] = lastNode
            self.pos[lastNode[0]] = 1
            self.pos[result[0]] = self.heapSize
            self.heapSize -= 1
            # print("OOJOJ")
            # print(self.heap)
            self.minHeapify(1)
            # print("result" +str(result))
            return result

    def decreaseKey(self, src, dest, value):
        i = self.pos[src]
        self.heap[i][1] = dest
        self.heap[i][2] = value
        while i > 1 and self.heap[self.getParent(i)][2] > self.heap[i][2]:
            self.pos[self.heap[i][0]] = self.getParent(i)
            self.pos[self.heap[self.getParent(i)][0]] = i
            self.swapMinHeapNode(self.getParent(i), i)
            i = self.getParent(i)


# a = MinHeap(100)

# a.insertKey(1, 1, 9)
# a.insertKey(2, 8, 8)
# a.insertKey(3, 7, 1)

# a.printheap()


def minkey(Key, Set, V):
    INF = 99999
    min2 = INF
    for i in range(1, V + 1):
        if Key[i][1] < min2 and Set[i] == False:
            min1 = Key[i][0]
            min2 = Key[i][1]
            min3 = i
    return min3, min1, min2


tong123 = 0


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
    global tong123
    INF = 999999
    Set = np.ones(v + 1, dtype=int)
    Key = np.ones((v + 1, 2), dtype=int)
    result = np.zeros((v + 1, v + 1), dtype=int)
    heap = MinHeap(100)
    # print(heap.heap)
    for i in range(0, v + 1):
        Set[i] = False
        Key[i][0] = -1
        Key[i][1] = INF
        heap.heap.append([i, i, 99999])
        heap.heapSize += 1
        heap.pos.append(i)
        # result[i][0] = -1
        # result[i][1] = -1
    # print("OKOKOKO")
    # print(heap.heap)
    start = 1
    Key[1][1] = 1
    heap.decreaseKey(1, 1, 0)

    # print("sdkfjsyuuuuuuuuuuuuug")
    # print(heap.heap)
    # print(heap.pos)
    count = -1
    # result[start][0] = start
    # result[start][1] = 0
    while start <= v:

        # print("---------------------------")
        # print(Set)
        # print(Key)
        # print(result)
        # print("---------------------------")
        ur = heap.extractMin()
        tong123 += ur[2]
        print(ur)
        # display_sulf.blit()
        # print(ur)
        # print("njsfdhgshjk")
        Set[ur[0]] = True
        if ur[0] == -1 or ur[1] == -1 or ur[2] == -1:
            pass
        else:
            result[ur[0]][ur[1]] = 1
            result[ur[1]][ur[0]] = 1
        # print(result)
        # result[ur[0]][0] = ur[1]
        # result[ur[0]][1] = ur[2]
        # break
        for i in range(1, v + 1):
            # print("Day LL : " + str(ur[0]) + " --- " + str(i) + " --- " + str(adjMatrix[ur[0]][i]))
            if adjMatrix[ur[0]][i] and Set[i] == False and adjMatrix[ur[0]][i] < Key[i][1]:
                # print("Day LL : " + str(ur[0]) + " --- " + str(i) + " --- " + str(adjMatrix[ur[0]][i]))
                Key[i][0] = ur[0]
                Key[i][1] = adjMatrix[ur[0], i]
                heap.decreaseKey(i, ur[0], adjMatrix[ur[0], i])
        start += 1
    return result


# a = np.array([[0, 0, 0, 0, 0, 0],
#               [0, 0, 2, 1, 0, 0],
#               [0, 2, 0, 9, 6, 0],
#               [0, 1, 9, 0, 4, 8],
#               [0, 0, 6, 4, 0, 5],
#               [0, 0, 0, 8, 5, 0]])
#
# a = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 40, 0, 49, 0, 0, 0, 0, 0],
#               [0, 40, 0, 40, 0, 12, 0, 0, 0, 0],
#               [0, 0, 40, 0, 0, 0, 8, 0, 0, 0],
#               [0, 49, 0, 0, 0, 92, 0, 68, 0, 0],
#               [0, 0, 12, 0, 92, 0, 35, 0, 77, 0],
#               [0, 0, 0, 8, 0, 35, 0, 55, 0, 29],
#               [0, 0, 0, 0, 68, 0, 55, 0, 45, 0],
#               [0, 0, 0, 0, 0, 77, 0, 45, 0, 79],
#               [0, 0, 0, 0, 0, 0, 29, 0, 79, 0]])

a = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 2, 0, 0, 0, 0],
              [0, 1, 0, 0, 2, 6, 9, 0],
              [0, 2, 0, 0, 4, 0, 0, 0],
              [0, 0, 2, 4, 0, 0, 0, 5],
              [0, 0, 6, 0, 0, 0, 0, 6],
              [0, 0, 9, 0, 0, 0, 0, 2],
              [0, 0, 0, 0, 5, 6, 2, 0]])

print(prim(7, a))
print(tong123)
