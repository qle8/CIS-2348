# Student Name: Quang Le
# Student ID: 1768324
# Class: CIS2348-14654
# Professor: Amaury Lendasse
import csv
import time
import copy

class InputList:

    ## InputList class has functions to import list of manufacturer, type, damage, price, and service date from .csv data files

    def manufacturer():
        with open('ManufacturerList.csv', 'r') as csvfile:
            manufacturer_reader = csv.reader(csvfile, delimiter=',')
            mnftr = {}
            for row in manufacturer_reader:
                mnftr[row[0]] = row[1]
            return mnftr

    def type():

        with open('ManufacturerList.csv', 'r') as csvfile:
            type_reader = csv.reader(csvfile, delimiter=',')
            tp = {}
            for row in type_reader:
                tp[row[0]] = row[2]
            return tp

    def damage():

        with open('ManufacturerList.csv', 'r') as csvfile:
            damaged_reader = csv.reader(csvfile, delimiter=',')
            dmg = {}
            for row in damaged_reader:
                dmg[row[0]] = row[3]
            return dmg

    def price():

        with open('PriceList.csv', 'r') as csvfile:
            price_reader = csv.reader(csvfile, delimiter=',')
            prc = {}
            for row in price_reader:
                prc[row[0]] = row[1]
            return prc

    def service():

        with open('ServiceDatesList.csv', 'r') as csvfile:
            service_reader = csv.reader(csvfile, delimiter=',')
            srvc = {}
            for row in service_reader:
                srvc[row[0]] = row[1]
            return srvc

class WriteOutput:

    ## This class will handle all the .csv reports

    ## This function write Full Inventory Report. It takes a comprehensive data list as parameter
    def writeFullInv(full_list):
        ## Since list is already sorted by manufacturer, we can output it directly to FullInventory.csv
        with open('FullInventory.csv', 'w', newline='') as scvFullInv:
            full_inv = csv.writer(scvFullInv)
            full_inv.writerows(full_list)

    ## This function write Full Inventory Report. It takes a comprehensive data list and type list as parameter
    def writeTypeInv(full_list, type_list):
        sorted_list = sorted(full_list, key=lambda k: k[0])

        # This block of code is to find unique types of items in inventory, to be used later to name item files
        types_list = []
        for row3 in type_list:
            types_list.append(type_list[row3])
        unique_types = set(types_list)

        # This block of code reformat the list to NOT include type
        # In python, I can't copy an object with Assignment. However, using 'copy' module, I can make a deep copy of the list, even if it's 2-dimensional.
        duplicatelist1 = copy.deepcopy(sorted_list)
        for vudu in duplicatelist1:
            vudu.pop(2)

        # This block of code write Inventory
        for row4 in unique_types:
            hu = row4.strip().capitalize()
            with open('{}Inventory.csv'.format(hu), 'w', newline='') as scvfl:
                grades_writer = csv.writer(scvfl)
                # In order to if know an item belong to its respective inventory file, I need to check the type
                # Since I already made a copy of list early before remove the types, I'll use original list to check
                counter = 0
                for row4a in sorted_list:
                    if sorted_list[counter][2] == row4:
                        grades_writer.writerow(duplicatelist1[counter])
                    counter += 1

    ## This function write Past Service Dates Inventory Report. It takes a comprehensive data list as parameter
    def writePastDateInv(full_list):
        # I need to import time module to work with time-related inputs
        # This line sort the list by time
        sorted_list = sorted(full_list, key=lambda k: time.strptime(k[4], "%m/%d/%Y"))

        # This block of code determine if newlist2 has any items past service date. If it is, that item won't be imported to servicelist
        today = time.localtime()
        servicelist = []
        for row5 in sorted_list:
            date_format = time.strptime(row5[4], "%m/%d/%Y")
            if date_format < today:
                servicelist.append(row5)

        # Write to file
        with open('PastServiceDateInventory.csv', 'w', newline='') as scvflx:
            serviceWriter = csv.writer(scvflx)
            serviceWriter.writerows(servicelist)

    ## This function write Damaged Inventory Report. It takes a comprehensive data list as parameter
    def writeDmgInv(full_list):
        sorted_list = sorted(full_list, key=lambda k: int(k[3]), reverse=True)

        # This block determine of the item is damaged. If it is, it wont be imported to damagedList
        damaged_list = []
        for row6 in sorted_list:
            if row6[5] == "damaged":
                damaged_list.append(row6)

        # This block code remove the 'damaged' tag from the list
        # For posterity, damaged_list is copy, and only damaged_copy is edited
        damaged_copy = copy.deepcopy(damaged_list)
        for vudu1 in damaged_copy:
            vudu1.pop(5)

        # Write to file
        with open('DamagedInventory.csv', 'w', newline='') as scvflq:
            dmgWriter = csv.writer(scvflq)
            dmgWriter.writerows(damaged_copy)

