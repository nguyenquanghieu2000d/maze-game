import copy
import queue
import random
import time

import numpy as np
import pygame
# Nhap mon tri tue nhan tao UPDATE
from numpy import random
from pqdict import pqdict
from pygame.locals import *

#
################## READ ME ###########################
######### SỬA CÁC THAM SỐ SAU ĐỂ ĐẠT ĐƯỢC KẾT QUẢ MONG MUỐN #######################

CHIEU_CAO = 18  # Chiều cao của mê cung
CHIEU_DAI = 39  # Chiều dài của mê cung
KICH_THUOC_KHUNG_HINH = (1300, 700)  # Đặt kích thước khung hình

#####################################################################################


margin_top = 100
margin_left = 20


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

    #
    # def insertKey(self, src, dest, weight):
    #     self.heapSize += 1
    #     if self.heapSize == self.capacity:
    #         print("Overflow")
    #         return
    #     else:
    #         self.heap[self.heapSize][0] = src
    #         self.heap[self.heapSize][1] = dest
    #         self.heap[self.heapSize][2] = weight
    #         self.pos[self.heapSize] = self.heapSize
    #
    #         i = self.heapSize
    #         while i > 1 and self.heap[self.getParent(i)][2] > self.heap[i][2]:
    #             self.swapPos(self.heap[self.getParent(i)][0], self.heap[i][0])
    #             self.swapMinHeapNode(self.getParent(i), i)
    #             i = self.getParent(i)
    #             # print("PKOK")

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


