#!/usr/bin/env python3
from os.path import isfile
import csv

MENU_DESCRIPTIONS = ["Exit",
                     "Display Total Number of Carparks in 'carpark-information.csv'",
                     "Display All Basement Carparks in 'carpark-information.csv'",
                     "Read Carpark Availability Data File",
                     "Print Total Number of Carparks in the File Read in [3]",
                     "Display Carparks Without Available Lots",
                     "Display Carparks With At Least x% Available Lots",
                     "Display Addresses of Carparks With At Least x% Available Lots",
                     "Display all information about a Carpark at a Address",
                     "Display all information about the Carpark with the most Lots",
                     "Write the Carpark Availability and Address to a new File"]

def generate_menu():
    menu = "\nMENU\n====\n"
    for option, description in enumerate(MENU_DESCRIPTIONS[1:], start=1):
        menu += f"[{option}]\t{description} \n"
    menu += f"[0]\t{MENU_DESCRIPTIONS[0]}"
    return menu 

def generate_line(values, spacings, alignments):
    line = ""
    for value, spacing, alignment in zip(values, spacings, alignments):
        if alignment == "<":
            line += " " + value.ljust(spacing) + " "
        elif alignment == ">":
            line += " " + value.rjust(spacing) + " "
    return line

def get_option():
    while True:
        option = input("Enter your option: ")
        if option.isdigit() and 0 <= int(option) <= len(MENU_DESCRIPTIONS) - 1:
            return int(option)
        print("Invalid option, please enter a valid number between 0 and", len(MENU_DESCRIPTIONS) - 1)

def get_percentage():
    while True:
        percentage = input("Enter the percentage required: ")
        if percentage.isdigit() and 0 <= float(percentage) <= 100:
            return float(percentage)
        print("Invalid percentage, please enter a valid number between 0 and 100")

def calculate_percentage(total_lots, lots_available):
    return round(lots_available/total_lots * 100, 1) 

def get_total_number(data_list):
    return len(data_list)

def is_existing_file(file_name):
    return isfile(file_name)

def append_percentages(carpark_availability):
    for carpark in carpark_availability:
        total_lots = int(carpark["Total Lots"])
        lots_available = int(carpark["Lots Available"])
        if lots_available == 0:
            carpark["Percentage"] = "0.0"
        else:
            carpark["Percentage"] = str(calculate_percentage(total_lots, lots_available)) 
    return carpark_availability

def append_addresses(carpark_availability, carpark_information):
    for carpark_a in carpark_availability:
        carpark_a["Address"] = ""
        for carpark_i in carpark_information:
            if carpark_i["Carpark Number"] == carpark_a["Carpark Number"]:
                carpark_a["Address"] = carpark_i["Address"]
    return carpark_availability

def display_total_number_of_carpark_information(cpi_file_name, carpark_information):
    print(f"Total Number of carparks in '{cpi_file_name}': {get_total_number(carpark_information)}")

def display_basement_carparks(carpark_information):
    headers = ["Carpark Number", "Carpark Type", "Address"]
    spacings = [14, 17, 7]
    alignments = "<<<"
    total_number = 0

    print(generate_line(headers, spacings, alignments))

    for carpark in carpark_information:
        if carpark["Carpark Type"] == "BASEMENT CAR PARK":
            values = [carpark[header] for header in headers]
            print(generate_line(values, spacings, alignments))
            total_number += 1
    
    print(f"Total Number: {total_number}")

def get_carpark_availability_display_timestamp(carpark_availability):
    cpa_file_name = input("Enter file name: ") 
    
    try: 
        carpark_availability_file = open(cpa_file_name, "r")
    except FileNotFoundError:
        print(f"Invalid file name, {cpa_file_name} is not found\n"
              "Make sure that it is within the same directory.")
        return get_carpark_availability_display_timestamp(carpark_availability)
    else:
        timestamp = carpark_availability_file.readline().strip("\n")
        headers = carpark_availability_file.readline().strip("\n").split(",")
        for line in carpark_availability_file:
            line = line.strip("\n").split(",")
            carpark = dict(zip(headers, line))
            carpark_availability.append(carpark)
        carpark_availability_file.close()
        print(timestamp)
        return carpark_availability, timestamp

def display_total_number_of_carpark_availability(carpark_availability):
    print(f"Total Number of Carparks in the File: {get_total_number(carpark_availability)}")

def display_carpark_without_lots(carpark_availability):
    total_number = 0
    for carpark in carpark_availability:
        if int(carpark["Lots Available"]) == 0:
            print(f"Carpark Number: {carpark["Carpark Number"]}")
            total_number += 1
    print(f"Total Number: {total_number}")

