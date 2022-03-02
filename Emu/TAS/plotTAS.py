#!/usr/bin/python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import *

plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
plt.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
plt.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'


# Interpreting received data
data = pd.read_csv('../parsedpacketdata',sep='\s+',header=None)
data = pd.DataFrame(data)

x = data[0]
x = x.values.tolist()

date_time = seconds = x

for i in range(len(x)):
    date_time[i] = datetime.strptime(x[i], "%H:%M:%S.%f")
    a_timedelta = date_time[i] - datetime(1900, 1, 1)
    seconds[i] = a_timedelta.total_seconds()

y = data[1]

seconds = np.array(seconds)-seconds[0]
port = y.to_numpy()

normport1 = (port-6666)/1111
normport2 = -(port-7777)/1111

print(seconds)
print(port)

fig, (ax1,ax2) = plt.subplots(2)

ax1.set_title("Packet reception timestamps (TAS)")    
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Packet Arrival')

ax1.stem(seconds,normport1, 'C1-', label='PRI0',markerfmt='C1D')
ax1.stem(seconds,normport2, 'C0-', label='PRI1',markerfmt='C0o')

ax1.set_xlim([0, 0.2])

leg = ax1.legend()

# plt.show()

# Interpreting sent data
data = pd.read_csv('../parsedsenderoutput',sep='\s+',header=None)
data = pd.DataFrame(data)

x = data[1]
x = x.values.tolist()

date_time = seconds = x

for i in range(len(x)):
    date_time[i] = datetime.strptime(x[i], "%H:%M:%S.%f")
    a_timedelta = date_time[i] - datetime(1900, 1, 1)
    seconds[i] = a_timedelta.total_seconds()

y = data[0]

seconds = np.array(seconds)-seconds[0]
port = y.to_numpy()

normport1 = (port-6666)/1111
normport2 = -(port-7777)/1111

print(seconds)
print(port)

ax2.set_title("Packet emition timestamps (for TAS)")    
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Packet emition')

ax2.stem(seconds,normport1, 'C1-', label='PRI0',markerfmt='C1D')
ax2.stem(seconds,normport2, 'C0-', label='PRI1',markerfmt='C0o')

ax2.set_xlim([0, 0.2])

leg = ax2.legend()

plt.show()
