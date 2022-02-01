import re
import csv

#Declare File Locations
countries_txt = r"C:\Games\Victoria GIT\mod\PDX ARG MP\common\countries.txt"
saves_folder = r"C:\Users\Jaeger\Documents\Paradox Interactive\Victoria II\PDX ARG MP\save games"

#NOTE: Files MUST be named in a numerical date order, so 1.v2 2.v2 3.v2, etc. Otherwise this tool will NOT work 

#Data Configuration
saves_per_year = 1
number_of_saves = 17
first_year = 1836

include_vassal_in_overlord = False #Incoportate Vassals into the Overlod data
divide_all_results_by = 1 
remove_0_tags = True  # Remove Empty Tags
output_file_name = "test1"
Use_All_Tags = False  #False if using the below
Use_Only_These_Tags = ["USA","FRA","ENG","RUS","AUS","KUK","SAR","ITA","TKG","JAP","SPA","IBR","TUR","PRU","NGF","CAN"]

year_list = ["blah", "blah"]
country_list = [["XXX", "Indigenous People"]]

def read_in_countries():
    for line in open(countries_txt):
        firstsplit = line.split("=")

        if len(firstsplit) != 2:
            continue

        tag = firstsplit[0][:3]

        if firstsplit[0] == "dynamic_tags  ":
            continue

        secondsplit = re.split("/|\"", firstsplit[1])
        english_name = secondsplit[2].split(".")[0]
        country_list.append([tag, english_name])

    for i in range(number_of_saves):
        for i in range(saves_per_year):
            year_list.append(first_year + i)
        for i in range(len(country_list)):
            for j in range(saves_per_year):
                country_list[i].append(0)

def Population_Reader():
    for l in range(1, 1 + (saves_per_year * number_of_saves)):
        print(str(int(100 * l / (saves_per_year * number_of_saves))) + "%")
        filename = saves_folder + "/" + str(l) + ".v2"
        province_end_tag = True
        savefile = open(filename, encoding='ISO-8859-1')
        current_tag = "REB"
        i = 0
        current_province = 1
        for line in savefile:
            i += 1
            if province_end_tag:

                if line[1:6] == "owner":
                    current_tag = line[8:11]
                    for k in range(len(country_list)):
                        if current_tag == country_list[k][0]:
                            current_tag_index = k

                elif line == "REB=\n":
                    province_end_tag = False

                elif line == str(current_province) + "=\n":
                    current_tag = "XXX"
                    current_tag_index = 0
                    current_province += 1

                if line[2:7] == "size=":
                    pop_size = int(line[7:-1]) * 4 / divide_all_results_by
                    country_list[current_tag_index][l + 1] += pop_size

        if include_vassal_in_overlord:
            savefile = open(filename, encoding='ISO-8859-1')
            last_vassal = -5
            p = 0
            for line in savefile:

                p += 1
                if line[1:8] == "vassal=" or line[1:10] == "substate=":
                    last_vassal = p

                if p == last_vassal + 2:
                    master_tag = line[9:12]

                if p == last_vassal + 3:
                    vassal_tag = line[10:13]
                    master_index = None
                    vassal_index = None
                    for m in range(len(country_list)):
                        if country_list[m][0] == master_tag:
                            master_index = m
                        if country_list[m][0] == vassal_tag:
                            vassal_index = m

                    if master_index == None:
                        print(master_tag)
                    if vassal_index == None:
                        print(vassal_tag)

                    country_list[master_index][l + 1] += country_list[vassal_index][l + 1]
                    country_list[vassal_index][l + 1] = 0

                    master_tag = None
                    vassal_tag = None

