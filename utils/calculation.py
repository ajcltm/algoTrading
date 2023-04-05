import numpy as np

def create_price_data(type, alpha, votility, n):
    random = np.random.normal(loc=0, scale=votility, size=n)
    return [100+alpha*votility]

def golden_cross_signal(array, short_window, long_window):
    if np.average(array[short_window:]) >= np.average(array(long_window)):
        return 'buy'
    if np.average(array[short_window:]) <= np.average(array(long_window)):
        return 'sell'