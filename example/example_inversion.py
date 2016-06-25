#!/usr/bin/env python
import numpy as np
import cosinv.patch
from cosinv.gbuild import flatten_vector_array
from cosinv.gbuild import build_system_matrix
import matplotlib.pyplot as plt
import scipy.optimize

def build_reg_matrix(Ps,slip_direction):
G = cosinv.gbuild.build_system_matrix(obs_ext,Ps_ext,synth_dir,slip_dir)


def reg_nnls(G,L,d):
  dext = np.concatenate((d,np.zeros(L.shape[0])))
  Gext = np.vstack((G,L))
  return scipy.optimize.nnls(Gext,dext)[0]
  
### patch specifications
#####################################################################
strike = 20.0 # degrees
dip = 80.0 # degrees
length = 5.0
width = 5.0
pos = [0.0,0.0,0.0] # top center of patch
Nl = 10
Nw = 10

## observation points
#####################################################################
Nx = 100
obs = np.random.uniform(-10,10,(Nx,3))
obs[:,2] = 0.0
#####################################################################


#####################################################################
### create synthetic slip
#####################################################################
Ds = 2
P = cosinv.patch.Patch(pos,length,width,strike,dip)
Ps = np.array(P.discretize(Nl,Nw))
slip = np.zeros((Nl*Nw,Ds))
slip[:,0] = 1.0

### create synthetic displacements
#####################################################################
synth = np.zeros((Nx,3))
for i,p in enumerate(Ps):
  out = cosinv.okada.patch_dislocation(obs,slip[i],p)
  synth += out[0]
  
#synth += np.random.normal(0.0,1.0,synth.shape)

### format the data and slip 
synth_val,synth_dir,obs_ext = flatten_vector_array(synth,obs)

slip_val,slip_dir,Ps_ext = flatten_vector_array(slip,Ps)
G = cosinv.gbuild.build_system_matrix(obs_ext,Ps_ext,synth_dir,slip_dir)
L = 0.001*np.eye(len(Ps_ext))
L = rbf.fd.diff_matrix([i.pos for i in Ps_ext]
soln = reg_nnls(G,L,synth_val)
#soln = scipy.optimize.nnls(G,synth_val)[0]
soln = soln.reshape((-1,3))
print(G.shape)

### plot synthetic
fig,ax = plt.subplots()
ax.set_title('ll')
ax.set_xlim((-10,10))
ax.set_ylim((-10,10))
ax.quiver(obs[:,0],obs[:,1],synth[:,0],synth[:,1])
pc = cosinv.patch.draw_patches(Ps,ax=ax,zorder=0,colors=soln[:,0],edgecolor='none')
fig.colorbar(pc,ax=ax)

fig,ax = plt.subplots()
ax.set_title('thust')
ax.set_xlim((-10,10))
ax.set_ylim((-10,10))
ax.quiver(obs[:,0],obs[:,1],synth[:,0],synth[:,1])
pc = cosinv.patch.draw_patches(Ps,ax=ax,zorder=0,colors=soln[:,1],edgecolor='none')
fig.colorbar(pc,ax=ax)

fig,ax = plt.subplots()
ax.set_title('tensile')
ax.set_xlim((-10,10))
ax.set_ylim((-10,10))
ax.quiver(obs[:,0],obs[:,1],synth[:,0],synth[:,1])
pc = cosinv.patch.draw_patches(Ps,ax=ax,zorder=0,colors=soln[:,2],edgecolor='none')
fig.colorbar(pc,ax=ax)
plt.show()


