#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('parsedpacketdata',sep='\s+',header=None)
data = pd.DataFrame(data)
x = data[0]
y = data[1]

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.set_title("Packet reception timestamps")    
ax1.set_xlabel('time')
ax1.set_ylabel('port')

ax1.plot(x,y, 'ro', label='PRI0')

leg = ax1.legend()

plt.show()