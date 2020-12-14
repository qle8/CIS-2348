import csv
import operator
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


    ## 1st Report
    def writeFullInv(n1):
        ## Since list is already sorted by manufacturer, we can output it directly to FullInventory.csv
        with open('FullInventory.csv', 'w', newline='') as scvFullInv:
            full_inv = csv.writer(scvFullInv)
            full_inv.writerows(n1)

    ## 2nd Report
    def writeTypeInv(n2):
        newlist1 = sorted(n2, key=lambda k: k[0])

        # This block of code is to find unique types of items in inventory, to be used later to name item files
        types_list = []
        for row3 in b:
            types_list.append(b[row3])
        unique_types = set(types_list)

        # This block of code reformat the list to NOT include type
        # In python, I can't copy an object with Assignment. However, using 'copy' module, I can make a deep copy of the list, even if it's 2-dimensional.
        duplicatelist1 = copy.deepcopy(newlist1)
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
                for row4a in newlist1:
                    if newlist1[counter][2] == row4:
                        grades_writer.writerow(duplicatelist1[counter])
                    counter += 1

    ## 3rd Report
    def writePastDateInv(n3):
        # I need to import time module to work with time-related inputs
        # This line sort the list by time
        newlist2 = sorted(n3, key=lambda k: time.strptime(k[4], "%m/%d/%Y"))

        # This block of code determine if newlist2 has any items past service date. If it is, that item won't be imported to servicelist
        today = time.localtime()
        servicelist = []
        for row5 in newlist2:
            date_format = time.strptime(row5[4], "%m/%d/%Y")
            if date_format < today:
                servicelist.append(row5)

        # Write to file
        with open('PastServiceDateInventory.csv', 'w', newline='') as scvflx:
            serviceWriter = csv.writer(scvflx)
            serviceWriter.writerows(servicelist)

    ## 4th Report
    def writeDmgInv(n4):
        newlist3a = sorted(n4, key=lambda k: int(k[3]), reverse=True)

        # This block determine of the item is damaged. If it is, it wont be imported to damagedList
        damagedList = []
        for row6 in newlist3a:
            if row6[5] == "damaged":
                damagedList.append(row6)

        # This block code remove the 'damaged' tag from the list
        # In python, I can't copy an object with Assignment. However, using 'copy' module, I can make a deep copy of the list, even if it's 2-dimensional.
        printDMGList = copy.deepcopy(damagedList)
        for vudu1 in printDMGList:
            vudu1.pop(5)

        # Write to file
        with open('DamagedInventory.csv', 'w', newline='') as scvflq:
            dmgWriter = csv.writer(scvflq)
            dmgWriter.writerows(printDMGList)


class QueryUser:
    ## This class will handle queries from user

    def availInvList(m1):
        ## This function will list all items that neither damaged nor past service date

        # This block control sort undamaged items
        dmg_list = sorted(m1, key=lambda k: int(k[3]), reverse=True)
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

    # query func
    def queryUser(f_list):
        user_ip = 0
        while user_ip != "q":
            print("Hello user!")
            print("To find an item in our inventory, please specify manufacturer and item type of the item:")

            user_ip = input()
            UI_tokens = user_ip.split()
            found1 = False
            found2 = False
            found3 = False
            avail_items = []
            other_items = []
            # I'll search and compare each token of inputs to each element of items in inventory. It might not be the most efficient, but it will make sure whichever order the inputs are typed, they will be found (if exists in inventory)
            for row9 in UI_tokens:
                for row7 in f_list:
                    # In the input files posted on final project, there is was a problem that "Apple" manufacturer has a trailing space behind it in all the csv files. That's why instead of using comparison, I'm using 'in' operator for this.
                    if str(row9) in str(row7[1]):
                        found1 = True
                        for row112 in UI_tokens:
                            if str(row112) in str(row7[2]):
                                found2 = True
                                found3 = True
                                avail_items.append(row7)
                    elif str(row9) in str(row7[2]):
                        same_manufacturer = False
                        for row131 in UI_tokens:
                            if row131 in str(row7[1]):
                                same_manufacturer = True
                        if same_manufacturer == False:
                            other_items.append(row7)
                        found2 = True

            if found1 == True and found2 == True and found3 == True:
                print("Your item is:", avail_items[0])
                if other_items:
                    print("You may, also, consider:", other_items[0])
            elif found1 == True or found2 == True:
                print("Either you only specify a manufacturer or item type, or such specific set of item description does not match any item that exists in inventory.")
            else:
                print("No such item in inventory.")

            print("You can continue searching for another item by pressing enter, or enter 'q' if you're done")
            user_ip = input()


if __name__ == "__main__":

    a = InputList.manufacturer()
    b = InputList.type()
    c = InputList.price()
    d = InputList.damage()
    e = InputList.service()

    ## Goal: Using all the available informations from these list to generate a comprehensive dictionary of inventory

    u = a.keys()
    list_keys = []
    for row1 in u:
        list_keys.append(row1)

    comprehensive_data_dict = {}
    for row2 in list_keys:
        comprehensive_data_dict[row2] = [a[row2], b[row2], c[row2], e[row2], d[row2]]

    ## After obtaining data dictionary, I'll convert it to a sorted list (since dictionary is unsorted)
    ## The first list will be a comprehensive list of all data in data dictionary
    ## Each sorted list thereafter will be sorted depend of on the required output contents

    sortlist = sorted(comprehensive_data_dict.items(), key=lambda k: k[1][0])

    n = []
    list_counter = 0
    for row_sortlist in sortlist:
        temp_list = []
        temp_list.append(row_sortlist[0])
        temp_list.append(row_sortlist[1][0])
        temp_list.append(row_sortlist[1][1])
        temp_list.append(row_sortlist[1][2])
        temp_list.append(row_sortlist[1][3])
        temp_list.append(row_sortlist[1][4])
        n.append(temp_list)
        list_counter+=1

    ## Call WriteInventory and QueryUser classes

    WriteOutput.writeFullInv(n)
    WriteOutput.writeTypeInv(n)
    WriteOutput.writePastDateInv(n)
    WriteOutput.writeDmgInv(n)


    inv_list = QueryUser.availInvList(n)
    QueryUser.queryUser(inv_list)
