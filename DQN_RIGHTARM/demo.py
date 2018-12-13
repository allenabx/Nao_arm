import numpy as np
import torch
import numpy

a = torch.ones(1)
print(a)
b = a.numpy()
print(b)
c=[]
c.append(b[0])
c.append(b[0])
c.append(b[0]+1)
c.append(b[0]+22)
c.append(b[0]+4)
c.append(b[0])
c.append(b[0])
c.append(b[0])
print(c)


import matplotlib.pyplot as plt

y=c  # 设置y轴数据，以数组形式提供

x=len(y)           # 设置x轴，以y轴数组长度为宽度
x=range(x)      # 以0开始的递增序列作为x轴数据

plt.plot(x,y)  #  只提供x轴，y轴参数，画最简单图形
plt.show()