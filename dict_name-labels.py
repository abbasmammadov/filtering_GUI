


names = ['경전철제3궤조catenary-normal', '도시철도강체bolt-nut-normal', '도시철도강체catenary-normal', '고속철도카테너리catenary-normal', '고속철도카테너리insulator-normal', '도시철도강체safety_pin-normal', '고속철도카테너리clamp-normal', '고속철도카테너리insulator-abnormal', '고속철도카테너리protector-normal', '도시철도강체long_ear-normal', '도시철도강체insulator-normal', '고속철도카테너리hanger-abnormal', '고속철도카테너리hanger-normal', '도시철도강체T-Bar-normal', '경전철제3궤조bolt-nut-normal', '경전철제3궤조insulator-normal']

def labels_to_names(labels_file):
    res = list()
    with open(labels_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            res.append(names[int(line.split(' ')[0])])

    #list to dict with count
    res_dict = dict()
    for i in res:
        if i in res_dict:
            res_dict[i] += 1
        else:
            res_dict[i] = 1

    #sort dict by value
    res_dict = dict(sorted(res_dict.items(), key=lambda item: item[1], reverse=True))
    
    return res_dict


# let's make a csv file with img names and labels

import csv

img_names = list()
with open('/Users/abbasmammadov/Desktop/PyQt6-missings/totest.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        img_names.append(line.strip())

with open('pred_labels.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['img_name', 'labels'])
    for i in range(len(img_names)):
        writer.writerow([img_names[i], labels_to_names(f'/Users/abbasmammadov/Desktop/PyQt6-missings/pred_labels/{img_names[i]}.txt')])
