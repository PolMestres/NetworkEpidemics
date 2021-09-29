This repository includes code to simulate and visualize the spread of an stochastic SIR epidemic in a network with different preventive strategies.

**quar.py**

This script simulates an stochastic SIR model in which infected nodes independently have a chance to quarantine at every iteration
they are infected by dropping all connections to its neighboring nodes.
Nodes are displayed in different colors depending on whether they are susceptible (green), infected (red) or recovered (blue).


![](simulated-image.png)
