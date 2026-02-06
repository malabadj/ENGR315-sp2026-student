"""
For investments over $1M it can be typically assumed that they will return 5% forever.
Using the [2022 - 2023 JMU Cost of Attendance](https://www.jmu.edu/financialaid/learn/cost-of-attendance-undergrad.shtml),
calculate how much a rich alumnus would have to give to pay for one full year (all costs) for an in-state student
and an out-of-state student. Store your final answer in the variables: "in_state_gift" and "out_state_gift".

JMU 2022-2023 Annual:
In-state total cost: 30792 USD
Out-of-state total cost: 47882 USD

Note: this problem does not require the "compounding interest" formula from the previous problem.

"""

### Your code here ###
in_state_cost = 30792  # cost for one year for in-state student
out_state_cost = 47882  # cost for one year for out-of-state student

# relationship: cost = gift * 0.05
# formula used: gift = cost / 0.05

<<<<<<< Updated upstream
out_state_gift = 0
=======
in_state_gift = in_state_cost / 0.05

out_state_gift = out_state_cost / 0.05

print(in_state_gift)
print(out_state_gift)
>>>>>>> Stashed changes
