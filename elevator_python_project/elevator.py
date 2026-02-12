import threading
import time
from threading import Thread


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
                print(f"מעלית בתנועה {'↑' if self.direction == 1 else '↓'} - קומה: {self.current_floor} [🔴]")
                time.sleep(1)

            print(f"מעלית עצרה בקומה {self.current_floor} [🟢]")
            self.handle_floor()
            time.sleep(1)

    def handle_floor(self):
        for user in self.waiting_passengers[:]:
            if user.start_floor == self.current_floor:
                print(f"{user.name} נכנס למעלית, יעדו: {user.destination_floor}")
                self.passengers.append(user)
                self.waiting_passengers.remove(user)
                self.destination.add(user.destination_floor)

        for passenger in self.passengers[:]:
            if passenger.destination_floor == self.current_floor:
                print(f"{passenger.name} יצא מהמעלית")
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
        print("עצירת המעלית...")
        elevator.running = False
        elevator.join()




if __name__ == "__main__":
    main()