class MazeAndPlayer:

    def moveRight(self, display):

        # print(display.get_at((self.x + 28, self.y)))
        if display.get_at((self.x + 28, self.y)) == (255, 255, 255, 255):
            self.viTri += 1
            self.x = self.x + self.speed

    def moveLeft(self, display):

        if display.get_at((self.x - 4, self.y)) == (255, 255, 255, 255):
            self.viTri -= 1
            self.x = self.x - self.speed

    def moveUp(self, display):
        if (display.get_at((self.x, self.y - 4))) == (255, 255, 255, 255):
            self.viTri -= self.width
            self.y = self.y - self.speed

    def moveDown(self, display):
        if (display.get_at((self.x, self.y + 28))) == (255, 255, 255, 255):
            self.viTri += self.width
            self.y = self.y + self.speed

    # 2 biến này là tọa độ của nhân vật trong game, speed là tốc độ di chuyển
    x = 4 + 3 + margin_left
    y = 4 + 3 + margin_top
    speed = 32

    def __init__(self):
        self.INF = 9999999
        # Chiều cao và chiều rộng của ma trận
        self.height = CHIEU_CAO
        self.width = CHIEU_DAI
        self.v = self.width * self.height
        # Ma trận trọng số của đồ thị
        self.adjMatrix = self.makeMaze()
        self.Check = False
        self.maze, self.maze2, self.maze3 = self.prim2ThongDuong(self.adjMatrix)
        # random từ 2 nếu k sẽ trùng với thằng nhân vật
        self.dich = self.v
        self.viTri = 1
        self.path = self.ASaoAlgorithm()
        # Vị trí của thằng nhân vật

    def makeMaze(self):
        adjMatrix = np.zeros((self.v + 1, self.v + 1), dtype=int)
        adjList = dict()
        x = self.width + 1
        y = 2
        # print(self.v)
        for i in range(1, self.v + 1):
            # print(x, y)
            # Cái này là chọn nối các điểm trong đồ thị theo chiều dọc
            # Ví dụ :
            #   1 2 3
            #   | | |
            #   4 5 6
            if x <= self.v:
                adjMatrix[i][x] = random.randint(0, 100)
                adjMatrix[x][i] = adjMatrix[i][x]
                temp1 = random.randint(0, 100)
                if i not in adjList:
                    adjList[i] = dict()
                    adjList[i]['dist'] = list()
                adjList[i]['dist'].append((x, temp1))
                adjList[i]['g'] = self.INF
                adjList[i]['f'] = self.INF
                if x not in adjList:
                    adjList[x] = dict()
                    adjList[x]['dist'] = list()
                adjList[x]['dist'].append((i, temp1))
                adjList[x]['g'] = self.INF
                adjList[x]['f'] = self.INF

            # Cái này sẽ chọn nối điểm bên cạnh nó trong đồ thị
            # Ví dụ
            #
            # 1 - 2 - 3
            # 4 - 5 - 6
            #
            if i % self.width != 0 and y <= self.v:
                temp2 = random.randint(0, 100)
                adjMatrix[y][i] = random.randint(0, 100)
                adjMatrix[i][y] = adjMatrix[y][i]
                if i not in adjList:
                    adjList[i] = dict()
                    adjList[i]['dist'] = list()
                adjList[i]['dist'].append((y, temp2))
                adjList[i]['g'] = self.INF
                adjList[i]['f'] = self.INF
                if y not in adjList:
                    adjList[y] = dict()
                    adjList[y]['dist'] = list()
                adjList[y]['dist'].append((i, temp2))
                adjList[y]['g'] = self.INF
                adjList[y]['f'] = self.INF

                # adjList[i]['g'] = 0
                # adjList[i]['f'] = 0
                # adjList[i].insert(0, [y, temp2])
                # adjList[y].insert(0, [i, temp2])
                # adjList[y]['g'] = 0
                # adjList[y]['f'] = 0
            # if i == 1:
            #     adjMatrix[y][i] = random.randint(0, 100)
            #     adjMatrix[i][y] = adjMatrix[y][i]
            x += 1
            y += 1
        # print("Day la adjMatrix: ")
        # print(adjMatrix)
        # print(adjList)
        # print(adjList[1])
        return adjList

    def minkey(self, Key, Set, V):
        INF = 99999
        min2 = INF
        for i in range(1, V + 1):
            if Key[i][1] < min2 and Set[i] == False:
                min1 = Key[i][0]
                min2 = Key[i][1]
                min3 = i
        return min3, min1, min2

    def bfs(self):
        # print(self.maze3)
        # self.ASaoAlgorithm()
        truyvet = np.zeros(self.v + 1, dtype=int)
        path = []
        KiemTraDuyet = np.zeros(self.v + 1, dtype=int)
        hangChoDuyet = queue.Queue()
        hangChoDuyet.queue.append(self.viTri)

        while not hangChoDuyet.empty():
            a = hangChoDuyet.get()
            # print(a)
            # path.append(a)

            # print("Gia tri lay ra: " + str(a))
            if self.dich == a:
                break
            KiemTraDuyet[a] = 1
            for i in range(1, self.maze2.shape[0]):
                # print("So sanh 2 gia tri: " + str(i) + " va " + str(self.maze[i][0]) + " va " + str(a))
                if self.maze2[a][i] == 1 and KiemTraDuyet[i] == 0:
                    hangChoDuyet.queue.append(i)
                    KiemTraDuyet[i] = 1
                    truyvet[i] = a
        # print(truyvet)
        # print("duyet: " + str(self.path))
        u = self.dich
        # path.append(u)
        # count = 0
        # print(truyvet)
        while truyvet[u] != 0:
            # count+= 1
            path.append(truyvet[u])
            u = truyvet[u]
        path.sort()
        # print("==============================================")
        # print(path)
        # print("==============================================")
        return path

    # Nhap mon tri tue nhan tao UPDATE

    #
    def ASaoAlgorithm(self):
        self.bfs()
        # viTri
        # dich
        # make3
        # print(self.maze3)
        start = self.viTri

        goal = self.dich
        graph = copy.deepcopy(self.maze3)
        dinh = self.width * self.height
        # print(start)
        # print(goal)
        # print(graph)
        # Con van de ve h g va f
        INF = 99999999
        Open = pqdict()
        Close = dict()
        Father = dict()
        for i in range(1, int(dinh) + 1):
            Close[i] = False
            Open[i] = INF
            Father[i] = -1

        Open[start] = 0

        graph[start]['g'] = 0
        while True:
            x = Open.pop()
            Close[x] = True
            # print("x: " + str(x))
            if (x == goal):
                print("Tim kiem thanh cong")
                break
            for i in graph[x]['dist']:
                # print("i: " + str(i))
                dist = i
                weight = 0
                g = graph[x]['g'] + weight
                f = g + int(graph[dist]['h'])
                # print("day la dist: " + str(dist))
                # print(Open[str(dist)])

                if dist in Open:
                    if f < graph[dist]['f']:
                        Open[dist] = f
                        Father[dist] = x
                        graph[dist]['g'] = g
                        graph[dist]['f'] = f
                elif Close[dist]:
                    if f < graph[dist]['f']:
                        Open[dist] = f
                        Father[dist] = x
                        graph[dist]['g'] = g
                        graph[dist]['f'] = f
                else:
                    graph[dist]['g'] = g
                    graph[dist]['h'] = f
                    Open[dist] = f
                    Father[dist] = x
        u = int(goal)
        path = []
        # print(u)
        # path.append(u)
        # print(Father)
        while Father[u] != start:
            path.append(Father[u])
            # print(Father[u])
            # print(type(Father[u]))
            u = Father[u]
        path.append(start)
        path.sort()
        # print(start)
        # print("++++++++++++++++++++")
        # print(path)
        # print("++++++++++++++++++++")
        # print(start)
        # print("+=++++++======+++++=====")
        return path
        # print("----------------")

    def prim(self, adjMatrix):
        start1 = time.time()

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
        Set = np.ones(self.v + 1, dtype=int)
        Key = np.ones((self.v + 1, 2), dtype=int)
        result = np.ones((self.v + 1, 2), dtype=int)
        result2 = np.zeros((self.v + 1, self.v + 1), dtype=int)
        for i in range(0, self.v + 1):
            Set[i] = False
            Key[i][0] = -1
            Key[i][1] = INF
            result[i][0] = -1
            result[i][1] = -1
        start = 1
        Key[1][1] = 0
        Key[1][0] = 1
        count = -1
        result[start][0] = start
        result[start][1] = 0

        while start <= self.v:
            ur = self.minkey(Key, Set, self.v)
            if ur[0] == -1 or ur[1] == -1 or ur[2] == -1:
                pass
            else:
                result2[ur[0]][ur[1]] = 1
                result2[ur[1]][ur[0]] = 1
            # display_sulf.blit()
            # print(ur)
            Set[ur[0]] = True
            result[ur[0]][0] = ur[1]
            result[ur[0]][1] = ur[2]
            for i in range(1, self.v + 1):
                if adjMatrix[ur[0]][i] and Set[i] == False and adjMatrix[ur[0]][i] < Key[i][1]:
                    Key[i][0] = ur[0]
                    Key[i][1] = adjMatrix[ur[0], i]
            start += 1
        end = time.time()
        print("Thời gian chạy của Prim ma trận kề với tìm kiếm tuyến tính: " + str(end - start1))

        return result, result2

    def prim2(self, adjMatrix):

        start1 = time.time()
        INF = 999999
        Set = np.ones(self.v + 1, dtype=int)
        Key = np.ones((self.v + 1, 2), dtype=int)
        result = np.ones((self.v + 1, 2), dtype=int)
        result2 = np.zeros((self.v + 1, self.v + 1), dtype=int)
        result3 = dict()
        heap = MinHeap(100)
        # print(heap.heap)
        for i in range(0, self.v + 1):
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
        while start <= self.v:

            # print("---------------------------")
            # print(Set)
            # print(Key)
            # print(result)
            # print("---------------------------")
            ur = heap.extractMin()
            # print(ur)
            # display_sulf.blit()
            # print(ur)
            # print("njsfdhgshjk")
            # Set[ur[0]] = True
            # if ur[0] == -1 or ur[1] == -1 or ur[2] == -1:
            #     pass
            # else:
            #     result2[ur[0]][ur[1]] = 1
            #     result2[ur[1]][ur[0]] = 1

            if ur[0] == -1 or ur[1] == -1 or ur[2] == -1:
                pass
            else:

                if not ur[0] in result3:
                    result3[ur[0]] = dict()
                    result3[ur[0]]['dist'] = list()
                result3[ur[0]]['dist'].append(ur[1])
                result3[ur[1]]['dist'].append(ur[0])
                result3[ur[0]]['g'] = self.INF
                result3[ur[1]]['g'] = self.INF
                result3[ur[0]]['f'] = self.INF
                result3[ur[1]]['f'] = self.INF
                result3[ur[0]]['h'] = ur[0]
                result3[ur[1]]['h'] = ur[1]

                result2[ur[0]][ur[1]] = 1
                result2[ur[1]][ur[0]] = 1
                # display_sulf.blit()
                # print(ur)
            Set[ur[0]] = True
            result[ur[0]][0] = ur[1]
            result[ur[0]][1] = ur[2]

            # print(result)
            # result[ur[0]][0] = ur[1]
            # result[ur[0]][1] = ur[2]
            # break
            # for i in range(1, self.v + 1):
            #     # print("Day LL : " + str(ur[0]) + " --- " + str(i) + " --- " + str(adjMatrix[ur[0]][i]))
            #     if adjMatrix[ur[0]][i] and Set[i] == False and adjMatrix[ur[0]][i] < Key[i][1]:
            #         # print("Day LL : " + str(ur[0]) + " --- " + str(i) + " --- " + str(adjMatrix[ur[0]][i]))
            #         Key[i][0] = ur[0]
            #         Key[i][1] = adjMatrix[ur[0], i]
            #         heap.decreaseKey(i, ur[0], adjMatrix[ur[0], i])
            # start += 1
            # print(adjMatrix[5])
            # print(adjMatrix)
            for node in adjMatrix[ur[0]]['dist']:
                # print("Node: " + str(ur[0]) + " " +str(node))
                v = node[0]

                if Set[v] == False and node[1] < Key[v][1]:
                    Key[v][0] = ur[0]
                    Key[v][1] = node[1]
                    heap.decreaseKey(v, ur[0], node[1])
            start += 1
        # print("hello3")
        end = time.time()
        print("Thời gian chạy của Prim danh sách kề với binary heap: " + str(end - start1))
        return result, result2, result3

    # UPDATE Nhap mon tri tue nhan tao
    def prim2ThongDuong(self, adjMatrix):
        start1 = time.time()
        INF = 999999
        Set = np.ones(self.v + 1, dtype=int)
        Key = np.ones((self.v + 1, 2), dtype=int)
        # result = np.ones((self.v + 1, 2), dtype=int)
        result = [[0, 0] for i in range(self.v + 1)]
        result2 = np.zeros((self.v + 1, self.v + 1), dtype=int)
        result3 = dict()
        heap = MinHeap(100)
        # print(heap.heap)
        for i in range(0, self.v + 1):
            Set[i] = False
            Key[i][0] = -1
            Key[i][1] = INF
            heap.heap.append([i, i, 99999])
            heap.heapSize += 1
            heap.pos.append(i)
        start = 1
        Key[1][1] = 1
        heap.decreaseKey(1, 1, 0)
        while start <= self.v:
            ur = heap.extractMin()

            if True:
                if ur[0] == -1 or ur[1] == -1 or ur[2] == -1:
                    pass
                else:

                    if not ur[0] in result3:
                        result3[ur[0]] = dict()
                        result3[ur[0]]['dist'] = list()
                    result3[ur[0]]['dist'].append(ur[1])
                    result3[ur[1]]['dist'].append(ur[0])
                    result3[ur[0]]['g'] = self.INF
                    result3[ur[1]]['g'] = self.INF
                    result3[ur[0]]['f'] = self.INF
                    result3[ur[1]]['f'] = self.INF
                    result3[ur[0]]['h'] = ur[0]
                    result3[ur[1]]['h'] = ur[1]

                    result2[ur[0]][ur[1]] = 1
                    result2[ur[1]][ur[0]] = 1
                    # display_sulf.blit()
                    # print(ur)

                result[ur[0]][0] = ur[1]
                result[ur[0]][1] = ur[2]

            Set[ur[0]] = True

            for node in adjMatrix[ur[0]]['dist']:
                # print("Node: " + str(ur[0]) + " " +str(node))
                v = node[0]

                if Set[v] == False and node[1] < Key[v][1]:
                    Key[v][0] = ur[0]
                    Key[v][1] = node[1]
                    heap.decreaseKey(v, ur[0], node[1])
            start += 1
        # print("hello3")
        end = time.time()
        print("Thời gian chạy của Prim Thông Đường danh sách kề với binary heap: " + str(end - start1))
        return result, result2, result3

    ########################################################

    check = 1
    # Xác định xem có vẽ đường hay không
    status = 0

    def draw(self, display_surf, dich_surf, duongdi_surf):

        if self.status == 1 and self.check == 1:
            # self.path = self.bfs()
            self.path = self.ASaoAlgorithm()
            self.check = 0
            print(self.viTri)
            print("Check:" + str(self.check))
        count = 0
        bx = 0
        by = 0
        # print(self.dich)
        # print(self.maze)
        # Hàm vẽ hình , vẽ theo chiều dài và chiều rộng nhập ở trên nhé

        pygame.draw.rect(display_surf, [255, 255, 255], (bx * 32 + 4 + margin_left, by * 32 + 4 + margin_top, 30, 30))
        for i in range(1, self.height + 1):
            for j in range(1, self.width + 1):
                # print(i-1)
                # biến c sinh ra là để vẽ vạch đích nếu vẽ cố định vạch đích thì xóa đi vì biến c dùng như sau
                # Tạm thời chưa nhớ tại sao mình lại code cái này, từ từ
                c = i - 1
                # print(c * self.width + j)
                # display_surf.blit(image_surf, (bx * 32 + 4 + margin_left, by * 32 + 4 + margin_top))
                pygame.draw.rect(display_surf, [255, 255, 255], (bx * 32 + 4 + margin_left,
                                                                 by * 32 + 4 + margin_top, 30, 30))
                if c * self.width + j == self.dich:
                    display_surf.blit(dich_surf, (bx * 32 + 4 + 1 + margin_left, by * 32 + 4 + 1 + margin_top))
                    # pygame.draw.rect(display_surf, [255, 0, 0], (bx * 32 + 4 + 1 + margin_left,
                    #                                                  by * 32 + 4 + 1 + margin_top, 28, 28))

                # Giải thích phần tiếp theo k lại quên
                #
                #
                #
                #
                #
                # cái này chỉ đơn giản là convert từ giá trị 2 chiều về 1 chiều mà thôi
                # để làm gì ??? để biết đc rằng cái vòng lặp này đang vẽ đến đỉnh nào trong đồ thị
                x = (i - 1) * self.width + j
                # print(x)
                # Tại sao chúng ta k lấy 1
                # Vì x tại 1 thì self.maze[1] như đã code k có giá trị vì mày đã code đẩy cả cạnh 1 1 vào trong edge list sinh ra từ thằng prim
                # Nên ở đây xét bắt đầu từ 2
                if x != 1:
                    # print(x - self.maze[x][0])
                    #  Vế if này là gì ?? giải thích như sau
                    #
                    # mày sẽ có thằng đỉnh hiện tại là x và thằng nối với nó là giá trị nằm trong maze[x][0] ok
                    # rồi sẽ lấy 2 thằng trừ cho nhau mục đích nằm ở cái hiệu
                    # nếu cái hiệu ra là -width tức là bằng âm chiều rộng , ví dụ nhé;
                    # với 9 đỉnh và width = 3 và height = 3
                    # thì tại x = 3 mà trừ cho maze[x][0] bằng -3 thì ta có maze[x][0] = 6
                    #
                    # mà nếu nó bằng 6 thì nhìn nhé
                    #
                    # 1 2 3
                    #     |
                    # 4 5 6
                    #
                    # 7 8 9
                    # tức là tương đương 1 đường nối từ 3-6
                    # Tương tự với x - self.maze[x][0] = width tức là mày đã tìm được đường nối giữa 6 và 3 tương tự nhưng lần này là
                    # thằng 6 nối về thằng 3 chứ k phải thằng 3 nối lên thằng 6 nữa ok
                    # Trường hợp bằng 1 và -1 tức là nó nối với thằng đằng trước và thằng đằng sau ok
                    # Sau khi xác định đc trường hợp thì ta sẽ chèn các đường trắng vào các khe theo các trường hợp xác định, ở đây là 4 trường hợp
                    #
                    if x - self.maze[x][0] == -self.width:
                        # print("OKOK")
                        # pass
                        pygame.draw.rect(display_surf, [255, 255, 255], (bx * 32 + 4 + margin_left,
                                                                         by * 32 + 4 + 30 + margin_top, 30, 2))
                        # display_surf.blit(pygame.image.load("HorizonLine.png").convert(),
                        #                   (bx * 32 + 4 + margin_left, by * 32 + 4 + 30 + margin_top))
                    elif x - self.maze[x][0] == -1:
                        # pass
                        pygame.draw.rect(display_surf, [255, 255, 255], (bx * 32 + 4 + 30 + margin_left,
                                                                         by * 32 + 4 + margin_top, 2, 30))
                        # display_surf.blit(pygame.image.load("VerticalLine.png").convert(),
                        #                   (bx * 32 + 4 + 30 + margin_left, by * 32 + 4 + margin_top))
                    elif x - self.maze[x][0] == 1:
                        # pass
                        pygame.draw.rect(display_surf, [255, 255, 255], (bx * 32 + 2 + margin_left,
                                                                         by * 32 + 4 + margin_top, 2, 30))
                        # display_surf.blit(pygame.image.load("VerticalLine.png").convert(),
                        #                   (bx * 32 + 2 + margin_left, by * 32 + 4 + margin_top))
                    else:
                        # pass
                        pygame.draw.rect(display_surf, [255, 255, 255], (bx * 32 + 4 + margin_left,
                                                                         by * 32 + 2 + margin_top, 30, 2))
                        # display_surf.blit(pygame.image.load("HorizonLine.png").convert(),
                        #                   (bx * 32 + 4 + margin_left, by * 32 + 2 + margin_top))
                if self.status == 1:
                    # print(self.path)
                    try:
                        # print(count)
                        # print("Đầu vào: " + str(self.path))
                        # print("Đây nhé:" + str(x) + " " + str(self.path[count]) + str(len(self.path)))
                        if x == self.path[count]:
                            # print(self.path)181, 230, 29
                            pygame.draw.rect(display_surf, [181, 230, 29], (bx * 32 + 4 + 1 + margin_left,
                                                                            by * 32 + 4 + 1 + margin_top, 28, 28))
                            # display_surf.blit(duongdi_surf,
                            # (bx * 32 + 4 + 1 + margin_left, by * 32 + 4 + 1 + margin_top))
                            if count < len(self.path):
                                count += 1
                            else:
                                count = 0
                    except:
                        pass
                bx = bx + 1
            bx = 0
            by = by + 1
            a = []


