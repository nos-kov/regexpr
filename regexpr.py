from pprint import pprint
import csv
import re

keywords = ('Минфин', 'ФНС')

def regexp(clean_list):
    pattern = r"(\+7|8)\s*\(*(\d\d\d)\)*(\D*|\-)(\d\d\d)(\D*)(\d\d)(\D*)(\d\d)(\s*)(\(*)(доб.\s\d\d\d\d)*\)*"
    replace = r"+7(\2)\4-\6-\8 \11"
    for element in clean_list:
        element[5] = re.sub(pattern, replace, element[5])
        print(element[5])


    return clean_list


def remove_dups(mylist):
    '''removes the duplicates and condenses the list'''

    marker_set = set()
    dup_free = []
    flatten = []
    merged_flatten = ['']*8
    

    for sublist in mylist:
        first_elt = sublist[0]
        if first_elt not in marker_set:
            dup_free.append(sublist)
            marker_set.add(first_elt)
        else:

            first_dup = [x for x in dup_free if first_elt in x[0]]
            flatten = [item for row in first_dup for item in row]
            zipped = list(zip(sublist,flatten))
            merged =  [list(x) for x in zipped]
            merged_flatten = ['']*8
            for idx, element in enumerate(merged):
                if element[0] == element[1]:
                    merged_flatten[idx] = element[0]
                elif element[0] == '' and element[1] != '':
                    merged_flatten[idx] = element[1]
                elif element[0] != '' and element[1] == '':
                    merged_flatten[idx] = element[0]   
                elif element[0] != '' and element[1] != '':
                    if len(element[0]) > len(element[1]):
                        merged_flatten[idx] = element[0]
                    else: merged_flatten[idx] = element[1]
            
            for id, myelement in enumerate(dup_free):
                if id > 0 and merged_flatten[0] in myelement:
                    dup_free.pop(id)
                    dup_free.append(merged_flatten)
                    break



            
    return dup_free

if __name__ == '__main__':


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


    for idx, data in enumerate(clean_list):
        if idx > 0: 
            fixed = False
            flag, flag1, flag2, flag3 = (False,)*4
            for idy, result_element in enumerate(data):
                if fixed == True: continue
                if idy > 2: 
                    
                    if result_element in keywords and idy != 3: 
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
                        if result_element in keywords: continue
                        data[4] = result_element
                        if idy != 4:
                            data[idy] = ''
                        flag3 = True
                    if all((flag,flag1,flag2,flag3)) : fixed = True

regexp(clean_list)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(clean_list)

#(\+7|8)\s*\(*(\d\d\d)\)*(\D*|\-)(\d\d\d)(\D*)(\d\d)(\D*)(\d\d)(\s*)(\(*)(доб.\s\d\d\d\d)*\)*
#+7(\2)\4-\6-\8 \11