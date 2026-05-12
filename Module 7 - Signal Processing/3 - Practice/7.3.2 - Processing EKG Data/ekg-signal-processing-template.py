import matplotlib.pyplot as plt
import numpy as np

"""
Step 0: Select which database you wish to use.
"""

# database name
database_name = 'mitdb_201'

# path to ekg folder
path_to_folder = "../../../data/ekg/"

# select a signal file to run
signal_filepath = path_to_folder + database_name + ".csv"

"""
Step #1: load data in matrix from CSV file; skip first two rows. Name the returned matrix 'signal'
"""

signal = 0
## YOUR CODE HERE ##
signal = np.loadtxt(signal_filepath, delimiter=',', skiprows=2)


"""
Step 2: (OPTIONAL) pass data through LOW PASS FILTER
"""

"""
Step 3: Pass data through differentiator. Optional to make it weighted.
"""
## implement differentiator, utilizing the slope of the signal.
np.diff(signal)

"""
Step 4: Square the results of the previous step
"""
 ## square the results
signal = signal ** 2


"""
Step 5: Pass a moving average over your data
"""
# implement moving average, using a for loop to iterate through the signal and average over a window
window_size = 5
moving_average_signal = np.zeros(len(signal) - window_size + 1)
for i in range(len(moving_average_signal)):
    moving_average_signal[i] = np.mean(signal[i:i + window_size])


## YOUR CODE HERE
# make a plot of the results. Can change the plot() parameter below to show different intermediate signals
plt.figure(figsize=(10, 5))
plt.plot(moving_average_signal)
plt.title('EKG Signal for ' + database_name)
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()