class GiaoDien:
    def __init__(self):
        self._display_surf = None
        self.status = 0
        self.currentTextFieldString = []

    def text_objects(self, text, font):
        textSurface = font.render(text, True, [0, 0, 0])
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h, ic, ac, event):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        # print(type(event))
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self._display_surf, ac, (x, y, w, h))
            if click[0] == 1 and event == "start":
                self._running = False
                theApp = App()
                theApp.on_execute()
            elif click[0] == 1 and event == "quit":
                self._running = False
                exit(0)
            elif click[0] == 1 and event == "win":
                theApp = App()
                # theApp.on_execute()
            elif click[0] == 1 and event == "back":
                MazeAndPlayer.status = 0
                startForm = StartForm()
                startForm.on_execute()

            elif click[0] == 1 and event == "findpath":
                print(MazeAndPlayer.status)
                print(MazeAndPlayer.check)
                MazeAndPlayer.status = 1
                MazeAndPlayer.check = 1
        else:
            pygame.draw.rect(self._display_surf, ic, (x, y, w, h))

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self._display_surf.blit(textSurf, textRect)

    def label(self, msg, x, y, w, h, Mau):
        if Mau == 1:
            a = random.randint(0, 255)
            b = random.randint(0, 255)
            c = random.randint(0, 255)
        else:
            a = Mau[0]
            b = Mau[1]
            c = Mau[2]

        pygame.draw.rect(self._display_surf, [a, b, c], (x, y, w, h))

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self._display_surf.blit(textSurf, textRect)

    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            else:
                pass

        # pygame.draw.rect(self._display_surf, [a, b, c], (x, y, w, h))


