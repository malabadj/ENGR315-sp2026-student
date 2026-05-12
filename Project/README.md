# Healthcare Obesity Data Analysis Program

## Project Overview

This Python program analyzes healthcare and obesity-related datasets using several different statistical and graphical methods. The program parses CSV healthcare data, organizes it into multiple storage structures, and generates visualizations to help identify obesity trends and relationships between lifestyle factors and obesity rates.

The project combines three separate analysis programs into one cohesive application.

---

# Main Features

## Included Analyses

- Obesity rates by demographic group
- National obesity trends over time
- Correlation analysis between obesity and:
    - Physical inactivity
    - Dietary habits / fruit consumption
- Automatic graph generation using matplotlib
- Statistical calculations including:
    - averages
    - correlation coefficients
    - trendlines / linear regression

---

# Required Libraries

The following Python libraries are required:

```python
import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt