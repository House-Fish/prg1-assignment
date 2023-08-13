#!/usr/bin/env python3
#Lee Jia Yu - S10256965 - CSF01 - P06

import os
import csv
import requests
from requests.exceptions import HTTPError
import shelve 

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
                     "Write the Carpark Availability and Address to a new File",
                     "Read Full Carpark Availability Data File",
                     "Display all information about Favourite Carparks",
                     "Add Favourite Carpark",
                     "Remove Favourite Carpark",
                     "Display all information about Carparks nearest to the Address"]

USER_FOLDER_FILE_PATH = os.path.relpath("user")
USER_DATA_FILE_PATH = os.path.relpath("user/data")

API_URL = "https://api.data.gov.sg/v1/transport/carpark-availability"

def generate_menu(menu_description):
    """ 
    Return the formatted main menu with option numbers.

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
    Returns the spaced and aligned values.

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
    #Ask the user to 'Enter' to continue the next iteration of the main loop.
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
    return os.path.isfile(file_name)

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
            carpark_information (list[dict]): The list of carparks from file_name
    """
    carpark_information = []
    try:
        with open(file_name, "r") as carpark_information_file:
            headers = carpark_information_file.readline().strip("\n").split(",")
            for line in carpark_information_file:
                sentence = ""
                values = []
                within_quotes = False
                for char in line.strip("\n"):
                    if char == '"':
                        within_quotes = not within_quotes
                    elif char == ',' and not within_quotes:
                        values.append(sentence.strip())
                        sentence = ""
                    else:
                        sentence += char
                if sentence:
                    values.append(sentence.strip())
                carpark = dict(zip(headers, values))
                carpark_information.append(carpark)
    except FileNotFoundError:
        print(f"Invalid file name, {file_name} is not found.")
    else:
        print(f"'{file_name}' was successfully read.")
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
                assert "Total Lots" in headers
                for line in carpark_availability_file:
                    line = line.strip("\n").split(",")
                    carpark = dict(zip(headers, line))
                    carpark_availability.append(carpark)
        except FileNotFoundError:
            print(f"Invalid file name, '{cpa_file_name}' is not found, make sure that it is within the same directory.")
        except AssertionError: 
            print(f"Invalid file name, '{cpa_file_name}' should contain the Total Lots at a carpark.")
        except Exception as err: 
            print(f"Error occurred: {err}")
        else:
            print(f"'{cpa_file_name}' was successfully read.")
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
    Option 5: Prints the carpark numbers with 0 lots available

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
    """
    Option 10: Writes the carpark_availability list with the addresses from carpark_information

    Parameters: 
        carpark_availability (list[dict]): The carpark availability list from the file
        timestamp (str): The timestamp from the carpark_availability file

    Returns: 
        None   
    """
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

def display_favourite_carparks(carpark_information, url, option, user_data):
    """
    Option 12: Displays information about the carparks that have been stored as Favourites

    Parameters: 
        carpark_information (list[dict]): The full carpark availability list
        url (str): The url of the API used to get the carpark's lot availability
        option (int): The option choosen by the user
        user_data (shelf object): A shelf object that stores the Favourited carparks
    
    Returns:
        None
    """
    headers = ["Carpark Number", "Carpark Type", "Type of Parking System", "Total Lots", "Lots Available", "Address"]
    spacing = [14, 17, 25, 10, 14, 7]
    align = "<<<<<<"

    favourite_carparks = user_data.get("Favourite Carparks") 
    if not favourite_carparks: 
        print("You have not saved any carparks to your favourite.\n"
                f"Add carparks to your favourite in option {option + 1}")
        return

    carpark_availability = get_carpark_availability(url)
    if not carpark_availability:
        return
   
    print(generate_line(headers, spacing, align))
    for favouite_carpark in favourite_carparks:
        for information_carpark in carpark_information: 
            carpark_number = information_carpark.get("Carpark Number")
            availability_carpark = carpark_availability.get(carpark_number)
            if carpark_number == favouite_carpark and availability_carpark: 
                line_data = [information_carpark.get(header, availability_carpark.get(header)) for header in headers]
                print(generate_line(line_data, spacing, align))

