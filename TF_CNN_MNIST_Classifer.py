# Trains hand-written digit classifier on MNIST data

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

mnist = input_data.read_data_sets(".", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])

x_image = tf.reshape(x, [-1, 28, 28, 1])

# Layers:
#   First Layer
#       Filter bank
W_conv1 = tf.Variable(tf.truncated_normal([5,5,1,32], stddev = .1))
b_conv1 = tf.Variable(tf.constant(.1, shape = [32]))
h_conv1 =  tf.nn.relu(tf.nn.conv2d(x_image, W_conv1, strides = [1,1,1,1], padding = 'SAME') + b_conv1)
h_pool1 = tf.nn.max_pool(h_conv1, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')

#   Second Layer
W_conv2 = tf.Variable(tf.truncated_normal([5,5,32,64], stddev = .1))
b_conv2 = tf.Variable(tf.constant(.1, shape = [64]))
h_conv2 =  tf.nn.relu(tf.nn.conv2d(h_pool1, W_conv2, strides = [1,1,1,1], padding = 'SAME') + b_conv2)
h_pool2 = tf.nn.max_pool(h_conv2, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')

#   Fully Connected Layer
W_fc1 = tf.Variable(tf.truncated_normal([7*7*64, 1024], stddev = 0.1))
b_fc1 = tf.Variable(tf.constant(.1, shape = [1024]))
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

#   Output Layer and Dropout
W_fc2 = tf.Variable(tf.truncated_normal([1024, 10], stddev = .1))
b_fc2 = tf.Variable(tf.constant(.1, shape = [10]))
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

# Training and Testing
#   Cost function:
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = y_, logits = y_conv))
#   Learning algorithm:
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
yHat = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(yHat, tf.float32))

# Start session:
sess = tf.InteractiveSession()

sess.run(tf.global_variables_initializer())
numIterations = 20000
for i in range(numIterations):
    batch = mnist.train.next_batch(50)
    if i%100 ==0:
        train_accuracy = accuracy.eval(feed_dict = {x:batch[0], y_: batch[1], keep_prob: 1.0})
        print("Step %d training accuracy %g"%(i, train_accuracy))
    train_step.run(feed_dict = {x: batch[0], y_: batch[1], keep_prob: .5})

print("Test accuracy %g"%accuracy.eval(feed_dict = {x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
# Test accuracy 0.993
