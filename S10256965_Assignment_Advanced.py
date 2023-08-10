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

def generate_menu(menu_description):
    """ 
    Return the string formatted main menu.

        Parameters: 
            menu_description (list): A list of MENU_DESCRIPTIONS
        
        Returns:
            menu (str): MENU_DESCRIPTIONS with their option numbers
    """
    menu = "\nMENU\n====\n"
    for option, description in enumerate(menu_description[1:], start=1):
        menu += f"[{option}]\t{description} \n"
    menu += f"[0]\t{menu_description[0]}"
    return menu 

def generate_line(values, spacings, alignments):
    """
    Returns the spaced and aligned values in a string.

        Parameters: 
            values (list): A list of the values to be represented
            spacing (list): A list of the spacing of each value
            alignments (list): A list of the alignments of each value
        
        Returns: 
            line (str): The spaced and aligned values
    """
    line = ""
    for value, spacing, alignment in zip(values, spacings, alignments):
        if alignment == "<":
            line += " " + value.ljust(spacing) + " "
        elif alignment == ">":
            line += " " + value.rjust(spacing) + " "
    return line

def get_option(menu_description):
    """
    Returns the option choosen by user. 

        Parameters: 
            menu_description (list): A list of the MENU_DESCRIPTION
        
        Returns: 
            option (int): The option choosen by the user
    """
    while True:
        option = input("Enter your option: ")
        if option.isdigit() and 0 <= int(option) <= len(menu_description) - 1:
            return int(option)
        print("Invalid option, please enter a valid number between 0 and", len(menu_description) - 1)

def get_percentage():
    """
    Returns the percentage given by the user. 

        Paramters: 
            None
        
        Returns: 
            percentage (float): The percentage that the user has choosen
    """
    while True:
        percentage = input("Enter the percentage required: ")
        if percentage.isdigit() and 0 <= float(percentage) <= 100:
            return float(percentage)
        print("Invalid percentage, please enter a valid number between 0 and 100")

def continue_hold():
    #Ask the user to 'Enter' to continue the next round of the program.
    input("Enter to continue: ")

def calculate_percentage(total_lots, lots_available):
    """
    Returns the percentage of lots available. 

        Parameters: 
            total_lots (int): The total number of lots at a carpark
            lots_available (int): The total number of lots available at a carpark

        Returns: 
            percentage (float): The percentage rounded to 1d.p.
    """
    return round(lots_available/total_lots * 100, 1) 

def get_total_number(data_list):
    #Returns the length of a list
    return len(data_list)

def is_existing_file(file_name):
    #Checks if a file exists within the path
    return isfile(file_name)

def append_percentages(carpark_availability):
    """
    Returns the carpark_availability list with the percentages of available lots

        Parameters: 
            carpark_availability (list[dict]): The list of carparks from 'carpark-availability-vX.csv'
        
        Returns:
            carpark_availability (list[dict]): With the percentage of available lots
    """
    for carpark in carpark_availability:
        total_lots = int(carpark["Total Lots"])
        lots_available = int(carpark["Lots Available"])
        if lots_available == 0:
            carpark["Percentage"] = "0.0"
        else:
            carpark["Percentage"] = str(calculate_percentage(total_lots, lots_available)) 
    return carpark_availability

def append_addresses(carpark_availability, carpark_information):
    """
    Returns the carpark_availability list with their addresses from carpark_information.

        Parameters:
            carpark_availability (list[dict]): The list of carparks from 'carpark-availability-vX.csv'
            carpark_information (list[dict]): The list of carparks from 'carpark-information.csv'
        
        Returns:
            carpark_availability (list[dict]): With the addresses from carpark_information
    """
    for carpark_a in carpark_availability:
        carpark_a["Address"] = ""
        for carpark_i in carpark_information:
            if carpark_i["Carpark Number"] == carpark_a["Carpark Number"]:
                carpark_a["Address"] = carpark_i["Address"]
    return carpark_availability

def get_carpark_information(file_name):
    """
    Returns the carpark_information list from 'carpark-information.csv'

        Parameters: 
            file_name (str): The name of the carpark information file

        Returns: 
            carpark_information (list[dict]): The list of carparks from 'carpark-information.csv'
    """
    carpark_information = []
    try:
        with open(file_name, "r") as carpark_information_file:
            headers = carpark_information_file.readline().strip("\n").split(",")
            for values in carpark_information_file:
                values = values.strip("\n").split(",")
                address_index = len(headers) - 1 
                if values[address_index][0] == '"':
                    values[address_index] = ",".join(values[address_index:])
                carpark = dict(zip(headers, values))
                carpark_information.append(carpark)
    except FileNotFoundError:
        print(f"Invalid file name, {file_name} is not found.")
    else:
        return carpark_information

def display_total_number_of_carpark_information(file_name, carpark_information):
    """
    Option 1: Prints the total number of carparks in carpark_information

        Parameters:
            file_name (str): The name of the carpark information file 
            carpark_information (list[dict]): The list of carparks from the carpark information file

        Returns:
            None 
    """
    print(f"Total Number of carparks in '{file_name}': {get_total_number(carpark_information)}")

def display_basement_carparks(carpark_information):
    """
    Option 2: Prints information about the 'BASEMENT CAR PARK's

        Parameters: 
            carpark_information (list[dict]): The list of carparks from the carpark information file

        Returns: 
            None
    """
    total_number = 0
    headers = ["Carpark Number", "Carpark Type", "Address"]
    spacings = [14, 17, 7]
    alignments = "<<<"

    print(generate_line(headers, spacings, alignments))

    for carpark in carpark_information:
        if carpark["Carpark Type"] == "BASEMENT CAR PARK":
            values = [carpark[header] for header in headers]
            print(generate_line(values, spacings, alignments))
            total_number += 1
    
    print(f"Total Number: {total_number}")

