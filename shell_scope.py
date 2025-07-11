import os
import time
import pyautogui
import keyboard
import math
from win32 import win32gui  # pip install pywin32

try:
    with open("scale.txt", "r") as f:
        SCALE = list(map(float, f.read().strip().split(",")))
except FileNotFoundError:
    print("scale.txt not found, maybe this is your first run?")
    print("Please read the README.md for instructions.")
    exit(1)


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
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def get_window_handle(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        raise RuntimeError(f"Window '{title}' not found")
    return hwnd


def get_window_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    print(rect)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    return width, height


class State:
    start: Point | None
    though: Point | None
    target: Point | None
    solution: list
    need_refresh: bool
    hwnd: int

    def __init__(self):
        self.start = None
        self.though = None
        self.target = None
        self.solution = []
        self.need_refresh = False
        self.hwnd = get_window_handle("ShellShock Live")

    def set_start_point(self):
        x, y = pyautogui.position()
        self.start = Point(x, y)
        print(f"start point: {self.start}")
        # self.need_refresh = self.target is not None

    def set_target_point(self):
        x, y = pyautogui.position()
        self.target = Point(x, y)
        print(f"target point: {self.target}")
        self.need_refresh = self.start is not None

    def set_though_point(self):
        x, y = pyautogui.position()
        self.though = Point(x, y)
        self.though.x = abs(self.though.x)
        print(f"through point: {self.though}")
        

    def find_solution(self):
        assert self.start is not None, "Start point must be set"
        assert self.target is not None, "Target point must be set"

        window_width, window_height = get_window_size(self.hwnd)
        screen_width, screen_height = pyautogui.size()
        # only tested on **my** screen
        scale = screen_width / window_width

        start = self.start
        target = start - self.target
        target.x = abs(target.x)

        if self.though is not None:
            though = start - self.though
            though.x = abs(though.x)
        else:
            though = None

        solution = []
        for angle in range(90, 0, -1):
            best = math.inf
            ans = None
            for speed in range(1, 100):
                res_target = self.distance_to(angle, speed, target * scale)
                dis = abs(res_target)
                if though is not None:
                    res_though = self.distance_to(angle, speed, though * scale)
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
            return (
                -SCALE[0] * ((x / speed / math.cos(angle)) ** 2)
                + SCALE[1] * x * math.tan(angle)
                + SCALE[2]
            )

        def dis(x):
            return Point(x, y(x)).distance(target)

        # return min(dis(x) for x in range(int(target.x*0.8),target.x))

        left = target.x * 0.9
        right = target.x * 1.05
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

    keyboard.add_hotkey("[", state.set_start_point)
    keyboard.add_hotkey("]", state.set_target_point)
    keyboard.add_hotkey("\\", state.set_though_point)

    while True:
        if state.need_refresh:
            os.system("cls")
            state.find_solution()
            dis_top = [dis for (speed, angle, dis, mis) in state.solution]
            dis_top.sort(key=lambda x: abs(x))
            dis_top = dis_top[:30]
            for speed, angle, dis, mis in state.solution:
                if dis in dis_top and abs(mis[0]) < 20:
                    print(f"{speed},{angle} \t {int(mis[0]):+} {int(mis[1]):+}")
            state.need_refresh = False
            state.though = None
        else:
            time.sleep(0.05)


if __name__ == "__main__":
    print("[ at your ass")
    print("] at your target")
    print("\\ at your though")
    main()
