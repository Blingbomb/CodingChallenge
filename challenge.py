import operator
import os
import json
import sys


# extended "Main" to avoid repeating startup text
def startup():
    print("Possible commands: --help --start")
    us_inp = input('> ')
    if us_inp == "--help":
        print("Program made for BKWatch Challenge. Enter the path to a folder containing formatted xml, tsv, or txt"
              "\nfiles to batch convert them into JSON objects.")
    if us_inp == "--start":
        menu()
    else:
        startup()


# startup text
def main():
    print("XML / TSV / TXT -> JSON file converter")
    print("4/15/2024")
    print("by MicroCoin (Amateur)")
    startup()


# selection menu and file checking
def menu():
    parsed_list = []
    folder_path = input("Please Insert Path to Folder: ")
    if not os.path.isdir(folder_path):
        menu()
    else:
        for filename in os.listdir(folder_path):
            filecheck = os.path.join(folder_path, filename)

            if os.path.isfile(filecheck):
                file_type = type_checker(filecheck)
                file_dump = open(filecheck, "r")
                file_dump = file_dump.read()
                if file_type == "txt":
                    parsed_list += plaintext_to_json(file_dump)
                elif file_type == "xml":
                    parsed_list += xml_to_json(file_dump)
                elif file_type == "tsv":
                    parsed_list += tsv_to_json(file_dump)
                else:
                    pass
            else:
                pass
    parsed_list = sorted(parsed_list, key=operator.itemgetter('zip'))
    parsed_list = json.dumps(parsed_list, indent=4)
    sys.stdout.write(parsed_list)


# Check file type for correct handling
def type_checker(unk_file_ext):
    if ".tsv" in unk_file_ext:
        return "tsv"
    elif ".xml" in unk_file_ext:
        return "xml"
    elif ".txt" in unk_file_ext:
        return "txt"
    else:
        print("Error: Unsupported Filetype")
        return "err"


# Plaintext converter
def plaintext_to_json(plaintext):
    plaintext = plaintext.strip("\n")
    plaintext = plaintext.split("\n\n")
    output2 = []
    dict_key = {"name": 1, "street": 2, "city": 3, "county": 4, "state": 5, "zip": 6}
    for entry in plaintext:
        pdata = {}
        local_line_count = 0
        ent_lines = entry.count("\n")
        ent_list = entry.split("\n")
        if ent_lines > 0:
            for data in ent_list:
                data = data[2:]
                if local_line_count == 0:
                    pdata["name"] = data
                elif local_line_count == 1:
                    pdata["street"] = data
                elif local_line_count == 2 and ent_lines == 2 or local_line_count == 3 and ent_lines == 3:
                    temp_split = data.split(",")
                    pdata["city"] = temp_split[0]
                    temp_split = temp_split[1]
                    temp_split = temp_split[1:]
                    temp_split = temp_split.split(" ")
                    if len(temp_split) > 2:
                        zip_code = temp_split.pop().strip(" ")
                        if len(zip_code) == 6:
                            zip_code = zip_code[:5]
                        state = temp_split[0] + " " + temp_split[1]
                        pdata["state"] = state
                        pdata["zip"] = zip_code
                    elif len(temp_split) == 2:
                        zip_code = temp_split.pop().strip(" ")
                        if len(zip_code) == 6:
                            zip_code = zip_code[:5]
                        state = temp_split[0]
                        pdata["state"] = state
                        pdata["zip"] = zip_code
                    else:
                        print("Unknown Formatting")
                        sys.exit()
                elif local_line_count == 2 and ent_lines == 3:
                    pdata["county"] = data
                local_line_count += 1
        else:
            print("Incorrect Entry formatting")
            sys.exit()
        p_datavalues = []
        for key in pdata:
            p_datavalues.append(pdata[key])
        p_data_keys = sorted(pdata, key=lambda x: dict_key[x])
        pdata = zip(p_data_keys, p_datavalues)
        pdata = dict(pdata)
        output2.append(pdata)
    return output2


# Xml converter
def xml_to_json(xml_file):
    list_of_search_results = {}
    pdata = {}
    output2 = []
    data_type = ['name', 'company', 'street', 'city', 'state', 'zip']
    search_set_1 = ['<NAME>', '<COMPANY>', '<STREET>', '<CITY>', '<STATE>', '<POSTAL_CODE>']
    search_set_2 = ['</NAME>', '</COMPANY>', '</STREET>', '</CITY>', '</STATE>', '</POSTAL_CODE>']
    for search_var in range(len(search_set_1)):
        search_start = search_set_1[search_var]
        search_end = search_set_2[search_var]
        search_start_found = 0
        search_end_found = 0
        search_number = xml_file.count(search_start)
        search_list = []
        for _ in range(search_number):
            search_start_index = xml_file.find(search_start, search_start_found + 1)
            search_end_index = xml_file.find(search_end, search_end_found + 1)
            search_list.append(xml_file[search_start_index + len(search_start): search_end_index])
            search_start_found = search_start_index
            search_end_found = search_end_index
        list_of_search_results[search_start] = search_list
    for index, item in enumerate(list_of_search_results['<NAME>']):
        for index0, types in enumerate(data_type):
            if list_of_search_results[search_set_1[index0]][index] != ' ' and types != 'zip':
                pdata[types] = list_of_search_results[search_set_1[index0]][index]
            elif types == 'zip':
                zips = list_of_search_results[search_set_1[index0]][index]
                if len(zips) < 9:
                    pdata[types] = zips[:5]
                else:
                    pdata[types] = zips[:5] + zips[6] + zips[8:]

        output2.append(pdata)
        pdata = {}
    return output2


# Tsv converter
def tsv_to_json(tsv_file):
    types = ['firstname', 'middle-name', 'lastname', 'company', 'address', 'city', 'state', 'county', 'zip', 'zip4']
    usable_tsv = tsv_file.replace("\t", "--").strip().split('\n')
    people = []
    companies = []
    output2 = []
    for line in usable_tsv[1:]:
        if "----" not in line[0:4]:
            people.append(line)
        else:
            companies.append(line)
        pass
    pass
    for company in companies:
        for i in range(len(company)):
            if company[i] == '-':
                pass
            else:
                new_company = ("--" + "--" + "--" + company[i:])
                for v in range(len(new_company)):
                    if new_company[v + 5:v + 7] != '--':
                        pass
                    else:
                        temp_comp = str(new_company[0:v + 5]).strip() + "--" + str(new_company[12 + v:]).strip()
                        people.append(temp_comp)
                        break
                break
        pass
    pass
    for person in people:
        n = 0
        pdata = {}
        person = person.split('--')
        p_name = ''
        zips = ''
        for data in person:
            data_type = types[n]
            if n < 2 and data != "N/M/N":
                p_name += data + " "
            elif n == 2 and data != '' and data != ' ' and data != '  ':
                p_name += data
                pdata['name'] = p_name
            elif 8 > n > 2 and data != '' and data != 'N/A':
                pdata[data_type] = data
            elif n == 8 and data != '' and data != "N/A":
                zips = data
            elif n == 9 and data != "N/A":
                if data != '':
                    pdata['zip'] = zips + '-' + data
                else:
                    pdata['zip'] = zips

            n += 1
        output2.append(pdata)
    return output2


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        sys.exit(1)
    else:
        sys.exit(0)
