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

def generate_line(data_list, spacing_list, align_list):
    line = ""
    for data, spacing, align in zip(data_list, spacing_list, align_list):
        if align == "<":
            line += data.ljust(spacing)
        elif align == ">":
            line += " " + data.rjust(spacing) + " "
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

def get_file_name():
    while True:
        file_name = input("Enter the file name: ")
        if not(is_valid_file(file_name)):
            print("Invalid file name, ensure that the file is in the correct directory.")
        else:
            return file_name

def get_spacing(headers):
    return [header_spacings[header] for header in headers]

def calculate_percentage(total_lots, lots_available):
    return round(lots_available/total_lots * 100, 1) 

def get_total_number(data_list):
    return len(data_list)

def is_valid_file(file_name):
    return isfile(file_name)

def main():

    #Define
    global carpark_information, carpark_availability, header_spacings
    carpark_information = {}
    carpark_availability = {}
    header_spacings = {}
    percentage_calculated = False
    
    cpi_file_name = "carpark-information.csv"

    #Ensure that the 'carpark-information.csv' file exists
    if not(is_valid_file(cpi_file_name)):
        print(f"Invalid file name, {file_name} is not found.")
        return 

    #Open, Read and Store the 'carpark-information.csv' file into the carpark_information dict 
    with open(cpi_file_name, "r") as carpark_information_file: 
        headers = carpark_information_file.readline().strip("\n").split(",")
        header_spacings = {header: len(header) for header in headers}
        for line in carpark_information_file:
            line = line.strip("\n").split(",")
            carpark_details = {}
            carpark_number = line[0]
            if len(carpark_number) > header_spacings[headers[0]]:
                header_spacings[header[0]] = len(carpark_number)
            for detail, header in zip(line[1:], headers[1:]):
                carpark_details[header] = detail 
                if len(detail) > header_spacings[header]:
                    header_spacings[header] = len(detail)
            carpark_information[carpark_number] = carpark_details

    #Generate the menu
    menu = generate_menu()

    while True:
        #Display the menu
        print(menu)

        #Input the option selected by the user
        option = get_option()

        #Display the option description
        print(f"Option {option}: {MENU_DESCRIPTIONS[option]}")

        if option == 0: 
            """
            End Program
            """
            print("See you again, space cowbow!")
            break
        elif option == 1: 
            """
            Display the total number of carparks in 'carpark-information.csv'
            """
            print(f"Total Number of carparks in '{cpi_file_name}': {str(get_total_number(carpark_information))}")
        elif option == 2:
            """
            Display the 'Carpark Number', 'Carpark Type' and 'Address' of basement carparks
            """

            #Define
            headers = ["Carpark Number", "Carpark Type", "Address"]
            spacing = get_spacing(headers)
            adjust = "<<<"
            total_number = 0

            #Display table header
            print(generate_line(headers, spacing, adjust))

            #Filter and Display table information
            for carpark, carpark_details in carpark_information.items():
                if carpark_details["Carpark Type"] == "BASEMENT CAR PARK":
                    line_data = [carpark]
                    for header in headers[1:]:
                        line_data.append(carpark_details[header])
                    print(generate_line(line_data, spacing, adjust))
                    total_number += 1
            
            #Display total number 
            print(f"Total Number: {total_number}")
        elif option == 3:
            """
            Input, Read, Store and Display timestamp of carpark-availability file
            """

            #Input file name
            cpa_file_name = get_file_name()

            #Read and Store carpark-availability and add Headers with their maximum length 
            with open(cpa_file_name, "r") as carpark_availability_file:
                timestamp = carpark_availability_file.readline().strip("\n")
                headers = carpark_availability_file.readline().strip("\n").split(",")
                header_spacings.update({header: len(header) for header in headers})
                for line in carpark_availability_file:
                    line = line.strip("\n").split(",")
                    carpark_details = {}
                    carpark_number = line[0]
                    if len(carpark_number) > header_spacings[headers[0]]:
                        header_spacings[header[0]] = len(carpark_number)
                    for detail, header in zip(line[1:], headers[1:]):
                        carpark_details[header] = detail 
                        if len(detail) > header_spacings[header]:
                            header_spacings[header] = len(detail)
                    carpark_availability[carpark_number] = carpark_details
            
            #Display timestamp
            print(timestamp[:-2])
        elif carpark_availability != {}:
            #Check if Option 3 has been selected before selecting Options > 3

            if option == 4:
                """
                Display the total number of carparks in carpark-availability file
                """
                print(f"Total Number of Carparks in the File: {get_total_number(carpark_availability)}")
            elif option == 5: 
                """
                Display the total number of carparks with 0 lots available
                """
                total_number = 0

                #Filter and Display carparks with 0 lots available
                for carpark_number, carpark_details in carpark_availability.items():
                    if int(carpark_details["Lots Available"]) == 0:
                        print(f"Carpark Number: {carpark_number}")
                        total_number += 1
                
                #Display the total number of carparks
                print(f"Total Number: {total_number}")
            elif option < 10:
                #Calculate the percentage of lots available for Option 6, 7, 8 & 9
                total_number = 0

                if percentage_calculated == False:
                    header_spacings.update({"Percentage": 10})
                    for carpark_number, carpark_details in carpark_availability.items():
                        total_lots = int(carpark_details["Total Lots"])
                        lots_available = int(carpark_details["Lots Available"])
                        if lots_available == 0:
                            carpark_details["Percentage"] = "0.0"
                        else:
                            percentage = str(calculate_percentage(total_lots, lots_available))
                            carpark_details["Percentage"] = percentage 
                    percentage_calculated = True

                if option == 6: 
                    """
                    Input the minimum availability percentage and Display information about the carparks 
                    that are above that value
                    """
                    #Define
                    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage"]
                    spacing = get_spacing(headers)
                    adjust = "<>>>"

                    #Input the percentage
                    percentage = get_percentage()

                    #Display the header
                    print(generate_line(headers, spacing, adjust))

                    #Filter and Display the carparks with percentages above the input percentage
                    for carpark_number, carpark_details in carpark_availability.items():
                        if float(carpark_details["Percentage"]) > percentage:
                            line_data = [carpark_number]
                            for header in headers[1:]:
                                line_data.append(carpark_details[header])
                            print(generate_line(line_data, spacing, adjust))
                            total_number += 1
                    
                    #Display the total number of carparks
                    print(f"Total Number: {total_number}")
                else:
                    #Headers 
                    headers = ["Carpark Number", "Total Lots", "Lots Available", "Percentage", "Address"]
                    spacing = get_spacing(headers)
                    adjust = "<>>><"

                    if option == 7:
                        """
                        Input the minimum availability percentage and Display information (including Address)
                        about the carparks that are above that value 
                        """
                        #Input the percentage
                        percentage = get_percentage()

                        #Display the header
                        print(generate_line(headers, spacing, adjust))

                        #Filter and display the carparks and their addresses
                        for carpark_number, carpark_details in carpark_availability.items():
                            if float(carpark_details["Percentage"]) > percentage:
                                line_data = [carpark_number]
                                for header in headers[1:4]:
                                    line_data.append(carpark_details[header])
                                line_data.append(carpark_information[carpark_number]["Address"])
                                print(generate_line(line_data, spacing, adjust))
                                total_number += 1
                        
                        #Display the total number of carparks
                        print(f"Total Number: {total_number}")
                    elif option == 8:
                        """
                        Input the location and Display information about the carparks at that location if they
                        are available
                        """
                        #Input the location
                        location = input("Enter the location: ")

                        #Generate the header
                        output = generate_line(headers, spacing, adjust) + "\n"

                        #Filter and Generate the carparks information
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
                        
                        #Display the carpark information if there are any carparks at that location
                        if total_number > 0:
                            print(output)
                        else:
                            print(f"No carparks found in {location}")
                    elif option == 9:
                        """
                        Display information about the carpark with the highest total number of lots
                        """
                        #Define
                        most_lots = 0

                        #Find the carpark number with the most number of lots
                        for carpark_number, carpark_details in carpark_availability.items():
                            if carpark_information.get(carpark_number) != None:
                                total_lots = int(carpark_details["Total Lots"])
                                if total_lots > most_lots:
                                    most_lots_carpark_number = carpark_number
                                    most_lots = total_lots
                        
                        #Display information about the carpark
                        print(f"{headers[0]}: {most_lots_carpark_number}")
                        for header in headers[1:4]:
                            print(f"{header}: {carpark_availability[most_lots_carpark_number][header]}")
                        print(f"{headers[4]}: {carpark_information[most_lots_carpark_number]["Address"]}")
            elif option == 10:
                """
                Output a 'carpark-availability-with-address.csv' and Display the total number of lines written to it
                """
                #Define
                no_of_lines = 2
                headers = ["Carpark Number", "Total Lots", "Lots Available", "Address"]
                file_name = "carpark-availability-with-address.csv"

                #Sort out the carpark availability information by the total number of lots in ascending order
                carpark_availability = dict(sorted(carpark_availability.items(), \
                                                    key=lambda carpark: int(carpark[1]["Total Lots"])))
                
                #Check if the 'carpark-availability-with-address.csv' file exists
                if is_valid_file(file_name):
                    print(f"Invalid option, {file_name} already exits")
                    continue

                #Open and store the carpark availability information in the file
                with open(file_name, "w", newline='') as carpark_availability_address_file:
                    writer = csv.writer(carpark_availability_address_file)
                    carpark_availability_address_file.write(timestamp + "\n")
                    writer.writerow(headers)
                    for carpark_number, carpark_details in carpark_availability.items():
                        if carpark_information.get(carpark_number) != None:
                            line = [carpark_number] 
                            for header in headers[1:3]:
                                line.append(carpark_details[header])
                            line.append(carpark_information[carpark_number]["Address"])
                            writer.writerow(line)
                            no_of_lines += 1
                
                #Display the total number of lines written to the file
                print(f"{no_of_lines} lines were written to '{file_name}'")

        else:
            #Error telling the user to select option 3 before selecting options > 3
            print(f"Invalid option, select option 3 before selecting {option}")

if __name__ == "__main__":
    main()