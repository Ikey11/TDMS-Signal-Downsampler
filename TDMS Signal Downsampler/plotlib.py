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
from numpy import arange

# Bare bones plot of a channel
def channel_plot(data, channel):
    plt.plot(data[channel])
    plt.title('Data (Channel ' + str(channel)+ ')')
    plt.savefig('Output/Out.png')
    print("Figure Saved in Output/Out.png!")
    plt.show()
    plt.close()

# Offers the user an interactable side-by-side of the raw and decimated data using matplotlib
def interactable_compairson(raw, downsized, decimation):
    fig1, (ax1, ax2) = plt.subplots(2, 1)

    plot_1 = ax1.pcolor(downsized)
    ax1.set_title('Decimated Data by a factor of ' + str(decimation))

    plot_1 = ax2.pcolor(raw)
    ax2.set_title('Raw Data')

    plt.show()

def direct_compare(raw, downsized, channel, lim1, lim2, decimation):
    plt.plot(raw[channel], 'b', label = "Raw")
    plt.plot(arange(lim1, lim2, decimation) ,downsized[channel], 'r', label = "Downsized")

    plt.legend()
    plt.show()