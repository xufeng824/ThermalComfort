import tensorflow as tf
import numpy as np
import pandas as pd

tf.compat.v1.disable_eager_execution()

#数据准备
f = open('49_EXL.csv', encoding='utf-8')
c1 = f.readlines()
head = c1[4:6]
h1 = head[0].split(',')
h2 = head[1].split(',')
for i in range(len(h1)):
    if h1[i] == '':
        h1[i] = h2[i]
header = h1

data_set = pd.read_csv('49.csv', header=None, names=[i for i in header])

#训练集和测试集的划分
train_set = pd.read_csv('49.csv', nrows = 800, header=None, names=[i for i in header])
test_set = data_set.drop(i for i in range(800))
x_dat = np.array([i] for i in train_set['AGE'])
y_dat = np.array([j] for j in train_set['PMV'])

# 添加层
def add_layer(inputs, in_size, out_size, activation_function=None):
   # add one more layer and return the output of this layer
   Weights = tf.Variable(tf.compat.v1.random_normal([in_size, out_size]))
   biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
   Wx_plus_b = tf.matmul(inputs, Weights) + biases
   if activation_function is None:
       outputs = Wx_plus_b
   else:
       outputs = activation_function(Wx_plus_b)
   return outputs

# 1.训练的数据
# Make up some real data
x_data = x_dat
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

# 2.定义节点准备接收数据
# define placeholder for inputs to network
xs = tf.compat.v1.placeholder(tf.float32, [None, 1])
ys = tf.compat.v1.placeholder(tf.float32, [None, 1])

# 3.定义神经层：隐藏层和预测层
# add hidden layer 输入值是 xs，在隐藏层有 10 个神经元
l1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)
# add output layer 输入值是隐藏层 l1，在预测层输出 1 个结果
prediction = add_layer(l1, 10, 1, activation_function=None)

# 4.定义 loss 表达式
# the error between prediciton and real data
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),
                    axis=[1]))

# 5.选择 optimizer 使 loss 达到最小
# 这一行定义了用什么方式去减少 loss，学习率是 0.1
train_step = tf.compat.v1.train.GradientDescentOptimizer(0.1).minimize(loss)


# important step 对所有变量进行初始化
init = tf.compat.v1.initialize_all_variables()
sess = tf.compat.v1.Session()
# 上面定义的都没有运算，直到 sess.run 才会开始运算
sess.run(init)

# 迭代 1000 次学习，sess.run optimizer
for i in range(1000):
   # training train_step 和 loss 都是由 placeholder 定义的运算，所以这里要用 feed 传入参数
   sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
   if i % 50 == 0:
       # to see the step improvement
       print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
