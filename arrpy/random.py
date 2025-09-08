"""
Random number generation for arrpy arrays.
"""

import random as _random


class RandomState:
    """Random number generator state."""
    
    def __init__(self, seed=None):
        """
        Initialize random state.
        
        Parameters
        ----------
        seed : int, optional
            Random seed
        """
        self.seed(seed)
    
    def seed(self, seed=None):
        """Set the random seed."""
        _random.seed(seed)
    
    def uniform(self, low=0.0, high=1.0, size=None):
        """
        Generate uniform random numbers.
        
        Parameters
        ----------
        low : float
            Lower bound
        high : float
            Upper bound
        size : tuple of ints, optional
            Output shape
        
        Returns
        -------
        arrpy
            Random array
        """
        # TODO: Implement uniform distribution
        pass
    
    def normal(self, loc=0.0, scale=1.0, size=None):
        """
        Generate normal random numbers.
        
        Parameters
        ----------
        loc : float
            Mean
        scale : float
            Standard deviation
        size : tuple of ints, optional
            Output shape
        
        Returns
        -------
        arrpy
            Random array
        """
        # TODO: Implement normal distribution
        pass
    
    def randint(self, low, high=None, size=None):
        """
        Generate random integers.
        
        Parameters
        ----------
        low : int
            Lower bound (or upper if high is None)
        high : int, optional
            Upper bound
        size : tuple of ints, optional
            Output shape
        
        Returns
        -------
        arrpy
            Random integer array
        """
        # TODO: Implement random integers
        pass


# Default random state
_default_rng = RandomState()

# Convenience functions
seed = _default_rng.seed
uniform = _default_rng.uniform
normal = _default_rng.normal
randint = _default_rng.randint