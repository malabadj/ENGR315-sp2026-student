import sys

import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
path_to_datafile = r"C:\Users\danie\Documents\GitHub\ENGR315-sp2026-student\data\drop-jump\all_participant_data_rsi.csv"

### YOUR CODE HERE
## open the csv file from data path and load it into a pandas dataframe
try:
    df = pd.read_csv(path_to_datafile)
except FileNotFoundError:
    print(f'File {path_to_datafile} not found. Exiting!')
    sys.exit(-1)


"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

### YOUR CODE HERE
## load all data sets for force plate and acceleration based RSI into separate variables
accel_rsi = df['accelerometer_rsi'].values
force_plate_rsi = df['force_plate_rsi'].values

## fit normal distribution to each data set
accel_mu, accel_std = norm.fit(accel_rsi)
force_plate_mu, force_plate_std = norm.fit(force_plate_rsi)

## print distribution parameters
print(f'Acceleration RSI: mu={accel_mu:.2f}, std={accel_std:.2f}')
print(f'Force Plate RSI: mu={force_plate_mu:.2f}, std={force_plate_std:.2f}')

## generate x values for plotting the PDFs
x_accel = np.linspace(min(accel_rsi), max(accel_rsi), 100)
x_force_plate = np.linspace(min(force_plate_rsi), max(force_plate_rsi), 100)

## calculate the PDFs
accel_pdf = norm.pdf(x_accel, loc=accel_mu, scale=accel_std)
force_plate_pdf = norm.pdf(x_force_plate, loc=force_plate_mu, scale=force_plate_std)

## plot the PDFs
plt.figure(figsize=(10, 6))
plt.plot(x_accel, accel_pdf, label='Acceleration RSI PDF', color='blue')
plt.plot(x_force_plate, force_plate_pdf, label='Force Plate RSI PDF', color='orange')
plt.hist(accel_rsi, bins=16, density=True, alpha=0.5, color='blue', label='Acceleration RSI Data')
plt.hist(force_plate_rsi, bins=16, density=True, alpha=0.5, color='orange', label='Force Plate RSI Data')
plt.title('Probability Distribution Functions for RSI Data')
plt.xlabel('RSI Value')
plt.ylabel('Density')
plt.legend()
plt.grid()
plt.show()


"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), add append -inf and +inf to both ends of the bins. An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

"""
Acceleration
"""
### YOUR CODE HERE

## generate bins for chi2 test
bins = np.linspace(0, 2, 10)  # 9 bins between [0, 2)
bins = np.concatenate(([-np.inf], bins, [np.inf]))  # add -inf and +inf to the ends

## calculate observed frequencies for acceleration data
accel_observed_freq, _ = np.histogram(accel_rsi, bins=bins)

## calculate expected frequencies for acceleration data using the fitted normal distribution
accel_expected_freq = len(accel_rsi) * (norm.cdf(bins[1:], loc=accel_mu, scale=accel_std) - norm.cdf(bins[:-1], loc=accel_mu, scale=accel_std))

## perform chi2 test for acceleration data
accel_chi2_stat, accel_p_value = chisquare(accel_observed_freq, f_exp=accel_expected_freq)

## print results for acceleration data
print(f'Acceleration RSI: chi2_stat={accel_chi2_stat:.2f}, p_value={accel_p_value:.4f}')
if accel_p_value < 0.05:
    print('Acceleration RSI data does NOT fit the normal distribution (reject H0)')
else:
    print('Acceleration RSI data fits the normal distribution (fail to reject H0)')


"""
Force Plate
"""
### YOUR CODE HERE

##follow the same steps as above for force plate data

## calculate observed frequencies for force plate data
force_plate_observed_freq, _ = np.histogram(force_plate_rsi, bins=bins)

## calculate expected frequencies for force plate data using the fitted normal distribution
force_plate_expected_freq = len(force_plate_rsi) * (norm.cdf(bins[1:], loc=force_plate_mu, scale=force_plate_std) - norm.cdf(bins[:-1], loc=force_plate_mu, scale=force_plate_std))

## perform chi2 test for force plate data
force_plate_chi2_stat, force_plate_p_value = chisquare(force_plate_observed_freq, f_exp=force_plate_expected_freq)

## print results for force plate data
print(f'Force Plate RSI: chi2_stat={force_plate_chi2_stat:.2f}, p_value={force_plate_p_value:.4f}')
if force_plate_p_value < 0.05:
    print('Force Plate RSI data does NOT fit the normal distribution (reject H0)')
else:
    print('Force Plate RSI data fits the normal distribution (fail to reject H0)')

"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

### YOUR CODE HERE
## perform independent t-test between acceleration and force plate RSI data
t_stat, p_value = ttest_ind(accel_rsi, force_plate_rsi)

## print results for t-test
print(f'T-test: t_stat={t_stat:.2f}, p_value={p_value:.4f}')
if p_value < 0.05:
    print('The means of the acceleration and force plate RSI data are NOT equivalent (reject H0)')
else:
    print('The means of the acceleration and force plate RSI data are equivalent (fail to reject H0)') 


"""
Question 4: Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""

### YOUR CODE HERE
## calculate RSI error as the difference between force plate and accelerometer RSI
rsi_error = force_plate_rsi - accel_rsi

## fit normal distribution to RSI error
error_mu, error_std = norm.fit(rsi_error)

## generate x values for plotting the PDF of the error distribution
x_error = np.linspace(min(rsi_error), max(rsi_error), 100)

## calculate the PDF of the error distribution
error_pdf = norm.pdf(x_error, loc=error_mu, scale=error_std)

## plot histogram of RSI error with fitted normal curve
plt.figure(figsize=(10, 6))
plt.hist(rsi_error, bins=16, density=True, alpha=0.5, color='purple', label='RSI Error Data')
plt.plot(x_error, error_pdf, label='Fitted Normal PDF', color='red')
plt.title('RSI Error Distribution with Fitted Normal Curve')
plt.xlabel('RSI Error (Force Plate RSI - Accelerometer RSI)')
plt.ylabel('Density')
plt.legend()
plt.grid()
plt.show()