import os
import time
from threading import Thread, Lock
from collections import deque


class TrafficLight:
    def __init__(self):
        print("Welcome to the traffic management system!")
        self.max_roads = None
        self.interval = None
        self.start_time = int(time.time())
        self.l = Lock()
        self.k = 1
        self.state = ''
        self.roads = deque()
        self.open_time = None
        self.open_counter = None

    def validate_input(self):
        self.l.acquire()
        error = "Error! Incorrect Input. "
        input_line = "Input the number of roads:"
        while not self.max_roads:
            roads = input(input_line)
            if roads.isdigit() and int(roads) > 0:
                self.max_roads = int(roads)
                break
            print(error, end='')
            input_line = "Try Again:"
        input_line = "Input the interval:"
        while not self.interval:
            interval = input(input_line)
            if interval.isdigit() and int(interval) > 0:
                self.interval = int(interval)
                break
            print(error, end='')
            input_line = "Try Again:"
        self.start_time = int(time.time())
        self.l.release()

    @staticmethod
    def validate_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Menu:\n1. Add road\n2. Delete road\n3. Open system\n0. Quit")
        menu_choice = input()
        if menu_choice.isdigit():
            menu_choice = int(menu_choice)
            if menu_choice > 3:
                menu_choice = None
        else:
            menu_choice = None
        return menu_choice

    def add_road(self):
        a = input("Input road name:")
        if len(self.roads) < self.max_roads:
            if not len(self.roads):
                self.open_time = int(time.time())
                self.roads.append([a, 'open', self.interval])
                self.open_counter = self.interval
            else:
                self.roads.append([a, 'closed', None])
                self.shift_seconds_new()
            print(f"Road {a} added!")
        else:
            print("queue is full")

    def delete_road(self):
        if len(self.roads) > 0:
            a = self.roads.popleft()
            print(f"Road {a[0]} deleted!")
            if a[1] == 'open':
                self.shift_seconds(0)
        else:
            print("queue is empty")

    def run(self):
        self.validate_input()
        while True:
            self.l.acquire()
            self.state = ''
            i = self.validate_menu()
            if i is None:
                print("Incorrect option")
            elif i == 0:
                print("Bye!")
                self.k = 0
                break
            elif i == 1:
                self.add_road()
            elif i == 2:
                self.delete_road()
            else:
                print("System opened!")
                self.state = 'System'
            self.l.release()
            input()

    def shift_seconds(self, seconds):
        if len(self.roads):
            self.open_counter -= seconds  # how many seconds will open road be open
            if not self.open_counter:  # need to change which road is open
                self.open_counter = self.interval
                found = False
                for i, road in enumerate(self.roads):
                    if road[1] == 'open':
                        found = True
                        road[1] = 'closed'
                        road[2] = self.interval * (len(self.roads) - 1) + seconds
                        if i + 1 < len(self.roads):
                            self.roads[i + 1][1] = 'open'
                            self.roads[i + 1][2] = self.interval + seconds
                            if i + 2 < len(self.roads):
                                self.roads[i + 2][2] = self.interval + seconds
                            else:
                                self.roads[0][2] = self.interval + seconds
                        else:
                            self.roads[0][1] = 'open'
                            self.roads[0][2] = self.interval + seconds
                            if len(self.roads) > 1:
                                self.roads[1][2] = self.interval + seconds
                        break
                if not found:
                    self.roads[0][1] = 'open'
                    self.roads[0][2] = self.interval + seconds
            if seconds:
                for road in self.roads:
                    road[2] -= seconds

    def shift_seconds_new(self):  # new road was just added need to recalculate open/closed intervals
        for i, road in enumerate(self.roads):
            if road[1] == 'open':
                if i != len(self.roads) - 2:  # open road is not right before the newly added one
                    self.roads[-1][2] = (len(self.roads) - i - 2) * self.interval + road[2]  # calculate closed interval for the new road
                else:
                    self.roads[-1][2] = road[2]  # penultimate one is open and new road will be closed for same amount of secs
                for j in range(i):
                    self.roads[j][2] += self.interval  # all the roads before the open one will get an extra "closed" interval due to new road
                break

    def print_state(self):
        printed = False
        while self.k:
            if self.state == 'System':
                self.l.acquire()
                time_passed = int(time.time()) - self.start_time
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"! {time_passed}s. have passed since system startup !")
                print(f"! Number of roads: {self.max_roads} !")
                print(f"! Interval: {self.interval} !\n")
                for road in self.roads:
                    color = "\u001B[32m" if road[1] == 'open' else "\u001B[31m"
                    print(f'road "{road[0]}" will be {color}{road[1]} for {road[2]}s.\u001B[0m')
                printed = True
                print('\n! Press "Enter" to open menu !')
                self.l.release()
            time.sleep(1)
            if printed:
                self.shift_seconds(1)


if __name__ == '__main__':
    t = TrafficLight()
    t1 = Thread(target=TrafficLight.print_state, args=(t,))
    t1.setName("QueueThread")
    t1.start()
    t.run()
    t1.join()
