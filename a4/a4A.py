import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

# 定义两类点
Class1 = np.array([[1, 1], [1, 2], [2, 1]])
Class2 = np.array([[0, 0], [1, 0], [0, 1]])

# 将两类点合并到一个数组中，并添加一个维度来表示类别标签
X = np.vstack((Class1, Class2))
y = np.array([1, 1, 1, -1, -1, -1])  # Class1为1，Class2为-1

# 创建SVM模型并训练
clf = svm.SVC(kernel='linear')
clf.fit(X, y)

# 获取分离线的支持向量
support_vectors = clf.support_vectors_

# 绘制数据点和支持向量
plt.scatter(Class1[:, 0], Class1[:, 1], color='blue', label='Class1')
plt.scatter(Class2[:, 0], Class2[:, 1], color='red', label='Class2')
plt.scatter(support_vectors[:, 0], support_vectors[:, 1], s=100, facecolors='none', edgecolors='k', label='Support Vectors')

# 绘制最佳分离线
w = clf.coef_[0]
b = clf.intercept_[0]
x = np.linspace(-1, 3)
y = -w[0]/w[1] * x - b/w[1]
plt.plot(x, y, color='k', label='Decision Boundary')

# 添加图例
plt.legend()

# 显示图形
plt.show()