from ast import For
import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Target error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a= 1.0
    b= 1.0/math.sqrt(2)
    t= 0.25
    p= 1.0
    
    iterations = 5
    for i in range(iterations):
        a_next = (a + b) / 2
        b_next = math.sqrt(a * b)
        t_next = t - p * (a - a_next) ** 2
        p_next = 2 * p

        a, b, t, p = a_next, b_next, t_next, p_next
    pi_approximation = (a + b) ** 2 / (4 * t)
    return pi_approximation
    ### END OF YOUR CODE ###

desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)
error = abs(math.pi - approximation)

if error < abs(desired_error):
     print("Solution is acceptable")
else:
    print("Solution is not acceptable")