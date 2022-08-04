"""Plotting
Used for debugging and compairson of data.

Functions
---------
An easy way to visualize output.

Author
---------
Mason Becker
"""

import matplotlib.pyplot as plt

def channel_plot(data, channel):
    plt.plot(data[channel])
    plt.title('Data (Channel ' + str(channel)+ ')')
    plt.ylim(-500, 500)
    plt.savefig('Output/Out.png')
    plt.close()
