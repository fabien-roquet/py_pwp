import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import xarray as xr
import os


###############################################
##       plot section of state               ##
###############################################
def plot_TS_section(fname='output.nc',name_fig='section.png'):

    ds = xr.open_dataset(fname)
        
    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(16, 9), sharex=True)
    
    ds.si_thick.plot(ax=ax[0,0])
    ax[0,0].set_title('sea-ice thickness')

    (ds.si_conc*100).plot(ax=ax[0,1])
    ax[0,1].set_title('sea-ice concentration')

    ds.theta.isel(depth=0).plot(ax=ax[1,1])
    ax[1,1].set_title('sea surface temperature')

    ds.salt.isel(depth=0).plot(ax=ax[2,1])
    ax[2,1].set_title('sea surface salinity')

    ds.theta.T.plot(ax=ax[1,0],ylim=[200,-10])
    ds.ml_depth.plot(ax=ax[1,0],color='k')
    ax[1,0].set_title('temperature')
    
    ds.salt.T.plot(ax=ax[2,0],ylim=[200,-10])
    ds.ml_depth.plot(ax=ax[2,0],color='k')
    ax[2,0].set_title('salinity')
    ax[2,0].set_xlabel('time [days]')

    plt.savefig(name_fig)




###############################################
##       plot state at a given time          ##
###############################################
def plot_state(fname='output.nc',name_fig='profile_TS.png',niter=-1):

    ds = xr.open_dataset(fname)
    state = ds.isel(time=niter)

    min_temp   = state.theta.min()
    max_temp   = state.theta.max()
    min_salt   = state.salt.min()
    max_salt   = state.salt.max()
    max_depth  = state.depth.max()
    si_thick   = state.si_thick
    si_conc    = state.si_conc
    ml_index   = int(state.ml_index)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 9), sharey=True)
    plt.gca().set_ylim([-40,max_depth+10])
    plt.gca().invert_yaxis()

    ax1.plot(state.theta,state.depth)
    ax1.set_title('temperature')
    ax1.plot(state.theta[ml_index],state.depth[ml_index], color='r', linestyle='none', marker='o')
    ax1.add_patch(patches.Rectangle((min_temp, -si_thick*10), max_temp-min_temp, si_thick*10))
    ax1.annotate('sea ice: {:5.2f}m, {:4.1f}%'.format(si_thick,si_conc*100), 
                 xy=(min_temp, -20),  
                 xycoords='data')

    ax2.plot(state.salt,state.depth)
    ax2.set_title('salinity')
    ax2.plot(state.salt[ml_index],state.depth[ml_index], color='r', linestyle='none', marker='o')
    ax2.add_patch(
        patches.Rectangle((min_salt, -si_thick*10), max_salt-min_salt, si_thick*10))

    plt.savefig(name_fig)


###############################################
##       plot state at a given time          ##
###############################################
def extract_state(fname='output.nc',name_state_file='state.nc',niter=0):

    ds = xr.open_dataset(fname)
    state = ds.isel(time=niter)
    if os.path.isfile(name_state_file): os.remove(name_state_file)
    state.to_netcdf(name_state_file)

    
###############################################
##  diagnostic plots (to add to)/modularize  ##
###############################################
def plot_forcings(fname='output_forcing.nc',name_fig='forcing.png'):

    ds = xr.open_dataset(fname)    
    
    # print(OLR_ice, ILR_ice, ISW_ice, i_sens, i_lat, T_si)
    fig = plt.figure(figsize=(9, 9))
    
    ax1 = fig.add_subplot(421)
    ds.lw.plot(ax=ax1)
    plt.xlabel('')

    ax2 = fig.add_subplot(422)
    ds.sw.plot(ax=ax2)
    plt.xlabel('')

    ax3 = fig.add_subplot(423)
    ds.T_a.plot(ax=ax3)
    plt.ylabel('Tair')
    
    ax4 = fig.add_subplot(424)
    ds.U_a.plot(ax=ax4)
    plt.xlabel('time')
    plt.ylabel('Uair')

    ax5 = fig.add_subplot(425)
    ds.tx.plot(ax=ax5)

    ax6 = fig.add_subplot(426)
    ds.ty.plot(ax=ax6)

    ax7 = fig.add_subplot(427)
    ds.shum.plot(ax=ax7)
    plt.xlabel('time')

    ax8 = fig.add_subplot(428)
    ds.precip.plot(ax=ax8)
    plt.xlabel('time')

    plt.savefig(name_fig)

