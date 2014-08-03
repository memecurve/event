import scipy.special
import scipy.optimize
import scipy.stats


def detect( k, theta, data, n = 3 ):
    """
    detect checks to see if the data given in data is anomalous.

    :param data: The list of data points to check for anomalies
    :type data: list of floats

    :rtype: integer > 0 or False
    :returns: If an anomaly is detected, returns the location of the point + 1 that was anomalous.  Otherwise, returns False

    """

    threshold = find_threshold( k, theta )
    for i, point in enumerate( data[ : -1 ] ):
        if point > threshold:
            ands = True
            n = min( n, len( data ) - i )
            for point in data[ i : i + n ]:
                ands = ands and ( point > threshold )
            if ands:
                return i + 1
    return False

def find_threshold( k, theta ):
    guess = k * theta
    threshold = scipy.optimize.newton( obj_function, guess, args = ( k, theta ) )
    return threshold

def obj_function( x, k, theta, p = 0.95 ):
    val = scipy.stats.gamma.cdf( x, k, loc = 0., scale = theta ) - p
    return val


if __name__ == "__main__":
    import numpy.random
    import matplotlib.pyplot as pp

    k = 2
    theta = 3

    data = numpy.random.gamma( k, theta, 1000 )
    pp.plot( range( len( data) ) , data )
    pp.axhline( y = find_threshold( k, theta ) )
    pp.show( )    

    print detect( k, theta, data )

