import csv
import numpy as np
import math
import sys

maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

with open('training_data_abridged.csv') as infile:
    data = csv.DictReader(infile)

    ids = []
    features = []
    classes = []
    for line in data:
        p = line['pixels']
        p = p.split()
        #print (p)

        p_2 = []
        for i in p:
            p_2.append(float(i))

        c = [0,0,0]
        c[int(line['class'])] = 1

        ids.append(line['OBJID'])
        features.append(p_2)
        classes.append(c)


def bounding_box(f):
    threshold = np.median(f) / 2
    #print (f)
    max_dir = 0

    n = len(f)
    sqrt_n = int(math.sqrt(n))
    start = int(n // 2)

    # check right
    s = start
    i = 0
    while(f[s] > threshold):
        i = i+1
        s = s+1
        if (s > start + sqrt_n):
            return sqrt_n

    if (i > max_dir):
        max_dir = i

    # check left
    s = start
    i = 0
    while(f[s] > threshold):
        i = i+1
        s = s-1

        if (s < start - sqrt_n):
            return sqrt_n

    if (i > max_dir):
        max_dir = i
    
    # check down
    s = start
    i = 0
    while(f[s] > threshold):
        i = i+1
        s = s+sqrt_n
        if (s > n):
            return sqrt_n

    if (i > max_dir):
        max_dir = i

    # check up
    s = start
    i = 0
    while(f[s] > threshold):
        i = i+1
        s = s-sqrt_n
        if (s < 0):
            return sqrt_n

    if (i > max_dir):
        max_dir = i

    return max_dir


for feature in features:
    galaxy = bounding_box(feature)
    print (galaxy)

    n = len(feature)
    sqrt_n = math.sqrt(n)
    start = n // 2

    for i in range(0, len(feature)):
        if (abs((i%sqrt_n)-start) <= galaxy and (i < start + galaxy*sqrt_n + galaxy) and (i > start - galaxy*sqrt_n - galaxy)):
            feature[i] = 0.0

with open('training_data_abridged_blacked.csv', 'w', newline='') as  outputfile:
    writer = csv.DictWriter(outputfile, ['OBJID', 'pixels', 'class'])
    writer.writeheader()

    for i in range(0, len(features)):
        line = features[i]
        line = [str(l) for l in line]
        c = classes[i]
        c = c.index(1)
        pixels_string = ' '.join(line)
        row = {'OBJID': ids[i], 'pixels': pixels_string, 'class': c}
        writer.writerow(row)
    