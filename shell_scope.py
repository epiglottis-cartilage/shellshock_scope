import os
import time
import pyautogui
import keyboard
import math
from win32 import win32gui


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scale):
        return Point(self.x * scale, self.y * scale)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


def get_window_handle(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        raise Exception(f"Window '{title}' not found")
    return hwnd


def get_window_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    print(rect)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    return width, height


class State:
    def __init__(self):
        self.start = None
        self.though = None
        self.target = None
        self.solution = []
        self.flag = False
        self.hwnd = get_window_handle('ShellShock Live')

    def set_start_point(self):
        x, y = pyautogui.position()
        self.start = Point(x, y)
        print(f"start point: {self.start}")

    def set_target_point(self):
        x, y = pyautogui.position()
        self.target = self.start - Point(x, y)
        self.target.x = abs(self.target.x)
        print(f"target point: {self.target}")
        self.flag = True

    def set_though_point(self):
        x, y = pyautogui.position()
        self.though = self.start - Point(x, y)
        self.though.x = abs(self.though.x)
        print(f"through point: {self.though}")

    def find_solution(self):
        window_width, window_height = get_window_size(self.hwnd)
        screen_width, screen_height = pyautogui.size()
        # 2880 is resolution of **my** screen
        scale = 2880 / window_width

        solution = []
        for angle in range(90, 0, -1):
            best = math.inf
            ans = None
            for speed in range(1, 100):
                res_target = self.distance_to(angle, speed, self.target*scale)
                dis = abs(res_target)
                if self.though is not None:
                    res_though = self.distance_to(
                        angle, speed, self.though*scale)
                    dis += abs(res_though)
                else:
                    res_though = 0

                if dis <= best:
                    best: float = dis
                    ans = [speed, angle, dis, (res_though, res_target)]
            solution.append(ans)
        self.solution = solution

    def distance_to(self, angle, speed, target):
        angle = math.radians(angle)

        def y(x):
            return 1.0175*x*math.tan(angle) - 1.34175*((x/speed/math.cos(angle))**2)

        def dis(x):
            return Point(x, y(x)).distance(target)

        # return min(dis(x) for x in range(int(target.x*0.8),target.x))

        left = target.x*0.9
        right = target.x*1.05
        while right - left > 1:
            mid1 = left + (right - left) / 3
            mid2 = right - (right - left) / 3
            if dis(mid1) < dis(mid2):
                right = mid2
            else:
                left = mid1
        x = (left + right) / 2
        return dis(x) * (1 if y(x) > target.y else -1)


def main():
    state = State()

    screenWidth, screenHeight = pyautogui.size()
    px, py = pyautogui.position()

    keyboard.add_hotkey('[', state.set_start_point)
    keyboard.add_hotkey(']', state.set_target_point)
    keyboard.add_hotkey('\\', state.set_though_point)

    while True:
        if state.flag:
            os.system("cls")
            state.find_solution()
            dis_top = [dis for (speed, angle, dis, mis) in state.solution]
            dis_top.sort(key=lambda x: abs(x))
            dis_top = dis_top[:30]
            for (speed, angle, dis, mis) in state.solution:
                if dis in dis_top and abs(mis[0]) < 20:
                    print(f"{speed},{angle} \t {
                          int(mis[0]):+} {int(mis[1]):+}")
            state.flag = False
            state.though = None
        else:
            time.sleep(0.05)


if __name__ == '__main__':
    main()
