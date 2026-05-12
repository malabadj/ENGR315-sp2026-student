
import matplotlib.pyplot as plt
import numpy as np

# import the CSV file using numpy
path = '../../../data/ekg/mitdb_201.csv'

# load data in matrix from CSV file; skip first two rows; set a comma as the delimiter

### Your code here ###
data = np.loadtxt(path, delimiter=',', skiprows=2)

# save each vector as own variable

### Your code here ###
elapsed_time = data[:, 0]
MVII = data[:, 1]

# use matplot lib to generate a single
plt.figure(figsize=(10, 5))

### Your code here ###
plt.plot(elapsed_time, MVII)
plt.title('EKG Signal for ' + path)
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()