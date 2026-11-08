from main import df
import newtwork_profiling

import numpy as np

# Compare Efficiency_Status across network quality bands

df['Efficiency_Status'] = np.where(df['Efficiency'] < 0.5, 'Low', 
                                    np.where(df['Efficiency'] < 0.8, 'Medium', 'High'))

# check the quantity of low, medium, and high efficiency statuses within each network quality band