def get_carpark_availability_display_timestamp():
    """
    Option 3: Prompts and returns the carpark-availability from the users input

    Parameters: 
        None

    Returns: 
        carpark_availablility (list[dict]): The carpark availability list from the file
        timestamp (str): The timestamp of when the carpark availability file was created
    """
    carpark_availability = []
    while True: 
        cpa_file_name = input("Enter file name: ") 
        try: 
            with open(cpa_file_name, "r") as carpark_availability_file:
                timestamp = carpark_availability_file.readline().strip("\n")
                headers = carpark_availability_file.readline().strip("\n").split(",")
                for line in carpark_availability_file:
                    line = line.strip("\n").split(",")
                    carpark = dict(zip(headers, line))
                    carpark_availability.append(carpark)
        except FileNotFoundError:
            print(f"Invalid file name, {cpa_file_name} is not found\n"
                  "Make sure that it is within the same directory.")
        else:
            print(timestamp)
            return carpark_availability, timestamp

def display_total_number_of_carpark_availability(carpark_availability):
    """
    Option 4: Prints the total number of carparks in the carpark_availability list

    Parameters: 
        carpark_availability (list[dict]): The carpark availability list from the file

    Returns: 
        None
    """
    print(f"Total Number of Carparks in the File: {get_total_number(carpark_availability)}")

def display_carpark_without_lots(carpark_availability):
    """
    Option 5: Prints information about the carparks with 0 lots available

    Parameters: 
        carpark_availability (list[dict]): The carpark availability list from the file

    Returns: 
        None
    """
    total_number = 0
    for carpark in carpark_availability:
        if int(carpark["Lots Available"]) == 0:
            print(f"Carpark Number: {carpark["Carpark Number"]}")
            total_number += 1
    print(f"Total Number: {total_number}")

def display_carpark_with_x_available_lots(carpark_availability, with_address = False):
    """
    Option 6 & 7: Prompts and prints information (w & w/o address) about the carparks that have 
    availability percentage over the users requirement. 

 
    Parameters: 
        carpark_availability (list[dict]): The carpark availability list from the file
        with_address (bool): Whether the address should be displayed

    Returns: 
        None
    """

    total_number = 0
    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage"] 
    spacing = [14, 10, 14, 10] 
    alignments = "<>>>"

    if with_address: 
        headers.append("Address") 
        spacing.append(7)
        alignments += "<"

    percentage = get_percentage()

    print(generate_line(headers, spacing, alignments))
    for carpark in carpark_availability:
        if float(carpark["Percentage"]) > percentage:
            line_data = [carpark[header] for header in headers]
            print(generate_line(line_data, spacing, alignments))
            total_number += 1
    
    print(f"Total Number: {total_number}")

def display_carpark_at_address(carpark_availability):
    """
    Option 8: Prompts and prints information about the carparks that are at the users given
    location. 
 
    Parameters: 
        carpark_availability (list[dict]): The carpark availability list from the file

    Returns: 
        None   
    """

    total_number = 0
    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage", "Address"]
    spacing = [14, 10, 14, 10, 7]
    alignments = "<>>><"

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

def display_carpark_with_most_lots(carpark_availability):
    """
    Option 9: Prints information about the carpark with the most total lots

        Parameters: 
            carpark_availability (list[dict]): The carpark availability list from the file

        Returns: 
            None   
    """

    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage", "Address"]
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
                                              key=lambda carpark: int(carpark["Lots Available"])))

    if is_existing_file(cpaa_file_name):
        print(f"Invalid option, '{cpaa_file_name}' already exists in the directory.")
        return

    with open(cpaa_file_name, "w", newline='') as carpark_availability_address_file:
        carpark_availability_address_file.write(timestamp + "\n")
        writer = csv.DictWriter(carpark_availability_address_file, \
                                fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        for carpark in carpark_availability_sorted:
            writer.writerow(carpark)
            no_of_lines += 1

    print(f"{no_of_lines} lines were written to '{cpaa_file_name}'")

def main():
    carpark_information = []
    carpark_availability = [] 
    cpi_file_name = "carpark-information.csv"

    carpark_information = get_carpark_information(cpi_file_name)
    menu = generate_menu(MENU_DESCRIPTIONS)

    while True:
        print(menu)
        option = get_option(MENU_DESCRIPTIONS)
        print(f"Option {option}: {MENU_DESCRIPTIONS[option]}")

        if option == 0: 
            break
        elif option == 1: 
            display_total_number_of_carpark_information(cpi_file_name, carpark_information)
        elif option == 2:
            display_basement_carparks(carpark_information)
        elif option == 3:
            carpark_availability, timestamp = get_carpark_availability_display_timestamp()
            carpark_availability = append_addresses(carpark_availability, carpark_information)
            carpark_availability = append_percentages(carpark_availability)
        elif carpark_availability != []: 
            if option == 4:
                display_total_number_of_carpark_availability(carpark_availability) 
            elif option == 5: 
                display_carpark_without_lots(carpark_availability)
            elif option == 6:
                display_carpark_with_x_available_lots(carpark_availability)
            elif option == 7:
                display_carpark_with_x_available_lots(carpark_availability, with_address=True)
            elif option == 8:
                display_carpark_at_address(carpark_availability)
            elif option == 9:
                display_carpark_with_most_lots(carpark_availability)
            elif option == 10:
                write_carpark_availability_address(carpark_availability, timestamp)
        else:
            print(f"Invalid option, select option 3 before selecting {option}")

        continue_hold()

if __name__ == "__main__":
    main()
    print("See you again, space cowboy!")