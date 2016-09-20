import csv, png

with open('training_data_rmb.csv') as inputfile:
    data = csv.DictReader(inputfile)
    with open('training_data_abridged_rmb.csv', 'w', newline='') as  outputfile:
        writer = csv.DictWriter(outputfile, ['OBJID', 'pixels', 'class'])
        writer.writeheader()

        i = 0
        for line in data
            writer.writerow(line)
            i = i + 1
            if (i > 10000):
                break