class App(GiaoDien):
    # windowWidth = 1300
    # windowHeight = 700
    player = 0

    def __init__(self):
        super().__init__()
        self._running = True
        self.playerImage = None
        self.DichDenImage = None
        self.DuongDiImage = None
        self.realtime = None
        self.maze = MazeAndPlayer()
        self.Time = time.time()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(KICH_THUOC_KHUNG_HINH)
        # self._display_surf = pygame.display.set_mode((1300,700))
        pygame.display.set_caption('GAME ME CUNG :)))))))))))))')
        self._running = True
        self.playerImage = pygame.image.load("image/player.png").convert()
        self.DichDenImage = pygame.image.load("image/icons8-jake-48.png").convert()
        self.DuongDiImage = pygame.image.load("image/green.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_render(self):
        background_image = pygame.image.load("image/Webp.net-resizeimage.jpg").convert()
        self._display_surf.blit(background_image, [0, 0])
        # self._display_surf.blit(self.Jake,[1300,0])
        self.maze.draw(self._display_surf, self.DichDenImage, self.DuongDiImage)
        self._display_surf.blit(self.playerImage, (self.maze.x, self.maze.y))
        # Hàm time này đang tìm hiểu nó cho ra 1 cái số 1590 gì gì đó ấy
        # Nhưng sẽ sử dụng như sau ta có a = time.time() lấy cái số đó
        # sau đó lấy time.time() - a, vì time.time() sau mỗi lần gọi nó sẽ tăng thời gian lên 1 giây theo thực tế
        # Ví dụ time.time() ra 1 , 5 giây sau ra 5
        self.realtime = time.time() - self.Time
        self.button("BACK", 1150, 50, 150, 50, [0, 255, 255], [255, 0, 255], "back")
        # self.maze.findPath()
        self.button("FIND PATH", 750, 50, 150, 50, [0, 255, 255], [255, 0, 255], "findpath")
        self.label("Time: " + str(int(self.realtime)), 900, 50, 200, 50, [255, 255, 255])
        # self.button("FIND PATH", 950, 200, 250, 100, [0, 255, 255], [255, 0, 255], "findpath")
        pygame.display.flip()

    def on_execute(self):
        if not self.on_init():
            self._running = True
        count = 0
        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            # m = pygame.key.
            # print(keys)
            if keys[K_RIGHT] and count == 0:
                self.maze.moveRight(display=self._display_surf)
                count = 1

            if keys[K_LEFT] and count == 0:
                self.maze.moveLeft(display=self._display_surf)
                count = 1

            if keys[K_UP] and count == 0:
                self.maze.moveUp(display=self._display_surf)
                count = 1

            if keys[K_DOWN] and count == 0:
                self.maze.moveDown(display=self._display_surf)
                count = 1

            if not keys[K_UP] and not keys[K_RIGHT] and not keys[K_LEFT] and not keys[K_DOWN]:
                # print("sdfsdf")
                count = 0

            self.on_render()

            if self._display_surf.get_at((self.maze.x - 2, self.maze.y)) == (0, 0, 0, 255):
                # print("OKOOK")
                # print(self._display_surf.get_at((self.maze.x - 2, self.maze.y)))
                self._running = False
                theApp = WinForm(str(self.realtime))
                theApp.on_execute()
            # else: print(self._display_surf.get_at((self.maze.x - 2, self.maze.y)))
            if keys[K_ESCAPE]:
                self._running = False

        # on_cleanup()


class WinForm(GiaoDien):
    def __init__(self, realtime):
        super().__init__()
        self._display_surf = None

        self.realtime = realtime

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(KICH_THUOC_KHUNG_HINH)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_render(self):
        background_image = pygame.image.load("image/Webp.net-resizeimage.jpg").convert()
        self._display_surf.blit(background_image, [0, 0])
        self.button("BACK", 1150, 50, 150, 50, [0, 255, 255], [255, 0, 255], "back")
        self.button("CONTINUE", 550, 200, 200, 50, [0, 255, 255], [255, 0, 255], "start")
        self.label("Time:" + str(np.float32(self.realtime)), 550, 300, 200, 50, [255, 255, 255])
        self.label("WIN!!!", 550, 400, 200, 50, 1)
        pygame.display.flip()

    def on_execute(self):

        if not self.on_init():
            self._running = True

        while self._running:
            self.on_render()
            # for
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self._running = False

        # on_cleanup()


class StartForm(GiaoDien):
    def __init__(self):
        super().__init__()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(KICH_THUOC_KHUNG_HINH)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        background_image = pygame.image.load("image/Webp.net-resizeimage.jpg").convert()
        self._display_surf.blit(background_image, [0, 0])
        pygame.font.init()
        self.button("START!!!", 150, 100, 200, 100, [0, 255, 255], [255, 0, 255], "start")
        self.button("QUIT", 150, 250, 200, 100, [0, 255, 255], [255, 0, 255], "quit")

        pygame.display.flip()

    def on_execute(self):

        if not self.on_init():
            self._running = True

        while self._running:
            self.on_loop()
            self.on_render()
            # for
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self._running = False

        # on_cleanup()


theApp = StartForm()
theApp.on_execute()