def display_carpark_with_x_available_lots(carpark_availability, headers, spacing, alignments):
    total_number = 0
    percentage = get_percentage()
    print(generate_line(headers, spacing, alignments))
    for carpark in carpark_availability:
        if float(carpark["Percentage"]) > percentage:
            line_data = [carpark[header] for header in headers]
            print(generate_line(line_data, spacing, alignments))
            total_number += 1
    
    print(f"Total Number: {total_number}")

def display_carpark_at_address(carpark_availability, headers, spacing, alignments):
    total_number = 0
    location = input("Enter the location: ")
    output = generate_line(headers, spacing, alignments) + "\n"
    for carpark in carpark_availability:
        if location.lower() in carpark["Address"].lower():
            line_data = []
            for header in headers:
                line_data.append(carpark[header])
            output += generate_line(line_data, spacing, alignments) + "\n"
            total_number += 1
    if total_number > 0:
        print(output)
        print(f"Total Number: {total_number}")
    else:
        print(f"No carparks found in {location}")

def display_carpark_with_most_lots(carpark_availability, headers):
    most_lots = 0
    most_lots_index = 0
    for index, carpark in enumerate(carpark_availability):
        total_lots = int(carpark["Total Lots"])
        if total_lots > most_lots:
            most_lots_index = index 
            most_lots = total_lots
    for header in headers:
        print(f"{header}: {carpark_availability[most_lots_index][header]}")

def write_carpark_availability_address(carpark_availability, timestamp):
    no_of_lines = 2
    headers = ["Carpark Number", "Total Lots", "Lots Available", "Address"]
    cpaa_file_name = "carpark-availability-with-address.csv"

    carpark_availability_sorted = list(sorted(carpark_availability, \
                                              key=lambda carpark: int(carpark["Total Lots"])))

    if is_existing_file(cpaa_file_name):
        print(f"Invalid option, '{cpaa_file_name}' already exists in the directory.")
        return

    with open(cpaa_file_name, "w", newline='') as carpark_availability_address_file:
        writer = csv.writer(carpark_availability_address_file)
        carpark_availability_address_file.write(timestamp + "\n")
        writer.writerow(headers)
        for carpark in carpark_availability_sorted:
            line = [carpark[header] for header in headers]
            writer.writerow(line)
            no_of_lines += 1

    print(f"{no_of_lines} lines were written to '{cpaa_file_name}'")

def main():
    carpark_information = []
    carpark_availability = [] 
    percentage_appended = False
    address_appended = False
    cpi_file_name = "carpark-information.csv"

    try:
        carpark_information_file = open(cpi_file_name, "r")
    except FileNotFoundError:
        print(f"Invalid file name, {cpi_file_name} is not found.")
    else: 
        headers = carpark_information_file.readline().strip("\n").split(",")
        for values in carpark_information_file:
            values = values.strip("\n").split(",")
            carpark = dict(zip(headers, values))
            carpark_information.append(carpark)
    finally: 
        carpark_information_file.close()

    menu = generate_menu()

    while True:
        print(menu)
        option = get_option()
        print(f"Option {option}: {MENU_DESCRIPTIONS[option]}")
        if option == 0: 
            break
        elif option == 1: 
            display_total_number_of_carpark_information(cpi_file_name, carpark_information)
        elif option == 2:
            display_basement_carparks(carpark_information)
        elif option == 3:
            carpark_availability, timestamp = get_carpark_availability_display_timestamp(carpark_availability)
        elif carpark_availability != []: 
            if not(address_appended):
                carpark_availability = append_addresses(carpark_availability, carpark_information)
                address_appended = True 
            if option == 4:
                display_total_number_of_carpark_availability(carpark_availability) 
            elif option == 5: 
                display_carpark_without_lots(carpark_availability)
            elif option < 10: 
                if not(percentage_appended):
                    carpark_availability = append_percentages(carpark_availability)
                    percentage_appended = True
                headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage", "Address"]
                spacing = [14, 10, 14, 10, 7]
                alignments = "<>>><"
                if option == 6:
                    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage"]
                    spacing = [14, 10, 14, 10]
                    alignments = "<>>>"
                    display_carpark_with_x_available_lots(carpark_availability, headers, spacing, alignments)
                elif option == 7:
                    display_carpark_with_x_available_lots(carpark_availability, headers, spacing, alignments)
                elif option == 8:
                    display_carpark_at_address(carpark_availability, headers, spacing, alignments)
                elif option == 9:
                    display_carpark_with_most_lots(carpark_availability, headers)
            elif option == 10:
                write_carpark_availability_address(carpark_availability, timestamp)
        else:
            print(f"Invalid option, select option 3 before selecting {option}")

if __name__ == "__main__":
    main()
    print("See you again, space cowboy!")