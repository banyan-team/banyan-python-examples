"""
Code in this file was taken from https://waterprogramming.wordpress.com/2014/09/25/introduction-to-mpi4py/
"""

from stockflow import simulation
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD

# Model setup - linear reservoir
tmin = 0
tmax = 365
dt = 1
t = np.arange(tmin, tmax, dt)

data = np.loadtxt("/home/ec2-user/leaf-river-data.txt", skiprows=2)
data_P = data[tmin:tmax, 0]
data_PET = data[tmin:tmax, 1]
data_Q = data[tmin:tmax, 2]

s = simulation(t)
s.stocks({"S": 0})

k = (comm.rank + 1) / comm.size

# Flows: precip, ET, and streamflow
s.flow(
    "P",
    start=None,
    end="S",
    f=lambda t: data_P[int(t)] if isinstance(t, float) else data_P[t],
)
s.flow(
    "ET",
    start="S",
    end=None,
    f=lambda t: min(data_PET[int(t)] if isinstance(t, float) else data_PET[t], s.S),
)
s.flow("Q", start="S", end=None, f=lambda t: k * s.S)
s.run()

RMSE = np.sqrt(np.mean((s.Q - data_Q) ** 2))
comm.Barrier()

Qs = comm.gather(s.Q, root=0)
RMSEs = comm.gather(RMSE, root=0)
ks = comm.gather(k, root=0)

if comm.rank == 0:
    best = np.argmin(RMSEs)
    worst = np.argmax(RMSEs)
    print(f"best k = {ks[best]}")
    print(f"best rmse = {RMSEs[best]}")
    print(f"worst k = {ks[worst]}")
    print(f"worst rmse = {RMSEs[worst]}")
