# Introduction
The goal of this project is the creation of a software switch that allows reconfigurable deployments for time constrained networks. The norm implemented for this project is TSN and most specifically the latency management aspects found in 802.1Qav (Credit Based Shaper) and 802.Qbv (Time Aware Shaper). The first one works on a credit basis where it can only send the quantity of bits it has in terms of credits. The second one works on a time basis and divided schedules the traffic according to time slotted, time triggered events. 

# P4 implementation
As a first approach, P4 was chosen for the implementation of such a software switch. The language allows to port the same behavioral model to many different architectures. In order to do that it uses a switch model, where the most popular and the one that is most supported is the v1model. 

![test](https://wiki.geant.org/download/attachments/148079103/V1model.png?version=1&modificationDate=1590399738625&api=v2)

According to P4's documentation, the traffic manager is something static and specific to the target. Hence, in order to implement a software switch using this model an extra layer must be added on top of P4 to add the QoS features this project aims to implement. Nevertheless, implementing this feature goes out of the scope of the project (particularly due to time constraints). To solve this issue, the tc linux package was chosen as an approximation to the missing layer. It is said to be an approximation since it runs over the Linux Kernel, therefore, there's no guarantee of time constrained mechanisms, but most importantly it will be a solution that can only run on software switch solutions such as [DPDK](https://www.dpdk.org/) or [OpenVSwitch](http://www.openvswitch.org/). 

In the Wiki pages below, you'll find application notes on how to create test beds for TSN by creating a software switch in P4 and then on how to deploy switching techniques on a Linux-run software switch.

* [P4 application note](https://github.com/torressantiago/TSNOverP4/wiki/P4-TSN-oriented-switch-design-application-note) 
* [tc application note](https://github.com/torressantiago/TSNOverP4/wiki/TC-for-TSN-application-note)
