import math

from pyastar2d import astar_path


class Astar:
    def __init__(self, director):
        self.director = director
        self.cell = None

    def find_path(self, source, target):
        start = (int(source[1]) // 20, int(source[0] // 20))  # 初始坐标由像素地图坐标转为游戏坐标
        goal = (int(target[1] // 20), int(target[0] // 20))
        flag = True
        if 0 <= goal[0] < self.cell.shape[0] and 0 <= goal[1] < self.cell.shape[1]:
            if self.cell[goal[0], goal[1]] > 1:
                flag = False
                goal = self.nearest_valid_coord(goal)
        if goal[0] < 0 or goal[1] > self.director.window_w or goal[1] < 0 or goal[1] > self.director.window_h:
            return []
        try:
            path = astar_path(self.cell, start, goal, allow_diagonal=True)
        except ValueError:
            return []
        path_list = self.adjust_path(path)  # 去除多余点, 同时将游戏坐标转为地图像素坐标
        if flag and len(path_list) > 0:
            path_list[-1] = (int(target[0]), int(target[1]))  # 将最后一个坐标，设为target_pc
        return path_list

    def nearest_valid_coord(self, point):
        """
        获取离障碍点最近的可达点，广度搜索该点的四周
        :param point:
        :return:
        """
        _stack = [point]
        been = {}
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        while _stack:
            _point = _stack.pop(0)
            if self.cell[_point[0]][_point[1]] == 1:
                return _point
            been[_point] = 1
            for n in neighbors:
                temp = _point[0]+n[0], _point[1]+n[1]
                if temp not in been:
                    if 0 <= temp[0] < self.cell.shape[0] and 0 <= temp[1] < self.cell.shape[1]:
                        _stack.append(temp)
                        been[temp] = 1

    def adjust_path(self, path):
        """
        如果两个点之间没有阻碍，则抛弃他们之间点
        :param path:
        :return:
        """
        left = 0
        right = len(path) - 1
        _path = []
        while left < right:
            x1 = path[left][0]
            y1 = path[left][1]
            x2 = path[right][0]
            y2 = path[right][1]
            dis = math.dist(path[left], path[right])
            if dis > 8 or self.is_obstacle_in_between(x1, y1, x2, y2):  # 距离太远或者有阻碍，则right - 1，检验前一个点
                right -= 1
                # continue
            else:  # 没有阻碍，则可直接到这个点
                _path.append((path[right][1] * 20 + 10, path[right][0] * 20 + 10))
                left = right
                right = len(path) - 1

        return _path

    def is_obstacle_in_between(self, x1, y1, x2, y2):
        """
        查看两点之间是否有阻碍，有则返回True
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        f = self.generate_function(x1, y1, x2, y2)
        anti_f = self.generate_function(y1, x1, y2, x2)
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            if self.cell[x, int(f(x)) + 1] > 1:
                return True
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            if self.cell[int(anti_f(y)), y] > 1:
                return True
        return False

    @staticmethod
    def generate_function(x1, y1, x2, y2):
        def f(x):
            return y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)
        return f
