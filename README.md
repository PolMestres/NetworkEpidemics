This repository includes code to simulate and visualize the spread of an stochastic SIR epidemic in a network with different preventive strategies.

**quar.py**

This script simulates an stochastic SIR model in which infected nodes independently have a chance to quarantine at every iteration
they are infected by dropping all connections to its neighboring nodes.
Nodes are displayed in different colors depending on whether they are susceptible (green), infected (red) or recovered (blue).

<img width="1316" alt="simulation-image" src="https://user-images.githubusercontent.com/31922605/135208889-dab9eb17-a002-418d-a33c-35ee9f3ccfb0.png">

**twographs.py**

Central locations (yellow nodes) are added and every node connects to it with a certain probability at every iteration

<img width="1144" alt="simulation-image2" src="https://user-images.githubusercontent.com/31922605/135209115-0d497e77-b95a-489e-91b4-e10b21807bc5.png">
