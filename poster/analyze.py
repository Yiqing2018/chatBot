import matplotlib.pyplot as plt
# y_data = [0.46672, 0.460355, 0.47348, 0.43628,0.47649]
# x_data = ['1,000','10,000','100,000','1000,000','fulldata']
# x_scale = range(len(y_data))

# plt.figure(figsize=(20,4))
# l1=plt.plot(x_scale,y_data,'b--', label = "epoches = 3")


# plt.xticks(x_scale, x_data)

# plt.title('similarity score on different data size')
# plt.xlabel('data size')
# plt.ylabel('score')
# plt.legend()
# plt.show()

# y_data = [39.2, 46.6, 64.2, 312.8,207.7, 3126.1]
# x_data = ['1,000','10,000','100,000','1000,000','fulldata']
# x_scale = range(len(y_data))

# plt.figure(figsize=(20,4))
# l1=plt.plot(x_scale,y_data,'g--', label = "epoches = 3")


# plt.xticks(x_scale, x_data)

# plt.title('running time on different data size')
# plt.xlabel('data size')
# plt.ylabel('running time(seconds)')
# plt.legend()
# plt.show()

y_data = [39.2, 46.6, 64.2, 312.8,207.7, 3126.1]
x_data = ['1,000','10,000','100,000','1000,000','fulldata']
x_scale = range(len(y_data))

plt.figure(figsize=(20,4))
l1=plt.plot(x_scale,y_data,'g--', label = "epoches = 3")


plt.xticks(x_scale, x_data)

plt.title('running time on different data size')
plt.xlabel('data size')
plt.ylabel('running time(seconds)')
plt.legend()
plt.show()