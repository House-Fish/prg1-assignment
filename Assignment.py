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
    for option, description in enumerate(MENU_DESCRIPTIONS):
        menu += f"[{option}]\t{description} \n"
    return menu 

def get_option():
    while True:
        option = input("Enter your option: ")
        if is_valid_option(option):
            return int(option)

def is_valid_option(option):
    min_option, max_option = 0, len(MENU_DESCRIPTIONS)-1
    if not(option.isdigit()):
        print("Invalid option, should be a number.")
        return False
    elif not(min_option <= int(option) <= max_option):
        print(f"Invalid option, should be between {min_option} and {max_option} inclusive.")
        return False
    return True

def get_percentage():
    while True:
        percentage = input("Enter the percentage required: ")
        if is_valid_percentage(percentage):
            return float(percentage)

def is_valid_percentage(percentage):
    if not(percentage.isdigit()):
        print("Invalid percentage, should be a number.")
        return False
    elif not(0 <= float(percentage) <= 100):
        print(f"Invalid percentage, should be between 0 and 100 inclusive.")
        return False
    return True

def get_file_name():
    while True:
        file_name = input("Enter the file name: ")
        if not(is_valid_file(file_name)):
            print("Invalid file name, ensure that the file is in the correct directory.")
        else:
            return file_name

def generate_line(data_list, spacing_list, align_list):
    line = ""
    for data, spacing, align in zip(data_list, spacing_list, align_list):
        if align == "<":
            line += " " + data.ljust(spacing) 
        elif align == ">":
            line += data.rjust(spacing) + " "
    return line

def calculate_percentage(total_lots, lots_available):
    return round(lots_available/total_lots * 100, 1) 

def get_total_number(data_list):
    return len(data_list)

def is_valid_file(file_name):
    return isfile(file_name)

