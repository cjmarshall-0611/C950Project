# File to hold the Package class

import csv
from datetime import datetime,timedelta


class Package:
    def __init__(self):
        self.package_table = [[]for _ in range(40)] # Table to hold all 40 packages
        self.load_packages()

    def package_hash(self,package_id):
        return package_id % 40
    # Adds the data from the WGUPS Package file into the program and then adds that package into the hash table
    def insert(self, package_id, address, deadline, city, zip_code, weight, status, notes=""):
        index = self.package_hash(package_id)
        package_data = {
            "id": package_id,
            "address": address,
            "deadline": deadline,
            "city": city,
            "zip": zip_code,
            "weight": weight,
            "status": status,
            "delivery_time": None,  # Will be set when delivered
            "notes": notes

        }
        self.package_table[index].append(package_data)

    def update_status(self, package_id, status, delivery_time=None):
        package = self.lookup(package_id)
        if package:
            package["status"] = status
            if delivery_time:
                package["delivery_time"] = delivery_time

    # Part of the requirement. Returns a package based on its ID.
    def lookup(self, package_id):
        index = self.package_hash(package_id)
        for package in self.package_table[index]:
            if package["id"] == package_id:
                return package
        return None

    def load_packages(self): # Called when Package is initialized
        with open("packages.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                package_id = int(row["id"])
                address = row["address"].strip()
                city = row["city"]
                zip_code = row["zip"]
                deadline = row["deadline"] if row["deadline"]  != "EOD" else "5:00 PM"
                weight = int(row["weight"])
                notes = row["notes"] if "notes" in row else ""
                self.insert(package_id, address, deadline, city, zip_code, weight, "At Hub", notes)
    # Returns every package
    def get_all_packages(self):
        all_packages = []
        for bucket in self.package_table:
            all_packages.extend(bucket)
        return all_packages



