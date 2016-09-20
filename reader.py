import csv
import numpy as np
import tensorflow.contrib.learn as skflow
from sklearn import datasets, metrics
from sklearn.cross_validation import KFold
import sys
import tensorflow as tf

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

features = np.array(features)
classes = np.array(classes)



classes = np.argmax(classes, axis=1)
#print(features.shape, " ", classes.shape)

def max_pool_2x2(tensor_in):
    return tf.nn.max_pool(tensor_in, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
        padding='SAME')

def conv_model(X, y):
    # reshape X to 2d tensor with 2nd and 3rd dimensions being image width and height
    # final dimension being the number of color channels
    X = tf.reshape(X, [-1, 192, 192, 1])
    # first conv layer will compute 32 features for each 5x5 patch
    with tf.variable_scope('conv_layer1'):
        h_conv1 = skflow.ops.conv2d(X, n_filters=32, filter_shape=[5, 5], 
                                    bias=True, activation=tf.nn.relu)
        h_pool1 = max_pool_2x2(h_conv1)
    # second conv layer will compute 64 features for each 5x5 patch
    with tf.variable_scope('conv_layer2'):
        h_conv2 = skflow.ops.conv2d(h_pool1, n_filters=64, filter_shape=[5, 5], 
                                    bias=True, activation=tf.nn.relu)
        h_pool2 = max_pool_2x2(h_conv2)
        # reshape tensor into a batch of vectors
        h_pool2_flat = tf.reshape(h_pool2, [-1, 48 * 48 * 64])
    # densely connected layer with 1024 neurons
    h_fc1 = skflow.ops.dnn(h_pool2_flat, [1024], activation=tf.nn.relu, keep_prob=0.5)
    return skflow.models.logistic_regression(h_fc1, y)

# Training and predicting
classifier = skflow.TensorFlowEstimator(
    model_fn=conv_model, n_classes=3, batch_size=33, steps=500,
    learning_rate=0.001)

#classifier = skflow.TensorFlowDNNClassifier(hidden_units=[100, 20, 10], n_classes=3)
classifier.fit(features, classes)
score = metrics.accuracy_score(classes, classifier.predict(features))
print("Accuracy: %f" % score)