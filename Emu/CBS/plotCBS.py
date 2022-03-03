#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

# -- Sent data --
data = json.load(open('sendoutput.json'))
df = pd.DataFrame(data["intervals"])

exchangedData = df['sum'].apply(pd.Series)

# Obtain values of time
trec = exchangedData[['start']].to_numpy()
# Obtain values of bit rate
bytescaptrec = exchangedData[['bytes']].to_numpy()
secondsmeasrec = exchangedData[['seconds']].to_numpy()

bitr_rec = (bytescaptrec*8)/secondsmeasrec

ylast_rec = 0
y_rec = np.zeros((len(trec),1))

for i in range(len(trec)):
	y_rec[i] = trec[i]*bitr_rec[i]+ylast_rec
	ylast_rec = y_rec[i]

# -- Received data --
# Parse extracted data
data = json.load(open('packetdata.json'))
datan = data[0]
df = pd.DataFrame(datan["intervals"])

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


plt.plot(t,y,'o--',label='Received throughput')
plt.plot(trec,y_rec,'o--',label='Sent throughput')
plt.legend()
plt.ylabel('Data received [bits]',fontname="CMU Serif")
plt.xlabel('Time [seconds]',fontname="CMU Serif")
plt.title('Measured throughput (CBS)',fontname="CMU Serif")
plt.show()