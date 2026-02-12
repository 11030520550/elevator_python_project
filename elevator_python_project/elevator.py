import threading
import time
from threading import Thread

"""
Elevator simulation:

The code simulates an elevator system in a building/office
in which there is one elevator that picks up users
and takes passengers up and down.

With the option of course to expand to multiple elevators with a management department to monitor all elevators.
The elevator actually starts from floor 0 as a start
and picks up users in a THREE-way manner. A user enters the elevator and meanwhile user 2 orders the elevator and the elevator will pick him up as well.
Normal usage behavior - simulation:
-User 2 enters the elevator - his destination is floor 7
-The elevator starts to go up
-The elevator stops on floor 2 User 2 enters his destination is floor 4
-The elevator continues to floor 4, stops
-User 2 exits the elevator
-If there are no additional orders, the elevator continues to floor 7 without further stops.

It is possible that a user will be waiting on floor 7 who wants to go down to floor 3
The elevator will go down, pick up users on the way (or not) and repeat.
"""

class User:
    def __init__(self, name, destination_floor, start_floor):
        self.name = name
        self.destination_floor = destination_floor
        self.start_floor = start_floor
        self.in_elevator = False



class Elevator(threading.Thread):
    def __init__(self, num_floors):
        super().__init__()
        self.num_floors = num_floors
        self.destination = set()
        self.waiting_passengers = []
        self.current_floor = 0
        self.passengers = []
        self.direction = 1 # 1=up, -1=down

        self.running = True


    def add_user(self, user):
        self.waiting_passengers.append(user)
        self.destination.add(user.start_floor)


    def run(self):
        while self.running:
            if not self.destination:
                time.sleep(2)
                continue

            if self.direction == 1:
                next_floors = sorted([f for f in self.destination if f >= self.current_floor])
                if not next_floors:
                    self.direction = -1
                    continue
            else:
                next_floors = sorted([f for f in self.destination if f <= self.current_floor], reverse=True)
                if not next_floors:
                    self.direction = 1
                    continue
            next_floor = next_floors[0]

            while self.current_floor != next_floor:
                self.current_floor += 1 if self.direction == 1 else -1
                print(f"elevator in motion {'↑' if self.direction == 1 else '↓'} - floor: {self.current_floor} [🔴]")
                time.sleep(1)

            print(f"מעלית עצרה בקומה {self.current_floor} [🟢]")
            self.handle_floor()
            time.sleep(1)

    def handle_floor(self):
        for user in self.waiting_passengers[:]:
            if user.start_floor == self.current_floor:
                print(f"{user.name} entering thr elevator, destination: {user.destination_floor}")
                self.passengers.append(user)
                self.waiting_passengers.remove(user)
                self.destination.add(user.destination_floor)

        for passenger in self.passengers[:]:
            if passenger.destination_floor == self.current_floor:
                print(f"{passenger.name} get out of the elevator")
                self.passengers.remove(passenger)

        if self.current_floor in self.destination:
            self.destination.remove(self.current_floor)


    def show_users(self):
        for user in self.passengers:
            print(user.name, user.destination_floor, user.current_floor)


def main():

    elevator = Elevator(num_floors=10)
    elevator.start()

    user_1 = User("user_1", start_floor=0, destination_floor=7)
    user_2 = User("user2", start_floor=3, destination_floor=9)
    user_3 = User("user_3", start_floor=2, destination_floor=1)

    elevator.add_user(user_1)
    elevator.add_user(user_2)
    elevator.add_user(user_3)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("stopping the elevator")
        elevator.running = False
        elevator.join()




if __name__ == "__main__":
    main()


