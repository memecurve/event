import math
import scipy.special

def fit_gamma( data ):
    """
    Takes the time series of floats representing word counts, 
    and uses max likelihood estimation to measure the gamma 
    distribution parameters.  Uses the parameterization
    \\frac{ 1. }{  \\Gamma( k ) \\theta ^ k  } x ^{ k - 1. } e^{ - x / \\theta}

    :param data: The list of word counts for a word, with each entry a float
                 showing the number of counts in consecutive 15 minute intervals
    :type data: list( [ float, float, ...] )

    :raises: ApplicationException when blah happens
    :rtype: tuple of two floats
    :returns: Returns a pair of floats representing the max likelihood parameters for the data.
    """
    N = float( len( data ) ) 
    mu = float( sum( data ) ) / N
    lnmu = sum( [ math.log( xi ) for xi in data ] ) / N
    s = math.log( mu ) - lnmu
    y = float( sum( data ) )


    # approximate k
    k_hat = ( 3. - s + math.sqrt( ( ( s - 3. ) ** 2. ) + ( 24. * s ) ) ) / ( 12. * s )
    # 1st newton update
    k_hat = k_hat - ( math.log( k_hat ) - scipy.special.digamma( k_hat ) - s ) / ( (1. / k_hat ) - scipy.special.polygamma( 1, k_hat ) )
    
    theta_hat = y / ( ( N * k_hat ) - 1. )

    return ( k_hat, theta_hat )



if __name__ == "__main__":
    import numpy.random
    def test_estimate_gamma( ):
        data = numpy.random.gamma( 2,3 , 150 )
        data = list( data ) 
        print fit_gamma( data )
    test_estimate_gamma( )
