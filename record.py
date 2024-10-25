import time
import pyautogui
import keyboard
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


class Record:
    def __init__(self):
        self.points = []
        self.start_point = None
        self.finished = False

    def set_start_point(self, point):
        self.start_point = point
        print(point)

    def record(self):
        x, y = pyautogui.position()
        point = Point(x, y)
        if self.start_point is None:
            self.set_start_point(point)
        print(point - self.start_point)
        self.points.append(point - self.start_point)

    def finish(self):
        self.finished = True
        with open("data.csv", 'w') as f:
            for point in self.points:
                f.write(f"{point.x},{point.y}\n")


def f1():
    global x1, y1, flag1
    flag1 = True
    x1, y1 = pyautogui.position()


def f2():
    global x2, y2, flag2
    flag2 = True
    x2, y2 = pyautogui.position()


rec = Record()
keyboard.add_hotkey('\\', rec.record)
keyboard.add_hotkey('q', rec.finish)

print("Press hotkey <\\> to record your path.")
print("Start your first at middle of your tank as the start point.")
print("Press hotkey <q> to stop...\n")
while not rec.finished:
    time.sleep(1)