def GDP_Reader():
    for l in range(1, 1 + (saves_per_year * number_of_saves)):
        print(str(int(100 * l / (saves_per_year * number_of_saves))) + "%")
        filename = saves_folder + "/" + str(l) + ".v2"
        province_end_tag = True
        savefile = open(filename, encoding='ISO-8859-1')
        current_tag = "REB"
        i = 0
        current_province = 1
        for line in savefile:
            i += 1
            if province_end_tag:

                if line[1:6] == "owner":
                    current_tag = line[8:11]
                    for k in range(len(country_list)):
                        if current_tag == country_list[k][0]:
                            current_tag_index = k
                # print(current_tag)

                elif line == "REB=\n":
                    province_end_tag = False

                elif line == str(current_province) + "=\n":
                    current_tag = "XXX"
                    current_tag_index = 0
                    current_province += 1

                # Artisans
                if line[2:16] == "last_spending=":
                    country_list[current_tag_index][l + 1] -= float(line[16:]) / 1000 * 365.25 / divide_all_results_by
                elif line[2:20] == "production_income=":

                    country_list[current_tag_index][l + 1] += float(line[20:]) / 1000 * 365.25 / divide_all_results_by

                # RGO
                if line[2:14] == "last_income=":
                    country_list[current_tag_index][l + 1] += float(line[14:]) / 1000 * 365.25 / divide_all_results_by

            else:
                if line[3:] == "=\n":
                    if ord(line[0]) >= 65 and ord(line[0]) <= 90 and ord(line[1]) >= 65 and ord(
                            line[1]) <= 90 and ord(line[2]) >= 65 and ord(line[2]) <= 90:
                        current_tag = line[0:3]
                        for k in range(len(country_list)):
                            if current_tag == country_list[k][0]:
                                current_tag_index = k

                # factory
                if line[3:17] == "last_spending=":
                    country_list[current_tag_index][l + 1] -= float(line[17:]) / 1000 * 365.25 / divide_all_results_by
                elif line[3:15] == "last_income=":
                    country_list[current_tag_index][l + 1] += float(line[15:]) / 1000 * 365.25 / divide_all_results_by
        if include_vassal_in_overlord:
            savefile = open(filename, encoding='ISO-8859-1')
            last_vassal = -5
            p = 0
            for line in savefile:

                p += 1
                if line[1:8] == "vassal=" or line[1:10] == "substate=":
                    last_vassal = p

                if p == last_vassal + 2:
                    master_tag = line[9:12]

                if p == last_vassal + 3:
                    vassal_tag = line[10:13]
                    master_index = None
                    vassal_index = None
                    for m in range(len(country_list)):
                        if country_list[m][0] == master_tag:
                            master_index = m
                        if country_list[m][0] == vassal_tag:
                            vassal_index = m

                    if master_index == None:
                        print(master_tag)
                    if vassal_index == None:
                        print(vassal_tag)

                    country_list[master_index][l + 1] += country_list[vassal_index][l + 1]
                    country_list[vassal_index][l + 1] = 0

                    master_tag = None
                    vassal_tag = None

def Culture_Religion():
    for l in range(1, 1 + (saves_per_year * number_of_saves)):
        print(str(int(100 * l / (saves_per_year * number_of_saves))) + "%")
        filename = saves_folder + "/" + str(l) + ".v2"
        province_end_tag = True
        savefile = open(filename, encoding='ISO-8859-1')
        current_tag = "REB"
        current_province = 1
        size_flag = False
        province_num = 0
        for line in savefile:

            if province_end_tag:

                if line[1:6] == "owner":
                    current_tag = line[8:11]

                if line[4:6] == "=\n" and line[3:4] != "o" and line[3:4] != "d":
                    current_province = line[0:4]
                    current_tag = "Null"
                    # print(current_province)

                elif line == "REB=\n":
                    province_end_tag = False

                if current_tag in Use_Only_These_Tags or Use_All_Tags:
                    if size_flag:
                        size_flag = False
                        current_culture = line[2:-1]
                        added_Flag = False
                        for j in range(len(country_list)):
                            if current_culture == country_list[j][0]:
                                country_list[j][l] += pop_size
                                added_Flag = True
                                break
                        if not added_Flag:
                            country_list.append([current_culture])
                            for i in range(saves_per_year * number_of_saves):
                                country_list[-1].append(0)
                            country_list[-1][l] += pop_size

                    if line[2:7] == "size=":
                        pop_size = int(line[7:-1]) * 4 / divide_all_results_by
                        size_flag = True

if __name__ == "__main__":
    read_in_countries()

    Population_Reader()
    year_list = ["Code", "Name"]

    for j in range(number_of_saves):
        for k in range(saves_per_year):
            year_list.append(first_year + j)

    if remove_0_tags:
        country_list = [x for x in country_list if max(x[2:]) > 0]

    with open("Population" + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        f.write("SEP=,\n")
        writer.writerow(year_list)
        writer.writerows(country_list)

    country_list = [["XXX", "Indigenous People"]]
    read_in_countries()

    GDP_Reader()
    year_list = ["Code", "Name"]

    for j in range(number_of_saves):
        for k in range(saves_per_year):
            year_list.append(first_year + j)

    if remove_0_tags:
        country_list = [x for x in country_list if max(x[2:]) > 0]

    with open("GDP" + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        f.write("SEP=,\n")
        writer.writerow(year_list)
        writer.writerows(country_list)

    country_list = [["XXX", "Indigenous People"]]
    read_in_countries()

    Culture_Religion()
    year_list = ["Culture"]

    for j in range(number_of_saves):
        for k in range(saves_per_year):
            year_list.append(first_year + j)

    if remove_0_tags:
        country_list = [x for x in country_list if max(x[2:]) > 0]

    with open("Culture and Religion" + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        f.write("SEP=,\n")
        writer.writerow(year_list)
        writer.writerows(country_list)