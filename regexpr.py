from pprint import pprint
import re

def remove_dups(list):
    marker_set = set()
    dup_free = []

    for sublist in list:
        first_elt = sublist[0]
        if first_elt not in marker_set:
            dup_free.append(sublist)
            marker_set.add(first_elt)
    return dup_free

import csv
with open("phonebook_raw.csv", encoding="utf8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

semiresult = []

for element in contacts_list:
    clean1 = element[0].split()
    clean2 = element[1].split()
    new_element =[]
    new_element = clean1 + clean2 + new_element
    for id_el, nested_element in enumerate(element):

        if id_el > 1:
            
            nested_element_list = [nested_element]
            new_element = new_element + nested_element_list

    semiresult.append(new_element)

clean_list = remove_dups(semiresult)
#clean_list = semiresult
keywords = ('Минфин', 'ФНС')
for idx, data in enumerate(clean_list):
    if idx > 0: 
        fixed = False
        flag, flag1, flag2, flag3 = (False,)*4
        for idy, result_element in enumerate(data):
            if fixed == True: continue
            if idy > 2: 
                
                if result_element in keywords: 
                    data[3] = result_element
                    data[idy] = ''
                    flag = True
                            
                elif '@' in result_element:
                    data[6] = result_element
                    data.pop(idy)
                    flag1 = True

                elif re.search(r'\d\d\d', result_element) and '@' not in result_element:
                    data[5] = result_element
                    data[idy] = ''
                    flag2 = True
                elif result_element == '':
                    pass
                else:
                    data[4] = result_element
                    data[idy] = ''
                    flag3 = True
                if all((flag,flag1,flag2,flag3)) : fixed = True

pprint(clean_list)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
  
    datawriter.writerows(contacts_list)
