from pprint import pprint
import re
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
with open("phonebook_raw.csv", encoding="utf8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
#pprint(contacts_list)

## 1. Выполните пункты 1-3 задания.
## Ваш код
#flag = False
result = []
keywords = ('Минфин', 'ФНС')

for element in contacts_list:
    clean_ = element[0].split()
    new_element =[]
    new_element = clean_ + new_element
    for id_el, nested_element in enumerate(element):
        #nested_element_list =[]
        #if flag == True: break
        if id_el > 0:
            #if  nested_element: nested_element_list = [nested_element]
            nested_element_list = [nested_element]
            new_element = new_element + nested_element_list
            if id_el > 3:

                for idx, data in enumerate(new_element[4:]):
                    if data in keywords: 
                        new_element[3] = data
                        new_element[idx+4] = ''
                        #flag = True
                        #break
                    if '@' in data:
                        new_element[6] = data
                        new_element.pop(idx+4)

                for idx, data in enumerate(new_element[6:]):
                    if re.search(r'\d\d\d', data):
                        new_element[5] = data
                        #new_element.pop(idx+4)
                        new_element[idx+6] = ''


    result.append(new_element[:7])


pprint(result)
## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
  
## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_list)
    #e
