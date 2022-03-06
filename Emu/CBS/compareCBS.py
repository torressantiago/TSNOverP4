#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

plt.rc('font',family='CMU Serif')



# -- Comparison data --
# Parse extracted data
data = json.load(open('packetdata_10concurrent.json'))
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

fig, ax = plt.subplots()
ax.plot(t,y,'o--',label='Measured throughput PRI0, concurrent streams=10')
ax.set_ylim([0, np.amax(y)])

# -- Sent Data --
data = json.load(open('sendoutput_20concurrentpri1.json'))
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


ax.plot(trec,y_rec,'o--',label='Measured throughput PRI1, concurrent streams=20')

# -- Received data --
# Parse extracted data
data = json.load(open('packetdata_20concurrent.json'))
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


ax.plot(t,y,'o--',label='Measured throughput PRI0, concurrent streams=20')
ax.set_ylim([0, np.amax(y)])

ax.legend()
ax.grid(True)
plt.ylabel('Received data [bits]',fontname="CMU Serif")
plt.xlabel('Time [s]',fontname="CMU Serif")
plt.title('Measured throughput (CBS)',fontname="CMU Serif")
plt.show()