class QueryUser:
    ## This class will handle queries from user

    def availInvList(f_list):
        ## This function will list all items that neither damaged nor past service date

        # This block control sort undamaged items
        dmg_list = sorted(f_list, key=lambda k: int(k[3]), reverse=True)
        avail_list = []
        for row6 in dmg_list:
            if row6[5] != "damaged":
                avail_list.append(row6)

        # This block sort service date
        today = time.localtime()
        avail_list2 = []
        for row5 in avail_list:
            wtf = time.strptime(row5[4], "%m/%d/%Y")
            if wtf > today:
                avail_list2.append(row5)

        final_list = copy.deepcopy(avail_list2)
        for vudu2 in final_list:
            vudu2.pop(4)
            vudu2.pop(4)

        return final_list

    # Query function
    def queryUser(f_list):
        user_ip = 0
        while user_ip != "q":
            print("Hello user!")
            print("To find an item in our inventory, please specify manufacturer and item type of the item:")

            user_ip = input()
            UI_tokens = user_ip.split()
            found1 = False
            found2 = False
            avail_items = []
            other_items = []
            # I'll search and compare each token of inputs to each element of items in inventory. It might not be the most efficient, but it will make sure whichever order the inputs are typed, they will be found (if exists in inventory)
            for rowUI in UI_tokens:
                for rowF in f_list:
                    # The if statement is used to compare manufacturer in f_list with what the user has typed
                    # In the example input files posted on final project, there is was a problem that "Apple" manufacturer has a trailing space behind it in all the csv files. That's why instead of using comparison, I'm using 'in' operator for this.
                    if str(rowUI).lower() in str(rowF[1]).lower():
                        # To determine if the user has typed both manufacturer information AND item type information, there are two flags for each of them: found1 is True when manufacturer match, and found2 is True when item type also match user inputs
                        found1 = True
                        # As the manufacturer has been found, this block will check item type of that same item against the user inputs
                        for rowUI2 in UI_tokens:
                            if str(rowUI2).lower() in str(rowF[2]).lower():
                                # As both the manafacturer and item type matches, found2 will be true, and item is appended to list of available items
                                found2 = True
                                avail_items.append(rowF)
                    # This block of code find items that match the item type description from user, to recommend a different option
                    elif str(rowUI).lower() in str(rowF[2]).lower():
                        # This check to see if this item that match item type, has same manufacturer as what user has input. If it's not the same manufacturer, append the item to list of recommendation
                        same_manufacturer = False
                        for rowUI3 in UI_tokens:
                            if str(rowUI3).lower() in str(rowF[1]).lower():
                                same_manufacturer = True
                        if same_manufacturer == False:
                            other_items.append(rowF)
                        # Whether or not there is any other option to recommend to the user, we still want to output the main item. Therefore, found2 has to be flagged as True.
                        found2 = True

            if found1 == True and found2 == True:
                print("Your item is:", avail_items[0])
                # If other_items list is empty, do not print other option. This will also save from a potential error, as other_items[0] do not exist if the list is empty.
                if other_items:
                    print("You may, also, consider:", other_items[0])
            elif found1 == True or found2 == True:
                print("Either you only specify a manufacturer or item type, or such specific set of item description does not match any item that exists in inventory.")
            else:
                print("No such item in inventory.")

            print("You can continue searching for another item by pressing enter, or enter 'q' if you're done")
            user_ip = input()

class DataDict:

    # This function generate a data dictionary from lists. Takes manufacturer list, type list, price list, service date list, and damage status list as parameters, respectively
    def generateDataDict(manufacturer, type, price, service, damage):
        ## Goal: Using all the available informations from these list to generate a comprehensive dictionary of inventory
        ## Dictionary format: {(item_id_1: [manufacturer_1, type_1, price_1, service_date_1, damage_status_1]), (item_id_2: [etc.])]

        # List all item ids as keys, using item ids from manufacturer
        u = manufacturer.keys()
        list_keys = []
        for row1 in u:
            list_keys.append(row1)

        comprehensive_data_dict = {}
        for row2 in list_keys:
            comprehensive_data_dict[row2] = [manufacturer[row2], type[row2], price[row2], service[row2], damage[row2]]
        return comprehensive_data_dict

    # This function generate a sorted list. Takes data dictionary generated by DataDict.generateDataDict as parameter
    def dictToSortedList(data_dict):
        ## After obtaining data dictionary, it will be converted to a sorted list (since dictionary is unsorted)
        ## The first list will be a comprehensive list of all data in data dictionary, sorted by manufacturer
        ## Each sorted list thereafter will be based off this list, and will be re-sorted depending of on the required output contents

        # sort_tuple format: [(item_id_1, [manufacturer_1, type_1, price_1, service_date_1, damage_status_1]), (item_id_2, [manufacturer_2, ...])]
        sort_tuple = sorted(data_dict.items(), key=lambda k: k[1][0])

        # This block of codes changes the sortlist from a list of tuples to a list of lists, to make it easier to edit and output to .csv files
        # sort_list format: [[item_id_1, manufacturer_1, type_1, price_1, service_date_1, damage_status_1], [item_id_2, manufacturer_2, ...]]
        sort_list = []
        list_counter = 0
        for row_sort in sort_tuple:
            temp_list = []
            temp_list.append(row_sort[0])
            temp_list.append(row_sort[1][0])
            temp_list.append(row_sort[1][1])
            temp_list.append(row_sort[1][2])
            temp_list.append(row_sort[1][3])
            temp_list.append(row_sort[1][4])
            sort_list.append(temp_list)
            list_counter += 1

        return sort_list



## The main code process will run from here
if __name__ == "__main__":

    # Receive all inputs files into lists
    a = InputList.manufacturer()
    b = InputList.type()
    c = InputList.price()
    d = InputList.service()
    e = InputList.damage()

    ## To get full dictionary and sort it into a list, use DataDict class
    data_dict = DataDict.generateDataDict(a, b, c, d, e)
    n = DataDict.dictToSortedList(data_dict)

    ## Call WriteInventory class to write reports

    WriteOutput.writeFullInv(n)
    WriteOutput.writeTypeInv(n, b)
    WriteOutput.writePastDateInv(n)
    WriteOutput.writeDmgInv(n)

    ## Call QueryUser class and make inventory of sellable items and ask user to search inside that inventory
    inv_list = QueryUser.availInvList(n)
    QueryUser.queryUser(inv_list)
