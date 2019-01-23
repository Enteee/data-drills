"""
A abstract template for drills
@author Ente
"""

import abc

class Drill(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_headers(self):
        """
        Returns a list of column labels (strings)
        """
        pass

    @abc.abstractmethod
    def drill(self, line):
        """
        Does the actual data mining.
        @return a list of values mined (all values must implement __str__)
        """
        pass
