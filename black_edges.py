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

        features.append(p_2)
        classes.append(c)


#features = np.array(features)
#classes = np.array(classes)


# def bfs_recurse(f, n, stack, obj):
#     while(len(stack) > 0):
#         s = int(stack.pop())
#         print("here:", f[s], " ", s)

#         if (f[s] != 0.0):
#             obj.append(s)
#             if (s+1 <= n and (s+1) not in obj):
#                 stack.append(s+1)
#             if (s-1 >= 0 and (s-1) not in obj):
#                 stack.append(s-1)
#             if (s + math.sqrt(n) <= n and (s + math.sqrt(n)) not in obj):
#                 stack.append(s + math.sqrt(n))
#             if (s - math.sqrt(n) >= 0 and (s - math.sqrt(n)) not in obj):
#                 stack.append(s - math.sqrt(n))
    
#     return obj

def bfs_feature(f):
    start = len(f) // 2
    obj = []
    stack = []
    n = len(f)
    sqrt_n = int(math.sqrt(n))
    print ("sqrt n: ", sqrt_n)
    stack.append(start)
    stack.append(start +  1)
    stack.append(start - 1)
    stack.append(start + sqrt_n)
    stack.append(start - sqrt_n)
    threshold = np.mean(f) / 3
    print ("threshold: ", threshold)

    #obj = bfs_recurse(f, len(f), stack, obj)
    while(len(stack) > 0):
        s = int(stack.pop())
        if (s in obj):
            continue
        #print("here:", f[s], " ", s)

        if (f[s] > threshold):
            obj.append(s)
            if (s+1 < n and (s+1) not in obj):
                stack.append(s+1)
            if (s-1 >= 0 and (s-1) not in obj):
                stack.append(s-1)
            if (s + sqrt_n < n and (s + sqrt_n) not in obj):
                stack.append(s + sqrt_n)
            if (s - sqrt_n >= 0 and (s - sqrt_n) not in obj):
                stack.append(s - sqrt_n)

    print ("len obj: ", len(obj))
    return obj


for feature in features:
    galaxy = bfs_feature(feature)
    for i in range(0, len(feature)):
        if (i not in galaxy):
            feature[i] = 0.0

with open('training_data_abridged_blacked.csv', 'w', newline='') as  outputfile:
    writer = csv.DictWriter(outputfile, ['OBJID', 'pixels', 'class'])
    writer.writeheader()

    for i in range(0, len(features)):
        line = features[i]
        c = classes[i]
        c = c.index(1)
        pixels_string = ' '.join(line)
        row = {'OBJID': line['OBJID'], 'pixels': pixels_string, 'class': c}
        writer.writerow(row)
    