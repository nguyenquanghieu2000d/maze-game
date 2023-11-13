from heapq import heappush, heappop, heapify
import numpy as np


class MinHeap:

    # Tạo 1 heap được tổ chức theo mảng, thực ra tổ chức theo cây nhị phân cũng đc nhưng thôi tổ chức bằng mảng cho nhanh
    def __init__(self):
        self.heap = []

    # Trả về nốt cha của nôt hiện tại
    def parent(self, i):
        return (i - 1) / 2

    # Thêm 1 phần tử mới vào trong heap với giá trị là k
    # ở đây sử dụng thư viên nên cũng k quá phức tạp, xem lại code C++ để biết thêm chi tiết
    def insertKey(self, k):
        heappush(self.heap, k)

    # Thay thế key ở vị trí i bằng 1 giá trị mới lưu ý rằng giá trị mới nhỏ hơn giá trị key hiên tại 
    def decreaseKey(self, i, new_val):
        self.heap[i] = new_val
        while (i != 0 and self.heap[self.parent(i)] > self.heap[i]):
            # THực hiện sắp xếp lại heap vì có giá trị mới truyền vào
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)], self.heap[i])

    # Cái này sẽ lấy ra phần tử ở đầu heap vì đây là Minheap vì thế phần tử được lấy ra sẽ có giá trị bé nhất trong toàn heap
    def extractMin(self):
        return heappop(self.heap)

    # Hàm này sẽ xóa key trong heap  
    def deleteKey(self, i):
        self.decreaseKey(i, float("-inf"))
        self.extractMin()

    # Lấy phần tử bé nhất trong heap
    def getMin(self):
        return self.heap[0]


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
    INF = 999999
    Set = np.ones(v + 1, dtype=int)
    Key = MinHeap()
    result = []
    for i in range(0, v + 1):
        Set[i] = False
        result[i][0] = -1
        result[i][1] = -1
    start = 1

    Key.insertKey([0, 1, 1])
    count = -1
    result.append([0, 1, 1])
    while start <= v:
        # print("---------------------------")
        # print(Set)
        # print(Key)
        # print(result)
        # print("---------------------------")
        ur = Key.extractMin()
        # display_sulf.blit()
        # print(ur)
        Set[ur[2]] = True
        result.append(ur)
        for i in range(1, v + 1):
            if adjMatrix[ur[1]][i] and Set[i] == False and adjMatrix[ur[1]][i] < Key[i][1]:
                Key[i][0] = ur[0]
                Key[i][1] = adjMatrix[ur[0], i]
        start += 1
    return result


# a = MinHeap()

a = np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 2, 1, 0, 0],
              [0, 2, 0, 9, 6, 0],
              [0, 1, 9, 0, 4, 8],
              [0, 0, 6, 4, 0, 5],
              [0, 0, 0, 8, 5, 0]])

print(prim(5, a))
