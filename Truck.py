#File to hold the Truck package

import csv
from datetime import datetime,timedelta

hub = "4001 South 700 East" #holds the Hub address as a separate variable

class Truck:
    def __init__(self,truck_id, departure_time):
        self.truck_id = truck_id
        self.packages = []
        self.distances = {}
        self.departure_time = departure_time
        self.total_distance = 0
        self.speed = 18
        self.current_time = departure_time
        self.current_address = hub
        self.load_distances()

    def load_distances(self):   #Called when the Truck is initialized
        with open("distances.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            column_address = [addr.strip() for addr in headers[1:]] #Remove spaces from the addresses
            for row in reader:# The code reads in the addresses from the first row and column and uses the pairs as tuple-keys to lookup the distance
                row_address = row[0].strip()
                distances_list = row[1:]
                for col_address, distance in zip(column_address, distances_list):
                    self.distances[(row_address, col_address)] = float(distance.strip())


    def add_package(self, package_id):
        if len(self.packages) < 16:
            self.packages.append(package_id)
        else:
            raise ValueError(f"Truck {self.truck_id} is full" )

    def deliver_packages(self, package_manager): # The Nearest-Neighbor algorithm
        while self.packages:
            min_distance = float("inf")
            next_package = None
            next_address = None

            for package_id in self.packages:# Loop through the packages and use the addresses as tuple keys to find the distances
                package = package_manager.lookup(package_id)
                address = package["address"]
                if package_id == 9 and self.current_time < datetime.strptime("10:20 AM", "%I:%M %p"):
                    address = "300 State St"
                distance = self.distances[(self.current_address),(address)]
                if distance < min_distance: # Updates the next address if the package it is looking up is closer than the current nearest package
                    min_distance = distance
                    next_package = package_id
                    next_address = address

            self.total_distance += min_distance # Adds all the minimum distances to find the total distance
            self.current_address = next_address # updates with the nearest address to the current one
            time_traveled = timedelta(hours=min_distance / self.speed) # Calulates the time to the next address
            self.current_time += time_traveled # Totals the drive time to each location

            #Updates Package #9 based on the time
            if next_package == 9 and self.current_time >= datetime.strptime("10:20 AM", "%I:%M %p"):
                package_manager.lookup(next_package)["address"] = "410 S State St"
            package_manager.update_status(next_package, "delivered", self.current_time)
            self.packages.remove(next_package) # Remove packges already delivered
        # Return to the Hub to tally the last time/distance
        return_distance = self.distances[(self.current_address,hub)]
        self.total_distance += return_distance
        self.current_time += timedelta(hours=return_distance / self.speed)
        self.current_address = hub






