# Created 3-27-25
# C950 Performance Assessment
# Christopher Marshall, Student ID: 0001292385
# main.py

from Package import Package
from Truck import Truck
from datetime import datetime

#Print status has to be able to list all of the information for each pacakge that is searched
def print_status(package_manager, time, trucks, package_id=None):
    print(f"\nStatus at {time.strftime('%I:%M %p')}")
    packages = package_manager.get_all_packages() if package_id == "all" else [package_manager.lookup(int(package_id))] if package_id else []

    if not packages or packages == [None]:
        print ("Invalid Package ID")
        return

    for package in packages:
        package_id = package["id"]
        status = package["status"]
        delivery_time = package["delivery_time"]
        address = package["address"]
        deadline = package["deadline"]
        city = package["city"]
        zip_code = package["zip"]
        weight = int(package["weight"])


        truck = next((t for t in trucks if package_id in t.packages or (package_id not in t.packages and status == "delivered")), None)
        departure_time = truck.departure_time if truck else None

        status_text = ""
        if delivery_time and delivery_time <= time:
            status_text = f"delivered at {delivery_time.strftime('%I:%M %p')}"
        elif departure_time and time >= departure_time and (not delivery_time or time < delivery_time):
            status_text = "en route"
        else:
            status_text = "At hub"

        print(f"Package {package_id}: {status_text}  Address: {address}  City: {city}  Zip: {zip_code}  Weight(kg): {weight}")
        print(f"  Delivery time: {delivery_time.strftime('%I:%M %p')}  Deadline: {deadline}")

    # Here the milage for all trucks is calculated and displayed each time a status is requested
    total_miles = sum(truck.total_distance for truck in trucks)
    print(f"Total mileage: {total_miles:.2f} miles")

def main():

    package_manager = Package()# An instance of Package within Main to handle all Package lookups and statuses.

    # Here the trucks are initialzed and manually loaded to comply with the constraints of the program
    truck1 = Truck(1, datetime.strptime("8:00 AM", "%I:%M %p"))
    truck2 = Truck(2, datetime.strptime("8:00 AM", "%I:%M %p"))
    truck3 = Truck(3, None)

    for pid in [1,6, 13, 14, 15, 16, 20, 25, 29, 30, 31, 34, 37, 40]:
        truck1.add_package(pid)

    for pid in [2, 3, 4, 5, 7, 8, 10, 11, 12, 17, 18, 19, 21, 36, 38]:
        truck2.add_package(pid)
    # These are the packages left over. Truck 3 may not leave until either 1 or 2 has returned
    remaining = [9, 22, 23, 24, 26, 27, 28, 32, 33, 35, 39]

    truck1.deliver_packages(package_manager)
    truck2.deliver_packages(package_manager)
    truck3.departure_time = truck1.current_time
    truck3.current_time = truck3.departure_time
    for pid in remaining:
        truck3.add_package(pid)

    truck3.deliver_packages(package_manager)

    trucks = [truck1, truck2, truck3]

    while True:# This code is the entirety of the user interface, asking first for a package ID and then a time
        package_id = input("Welcome to WGUPS! Please enter a package ID (1-40) for the package you are trying to lookup or enter 'all' for all packages (or 'exit' to quit): ").lower()
        if package_id == "exit":
            break
        if package_id != "all" and not (package_id.isdigit() and 1 <= int(package_id) <= 40):
            print("Please enter a valid package ID (1-40) or else enter 'all'.")
            continue
        time_input = input("Enter a time to see the status of the package(e.g., '9:00 AM'): ")
        try:
            check_time = datetime.strptime(time_input, "%I:%M %p")
        except ValueError:
            print("Not a valid time format. Please use 'H:MM AM/PM'.")
            continue

        print_status(package_manager, check_time, trucks, package_id)

if __name__ == "__main__":
    main()




