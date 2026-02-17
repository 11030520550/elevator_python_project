import threading
import time
from threading import Thread

"""
Elevator Simulation Project

This program simulates an elevator system in a multi-floor building.
Users request the elevator from different floors and select destination floors.
The elevator moves according to pending requests, picking up and dropping off
passengers along the way.

The system is implemented using Object-Oriented Programming (OOP),
where users and the elevator are represented as classes.
The elevator runs on a separate thread to simulate continuous movement
independently from the main program.

"""


#Class representing a user of the elevator
class User:
    def __init__(self, name, destination_floor, start_floor):
        self.name = name  #User name
        self.destination_floor = destination_floor  #Target floor
        self.start_floor = start_floor  #Starting floor
        self.in_elevator = False  #Indicates if the user is inside the elevator


#Elevator class that runs as a separate thread
class Elevator(threading.Thread):
    def __init__(self, num_floors):
        super().__init__()
        self.num_floors = num_floors  #Total number of floors in the building
        self.destination = set()  #Set of floors where the elevator needs to stop
        self.waiting_passengers = []  #Users waiting for the elevator
        self.current_floor = 0  #Current floor of the elevator
        self.passengers = []  #Users currently inside the elevator
        self.direction = 1  #Movement direction: 1 = up, -1 = down
        self.running = True  #Controls elevator operation


    #Adds a new user to the system
    def add_user(self, user):
        self.waiting_passengers.append(user)  #Add user to waiting list
        self.destination.add(user.start_floor)  #Add starting floor as a stop


    #Main loop executed by the thread
    def run(self):
        while self.running:

            #If there are no destinations,wait
            if not self.destination:
                time.sleep(2)
                continue

            #Choose next destination based on current direction
            if self.direction == 1:  #Moving up
                next_floors = sorted(
                    [f for f in self.destination if f >= self.current_floor]
                )
                if not next_floors:
                    self.direction = -1  #Change direction
                    continue
            else:  #Moving down
                next_floors = sorted(
                    [f for f in self.destination if f <= self.current_floor],
                    reverse=True
                )
                if not next_floors:
                    self.direction = 1  #Change direction
                    continue

            next_floor = next_floors[0]  #Closest floor in current direction

            #Move floor by floor until reaching destination
            while self.current_floor != next_floor:
                self.current_floor += 1 if self.direction == 1 else -1
                print(f"Elevator moving {'↑' if self.direction == 1 else '↓'} - floor: {self.current_floor} [🔴]")
                time.sleep(1)

            #Elevator reached the floor
            print(f"Elevator stopped at floor {self.current_floor} [🟢]")
            self.handle_floor()
            time.sleep(1)


    #Handles passengers entering and exiting at current floor
    def handle_floor(self):

        #Let waiting passengers enter the elevator
        for user in self.waiting_passengers[:]:
            if user.start_floor == self.current_floor:
                print(f"{user.name} entered the elevator, destination: {user.destination_floor}")
                self.passengers.append(user)
                self.waiting_passengers.remove(user)
                self.destination.add(user.destination_floor)

        #Let passengers exit if this is their destination
        for passenger in self.passengers[:]:
            if passenger.destination_floor == self.current_floor:
                print(f"{passenger.name} exited the elevator")
                self.passengers.remove(passenger)

        #Remove current floor from destinations list
        if self.current_floor in self.destination:
            self.destination.remove(self.current_floor)


    #Prints current passengers inside the elevator
    def show_users(self):
        for user in self.passengers:
            print(user.name, user.destination_floor, user.current_floor)


#Main function that starts the simulation
def main():

    elevator = Elevator(num_floors=10)  # Create elevator with 10 floors
    elevator.start()  # Start elevator thread

    # Create users
    user_1 = User("Robert", start_floor=0, destination_floor=7)
    user_2 = User("Julia", start_floor=3, destination_floor=9)
    user_3 = User("Pier", start_floor=2, destination_floor=1)


    #Add users to the system
    elevator.add_user(user_1)
    elevator.add_user(user_2)
    elevator.add_user(user_3)


    #Run until manual interruption
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping elevator...")
        elevator.running = False
        elevator.join()


#Program entry point
if __name__ == "__main__":
    main()