def main():
    carpark_information = {}
    carpark_availability = {}
    percentage_calculated = False
    
    carpark_information_file_name = "carpark-information.csv"

    if not(is_valid_file(carpark_information_file_name)):
        print(f"Invalid file name, {carpark_information_file_name} is not found.")
        return 
    carpark_information_file = open(carpark_information_file_name, "r")
    headers = carpark_information_file.readline().strip("\n").split(",")
    for row in carpark_information_file:
        items = row.strip("\n").split(",")
        carpark_details = {}
        carpark_number = items[0]
        for item, header in zip(items[1:], headers[1:]):
            carpark_details[header] = item
        carpark_information[carpark_number] = carpark_details

    menu = generate_menu()

    while True:
        print(menu)
        option = get_option()
        print(f"Option {option}: {MENU_DESCRIPTIONS[option]}")

        if option < 4:
            if option == 0: 
                break
            elif option == 1: 
                print(f"Total Number of carparks in '{carpark_information_file_name}': " 
                    + str(get_total_number(carpark_information)))
            elif option == 2:
                headers = ["Carpark Number", "Carpark Type", "Address"]
                spacing = [15, 20, 20]
                adjust = "<<<"
                total_number = 0

                print(generate_line(headers, spacing, adjust))
                for carpark, carpark_details in carpark_information.items():
                    if carpark_details["Carpark Type"] == "BASEMENT CAR PARK":
                        line_data = [carpark]
                        for header in headers[1:]:
                            line_data.append(carpark_details[header])
                        print(generate_line(line_data, spacing, adjust))
                        total_number += 1
                print(f"Total Number: {total_number}")
            else:
                carpark_availability_file_name = get_file_name()
                carpark_availability_file = open(carpark_availability_file_name, "r")
                timestamp = carpark_availability_file.readline().strip("\n")
                headers = carpark_availability_file.readline().strip("\n").split(",")
                for row in carpark_availability_file:
                    items = row.strip("\n").split(",")
                    carpark_details = {}
                    carpark_number = items[0]
                    for item, header in zip(items[1:], headers[1:]):
                        carpark_details[header] = item 
                    carpark_availability[carpark_number] = carpark_details
                print(timestamp[:-2])
        elif carpark_availability != {}:
            if option == 4:
                print(f"Total Number of Carparks in the File: {get_total_number(carpark_availability)}")
            elif option == 5: 
                total_number = 0
                for carpark_number, carpark_details in carpark_availability.items():
                    if int(carpark_details["Lots Available"]) == 0:
                        print(f"Carpark Number: {carpark_number}")
                        total_number += 1
                print(f"Total Number: {total_number}")
            else:
                total_number = 0

                if percentage_calculated == False:
                    for carpark_number, carpark_details in carpark_availability.items():
                        total_lots = int(carpark_details["Total Lots"])
                        lots_available = int(carpark_details["Lots Available"])
                        if lots_available == 0:
                            carpark_details["Percentage"] = "0.0"
                        else:
                            carpark_details["Percentage"] = str(calculate_percentage(total_lots, lots_available))
                    percentage_calculated = True

                if option == 6: 
                    spacing = [15, 12, 16, 12]
                    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage"]
                    adjust = "<>>>"

                    percentage = get_percentage()

                    print(generate_line(headers, spacing, adjust))
                    for carpark_number, carpark_details in carpark_availability.items():
                        if float(carpark_details["Percentage"]) > percentage:
                            line_data = [carpark_number]
                            for header in headers[1:]:
                                line_data.append(carpark_details[header])
                            print(generate_line(line_data, spacing, adjust))
                            total_number += 1
                    print(f"Total Number: {total_number}")
                else: 
                    spacing = [15, 12, 16, 12, 10]
                    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage", "Address"]
                    adjust = "<>>><"

                    if option == 7:
                        percentage = get_percentage()

                        print(generate_line(headers, spacing, adjust))
                        for carpark_number, carpark_details in carpark_availability.items():
                            if float(carpark_details["Percentage"]) > percentage:
                                line_data = [carpark_number]
                                for header in headers[1:4]:
                                    line_data.append(carpark_details[header])
                                line_data.append(carpark_information[carpark_number]["Address"])
                                print(generate_line(line_data, spacing, adjust))
                                total_number += 1
                        print(f"Total Number: {total_number}")
                    elif option == 8:
                        output = ""

                        location = input("Enter the location: ")

                        output += generate_line(headers, spacing, adjust) + "\n"
                        for carpark_number, carpark_details in carpark_availability.items():
                            if carpark_information.get(carpark_number) != None:
                                carpark_address = carpark_information[carpark_number]["Address"]
                                if location.lower() in carpark_address.lower():
                                    line_data = [carpark_number]
                                    for header in headers[1:4]:
                                        line_data.append(carpark_details[header])
                                    line_data.append(carpark_address)
                                    output += generate_line(line_data, spacing, adjust) + "\n"
                                    total_number += 1

                        if total_number > 0:
                            print(output)
                        else:
                            print(f"No carparks found in {location}")
                    elif option == 9:
                        most_lots = 0
                        for carpark_number, carpark_details in carpark_availability.items():
                            if carpark_information.get(carpark_number) != None:
                                total_lots = int(carpark_details["Total Lots"])
                                if total_lots > most_lots:
                                    most_lots_carpark_number = carpark_number
                                    most_lots = total_lots
                        print(f"{headers[0]}: {most_lots_carpark_number}")
                        for header in headers[1:4]:
                            print(f"{header}: {carpark_availability[most_lots_carpark_number][header]}")
                        print(f"{headers[4]}: {carpark_information[most_lots_carpark_number]["Address"]}")
                    else:
                        no_of_lines = 2
                        file_name = "carpark-availability-with-address.csv"
                        carpark_availability = dict(sorted(carpark_availability.items(), \
                                                           key=lambda carpark: int(carpark[1]["Total Lots"])))
                        if is_valid_file(file_name):
                            print(f"Invalid option, {file_name} already exits")
                            continue
                        carpark_availability_address_file = open(file_name, "w", newline='')
                        writer = csv.writer(carpark_availability_address_file)
                        carpark_availability_address_file.write(timestamp + "\n")
                        writer.writerow(headers)
                        for carpark_number, carpark_details in carpark_availability.items():
                            if carpark_information.get(carpark_number) != None:
                                line = [carpark_number]
                                line += carpark_details.values()
                                line.append(carpark_information[carpark_number]["Address"])
                                writer.writerow(line)
                                no_of_lines += 1
                        carpark_availability_address_file.close()
                        print(f"{no_of_lines} lines were written to '{file_name}'")

        else:
            print(f"Invalid option, select option 3 before selecting {option}")

if __name__ == "__main__":
    main()
      
                           
                           
                           
                           
                           
                           
                           
                           
                           

