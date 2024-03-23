from timeit import default_timer as timer
import py_pwp as pwp
import py_pwp_utils as utils

utils.plot_forcings(fname='forcing.nc',name_fig='forcings.png')

start = timer()
my_model = pwp.py_mpwp_model()
my_model.run()
end = timer()
print('time={:g}'.format(end - start))

utils.plot_TS_section(fname='output.nc',name_fig='section.png')

utils.extract_state(fname='output.nc',name_state_file='final_state.nc',niter=-1)
utils.plot_state(fname='output.nc',name_fig='profile_TS.png',niter=-1)