def get_carpark_availability(url):
    """
    Request the most recent carpark lots availability from the API and parse the results

    Parameters: 
        url (str): The URL of the API to the carpark lots availability endpoint 
    
    Returns: 
        parse_availability (dict{dict}): Dictionary of carpark numbers to their Total Lots and Lots Available
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}') 
    else:
        print("Success, Carpark Availability received.")
        return parse_availability(response)

def parse_availability(response):
    """
    Parse the response from the API call to return a list of carparks with their total lots and availability

    Parameters: 
        reponse (object): The response from a get request to an API 
    
    Returns:
        carpark_availability (dict{dict}): A dictionary of carpark numbers to a dictionary of their Total 
        Lots and Lots Available
    """
    items = response.json().get("items")[0]
    carpark_data = items.get("carpark_data")
    carpark_availability = {} 
    for carpark in carpark_data:
        carpark_number = carpark.get("carpark_number")
        carpark_info = carpark.get("carpark_info")[0]
        carpark_availability[carpark_number] = {"Total Lots": carpark_info.get("total_lots"),
                                                "Lots Available": carpark_info.get("lots_available")}
    return carpark_availability

def add_favourite_carpark(carpark_information, user_data):
    """
    Option 13: Add a carpark to the Favourites dictionary 

    Parameters: 
        carpark_information (list[dict]): The full carpark availability list
        user_data (shelf object): A shelf object that stores the Favourited carparks
    
    Returns: 
        user_data (shelf object): The shelf object that has a Favourited carpark added
    """
    favourite_carparks = user_data.get("Favourite Carparks", [])

    while True:
        is_valid_carpark = False
        msg = "Carpark does not exist"
        possible_carpark_number = input("Enter Carpark Number: ")
        for carpark in carpark_information:
            if possible_carpark_number == carpark.get("Carpark Number"):
                if possible_carpark_number not in favourite_carparks:
                    is_valid_carpark = True
                else:
                    msg = "Carpark is already added to Favourites"
                break
        if is_valid_carpark: 
            break
        print(f"Invalid Carpark, {msg}")
    
    favourite_carparks.append(possible_carpark_number)
    user_data["Favourite Carparks"] = favourite_carparks
    print(f"Carpark: {possible_carpark_number} has been saved to the file")
    return user_data
            
def remove_favourite_carpark(user_data, option):
    """
    Option 14: Remove a carpark from the Favourites dictionary 

    Parameters: 
        user_data (shelf object): A shelf object that stores the Favourited carparks
        option (int): The option that the user has choosen
    
    Returns: 
        user_data (shelf object): The shelf object that has a Favourited carpark removed
    """
    favourite_carparks = user_data.get("Favourite Carparks")

    if not favourite_carparks:
        print("You have not added any carparks to your favourite\n"
              f"Add carparks to your favourite in option {option - 1}")
        return

    while True:
        is_valid_carpark = False
        possible_carpark_number = input("Enter Carpark Number: ")
        for carpark_number in favourite_carparks:
            if possible_carpark_number == carpark_number:
                is_valid_carpark = True
        if is_valid_carpark: 
            break
        print("Invalid Carpark, Carpark does not exist within Favourites")

    favourite_carparks.remove(possible_carpark_number)
    user_data["Favourite Carparks"] = favourite_carparks
    print(f"Carpark: {possible_carpark_number} has been removed from the file")
    return user_data

def find_centre(nearby_carpark):
    """
    Calculate the centre of a dictionary of carparks coordinates

    Parameters: 
        nearby_carpark (dict{dict}): A dictionary containing the Carpark Number mapped to their X and Y coordinates

    Returns: 
        X_coordinate (float): The X coordinate of the centre
        Y_coordinate (float): The Y coordinate of the centre
    """
    X_sum = 0
    Y_sum = 0
    count = 0
    for coordinates in nearby_carpark.values():
        X_sum += coordinates.get("X")
        Y_sum += coordinates.get("Y")
        count += 1
    return X_sum/count, Y_sum/count

def distance_from_centre(nearby_carparks, X_centre, Y_centre, carpark_number):
    """
    Returns the distance between the centre and carpark

    Parameters: 
        nearby_carparks (dict{dict}): A dictionary containing the Carparks Numbers mapped to their X and Y coorindates
        X_centre (float): The X coordinate of the centre
        Y_centre (float): The Y coordinate of the centre
        carpark_number (str): The carpark number that is being calculated
    
    Returns: 
        distance_from_centre (float): The distance between the centre and the carpark
    """
    X = nearby_carparks[carpark_number].get("X")
    Y = nearby_carparks[carpark_number].get("Y")
    return calculate_distance_between_two_points(X_centre, Y_centre, X, Y)

def calculate_distance_between_two_points(X1, Y1, X2, Y2):
    """
    Returns the distance between any two points 

    Parameters: 
        X1 (float): The first X coordinate
        Y1 (float): The first Y coordinate
        X2 (float): The second X coordinate
        Y2 (float): The second Y coordinate

    Returns: 
        distance_between_two_points (float): The distance between two pairs of X, Y coordinates
    """
    return ((X2 - X1)**2 + (Y2 - Y1)**2)**0.5

def display_nearest_carparks(carpark_information, url):
    """
    Option 15: Display the list of carparks closest to the address given 

    Parameters: 
        carpark_information (list[dict]): The full list of carpark information
        url (str): The API url to the most recent carpark lots availability 

    Returns: 
        None  
    """
    headers = ["Carpark Number", "Carpark Type", "Type of Parking System", "Total Lots", "Lots Available", "Address"]
    spacing = [14, 29, 25, 10, 14, 7]
    align = "<<<<<<"
    nearby_carparks = {} 

    while True: 
        address = input("Enter the address: ")
        for carpark in carpark_information:
            if address.lower() in carpark.get("Address").lower():
                carpark_coordinate = {"X": float(carpark.get("X")),
                                    "Y": float(carpark.get("Y"))}
                nearby_carparks[carpark.get("Carpark Number")] = carpark_coordinate
        if len(nearby_carparks) != 0:
            break
        print("Invalid Address, no carparks are at this location.")

    X_centre, Y_centre = find_centre(nearby_carparks)

    sorted_nearby_carparks = sorted(nearby_carparks, 
                                    key=lambda carpark_number: distance_from_centre(nearby_carparks, X_centre, Y_centre, carpark_number))

    carpark_availability = get_carpark_availability(url)
    if not carpark_availability:
        return
   
    print(generate_line(headers, spacing, align))
    for nearby_carpark in sorted_nearby_carparks:
        for information_carpark in carpark_information: 
            carpark_number = information_carpark.get("Carpark Number")
            availability_carpark = carpark_availability.get(carpark_number)
            if carpark_number == nearby_carpark and availability_carpark: 
                line_data = [information_carpark.get(header, availability_carpark.get(header)) for header in headers]
                print(generate_line(line_data, spacing, align))

def main():
    carpark_information = []
    carpark_availability = [] 
    full_carpark_information = []
    timestamp = ""
    cpi_file_name = "carpark-information.csv"
    fcpi_file_name = "carpark-information-full.csv"

    carpark_information = get_carpark_information(cpi_file_name)
    menu = generate_menu(MENU_DESCRIPTIONS)

    if not os.path.exists(USER_FOLDER_FILE_PATH):
        os.mkdir(USER_FOLDER_FILE_PATH)
    
    with shelve.open(USER_DATA_FILE_PATH) as user_data:
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
            elif carpark_availability == [] and option < 11: 
                print(f"Invalid option, select option 3 before selecting {option}")
            elif option == 4:
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
            elif option == 11: 
                full_carpark_information = get_carpark_information(fcpi_file_name)
            elif full_carpark_information == []:
                print(f"Invalid option, selection option 11 before selecting {option}")
            elif option == 12: 
                display_favourite_carparks(full_carpark_information, API_URL, option, user_data)
            elif option == 13: 
                user_data = add_favourite_carpark(full_carpark_information, user_data)
            elif option == 14:
                user_data = remove_favourite_carpark(user_data, option)
            elif option == 15: 
                display_nearest_carparks(full_carpark_information, API_URL)
            continue_hold()

if __name__ == "__main__":
    main()
    print("See you again, space cowboy!")