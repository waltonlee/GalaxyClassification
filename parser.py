# "cleans" the data into a sample for which the percent vote for a particular object is above 'confidence'


import csv

confidence = 0.9



with open('GalaxyZoo1_DR_table2.csv') as inputfile:
    data = csv.DictReader(inputfile)

    with open('GZ_clean.csv', 'w', newline='') as  outputfile:
        writer = csv.DictWriter(outputfile, data.fieldnames)
        writer.writeheader()

        for row in data:
            if (float(row['P_EL']) > confidence or float(row['P_CW']) > confidence or float(row['P_ACW']) > confidence):
                writer.writerow(row)

