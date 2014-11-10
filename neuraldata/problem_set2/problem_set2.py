#
#  NAME
#    problem_set2_solutions.py
#
#  DESCRIPTION
#    Open, view, and analyze action potentials recorded during a behavioral
#    task.  In Problem Set 2, you will write create and test your own code to
#    create tuning curves.
#

#Helper code to import some functions we will use
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as mlab
from scipy import optimize
from scipy import stats

def load_experiment(filename):
    """
    load_experiment takes the file name and reads in the data.  It returns a
    two-dimensional array, with the first column containing the direction of
    motion for the trial, and the second column giving you the time the
    animal began movement during thaht trial.
    """
    data = np.load(filename)[()];
    return np.array(data)

def load_neuraldata(filename):
    """
    load_neuraldata takes the file name and reads in the data for that neuron.
    It returns an arary of spike times.
    """
    data = np.load(filename)[()];
    return np.array(data)
    
    
def bin_spikes(trials, spk_times, time_bin):
    """
    bin_spikes takes the trials array (with directions and times) and the spk_times
    array with spike times and returns the average firing rate for each of the
    eight directions of motion, as calculated within a time_bin before and after
    the trial time (time_bin should be given in seconds).  For example,
    time_bin = .1 will count the spikes from 100ms before to 100ms after the 
    trial began.
    
    dir_rates should be an 8x2 array with the first column containing the directions
    (in degrees from 0-360) and the second column containing the average firing rate
    for each direction
    """
    
# Generate array [number_of_unique_directions x 2]
# With the first col = unique_directions,second col = zeros
    dir_rates = np.zeros((len(np.unique(trials[:, 0])), 2))
    np.put(dir_rates, range(0, len(dir_rates)*2, 2), np.unique(trials[:, 0]))

    association_ratio = [0, 0, 0] # Performance counters for monitoring
    
    for t in spk_times:
        associated = False # Flag used to control overlapping and performance
        
        for d, tt in trials[:]:
            if t >= (tt - time_bin) and t <= (tt + time_bin):
#                print "There was spike in direction %s at time: %s" % (d, t)

    # Control overlapping and record for monitoring
                if associated:
                    association_ratio[2] += 1
                associated = True

# Record the result to col 2 of dir_rates
                index = np.where(dir_rates[:,0] == d)
                dir_rates[index,1] += 1
#                print "For %s found index %s" % (d, index[0][0])

# Update association_ratio. Used for performance monitoring.
        if not associated:
#            print "Spike was not associated with training set at: %s" % t
            association_ratio[1] += 1
        else:
            association_ratio[0] += 1

# Careful! We update array on the go.
# FIXME! Hardcoded number of trains!!!  =17
    for i, v in enumerate(dir_rates[:,1]):
        dir_rates[i,1] = ( v / (time_bin * 2 * 17) )
    
#==============================================================================
# This was a check, because exactly 17 tries in each direction seemed strange
#     tmp = {0:0, 45:0, 90:0, 135:0, 180:0, 225:0, 270:0, 315:0}
#     for i in trials[:,0]:
#         tmp[i] = tmp[i] + 1
#     print tmp
#==============================================================================
      
    print "The association ratio is %s%%" % (float(association_ratio[0]) /
                                            sum(association_ratio) * 100)
    print "Overlapping was %s times" % association_ratio[2]

    return dir_rates
    
def plot_tuning_curves(direction_rates, title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates) and plots a histogram and 
    polar representation of the tuning curve. It adds the given title.
    """

    
def roll_axes(direction_rates):
    """
    roll_axes takes the x-values (directions) and y-values (direction_rates)
    and return new x and y values that have been "rolled" to put the maximum
    direction_rate in the center of the curve. The first and last y-value in the
    returned list should be set to be the same. (See problem set directions)
    Hint: Use np.roll()
    """
   
    
    return new_xs, new_ys, roll_degrees    
    

def normal_fit(x,mu, sigma, A):
    """
    This creates a normal curve over the values in x with mean mu and
    variance sigma.  It is scaled up to height A.
    """
    n = A*mlab.normpdf(x,mu,sigma)
    return n

def fit_tuning_curve(centered_x,centered_y):
    """
    This takes our rolled curve, generates the guesses for the fit function,
    and runs the fit.  It returns the parameters to generate the curve.
    """

    return p
    


def plot_fits(direction_rates,fit_curve,title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates and fit_curve) and plots the 
    actual values with circles, and the curves as lines in both linear and 
    polar plots.
    """
    

def von_mises_fitfunc(x, A, kappa, l, s):
    """
    This creates a scaled Von Mises distrubition.
    """
    return A*stats.vonmises.pdf(x, kappa, loc=l, scale=s)


    
def preferred_direction(fit_curve):
    """
    The function takes a 2-dimensional array with the x-values of the fit curve
    in the first column and the y-values of the fit curve in the second.  
    It returns the preferred direction of the neuron (in degrees).
    """
  
    return pd
    
        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    trials = load_experiment('trials.npy')   
    spk_times = load_neuraldata('example_spikes.npy')

 
    print bin_spikes(trials, spk_times[:10000], 0.1) # the last 1/3 cut off

#    print len(trials)
#    print len(spk_times)
    
#    print trials[:,0]

#    print trials
#    print spk_times[:500]
#    plt.hist(spk_times[:500], 20)
