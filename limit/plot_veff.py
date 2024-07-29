import numpy as np
import matplotlib.pyplot as plt
import scipy

from rnog import veff
import rnog as rnog

smt_veff = veff["SMT"]["veff"]
pa_veff = veff["PA"]["veff"]
energy = veff["SMT"]["energy"]

energy_ara = rnog.data_ara_200["arasim"]["energy"]
veff_ara = rnog.data_ara_200["arasim"]["veff"]


fig, ax = plt.subplots(1,1)
ax.plot(energy, pa_veff, label="RNO-G 2 sigma 100m (RNO-G White Paper)")
ax.plot(energy, smt_veff, label="RNO-G 2/4 100m (Martin)")
ax.plot(energy_ara, veff_ara, label="ARA 200m 3/8 (A23 Diffuse Paper)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.legend()
fig.savefig("veff.png")
