#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

# Parse extracted data
data = json.load(open('sendoutput.json'))
df = pd.DataFrame(data["intervals"])

exchangedData = df['sum'].apply(pd.Series)

# Obtain values of time
t = exchangedData[['start']].to_numpy()
# Obtain values of bit rate
bytescapt = exchangedData[['bytes']].to_numpy()
secondsmeas = exchangedData[['seconds']].to_numpy()

bitr = (bytescapt*8)/secondsmeas

ylast = 0
y = np.zeros((len(t),1))

for i in range(len(t)):
	y[i] = t[i]*bitr[i]+ylast
	ylast = y[i]


plt.plot(t,y)
plt.ylabel('Data received [bits]',fontname="CMU Serif")
plt.xlabel('Time [seconds]',fontname="CMU Serif")
plt.title('Measured throughput (CBS)',fontname="CMU Serif")
plt.show()