import csv
__author__ = 'stephen.finney'

"""
Checks that the address given exists in our list of all addresses so far
"""
def address_recorded(all_addresses, this_address):
    return this_address in all_addresses

"""
Checks that the address contains at least an Address line 1, City, State, and ZIP code
"""
def address_complete(this_address):
    return this_address[2] and this_address[4] and this_address[5] and this_address[6]

"""
Construct an address from the given CSV row
"""
def construct_address(csv_row):
    full_address = (csv_row[2] + ' ' + csv_row[3] + ' ' + csv_row[4] + ' ' + csv_row[5] + ' ')

    # Convert all ZIP codes to 5 digits only for consistency
    nine_digit_zip = csv_row[6].find('-')
    if nine_digit_zip > 0:
        full_address += csv_row[6][:nine_digit_zip]
    else:
        full_address += csv_row[6]

    return full_address.replace('.', ' ').replace('  ', ' ')

"""
Remove the given address from the existing list of data if it exists
"""
def remove_address_if_exists(all_addresses, this_address):
    count = 1
    for address in all_addresses:
        if address[7] == this_address:
            del all_addresses[count]
            return
        count += 1

"""
Identify new racers by comparing their addresses with the existing list of addresses
"""
def unique_racers(year, existing_addresses=[], results=[]):
    with open('./data/' + year + ' Participants.csv', newline='') as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='|')

        for row in csv_reader:
            # Skip if we're on the CSV headers, or the address is not complete
            if row[0] == 'LAST_NAME' or not address_complete(row):
                continue

            # Get a single, readable string for the address
            address = construct_address(row)

            # If the address hasn't been recorded yet, record it
            if not address_recorded(existing_addresses, address):
                existing_addresses.append(address)
                results.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], address])
    return results, existing_addresses

"""
Remove racers from the existing list of addresses if they match the addresses we find in the file for this year.
This method is used to find racers who haven't raced since 2011-2012. Therefore, I'm removing all racers that I
find in the 2013-2014 files from my list of racers from 2011-2012.
"""
def remove_existing_racers(year, existing_data=[]):
    with open('./data/' + year + ' Participants.csv', newline='') as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='|')

        for row in csv_reader:
            # Skip if we're on the CSV headers, or the address is not complete
            if row[0] == 'LAST_NAME' or not address_complete(row):
                continue

            # Get a single, readable string for the address
            address = construct_address(row)
            remove_address_if_exists(existing_data, address)


data_2011, address_list_2011 = unique_racers('2011')

print('2011 data')
print('----------')
print('Unique addresses: ' + str(len(data_2011)))
print()

data_2012, address_list_total = unique_racers('2012', address_list_2011, data_2011)

print('2012 data')
print('----------')
print('Unique addresses: ' + str(len(data_2012)))
print()

remove_existing_racers('2013', data_2012)
print('Removing duplicate racers from 2013')
print('-----------------------------------')
print('Unique addresses: ' + str(len(data_2012)))
print()

remove_existing_racers('2014', data_2012)
print('Removing duplicate racers from 2014')
print('-----------------------------------')
print('Unique addresses: ' + str(len(data_2012)))
print()

# Write out the final list of addresses
with open('./data/address_list_total.csv', 'w', newline='') as out_file:
    csv_writer = csv.writer(out_file, delimiter=',', quotechar='|')
    csv_writer.writerow(['LAST_NAME', 'FIRST_NAME', 'ADDRESS_1', 'ADDRESS_2', 'CITY', 'STATE', 'ZIP', 'FULL_ADDRESS'])
    for row in data_2012:
        csv_writer.writerow(row)

