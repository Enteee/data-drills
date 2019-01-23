# vim: set fenc=utf8 ts=4 sw=4 et :
import math

from master.drill import Drill

class EntropyDrill(Drill):
    """
    Calculates the Shannon entropy of a string.
    @source https://stackoverflow.com/questions/2979174/how-do-i-compute-the-approximate-entropy-of-a-bit-string
    @author Ente
    """
    def get_headers(self):
        return ["Entropy"]

    def drill(self, line):
        # get probability of chars in string
        prob = [ float(line.count(c)) / len(line) for c in dict.fromkeys(list(line)) ]
        # calculate the entropy
        entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
        return [entropy]

class IdealEntropyDrill(Drill):
    """
    Calculates the ideal (maximum) Shannon entropy of a string with given length.
    @author Ente
    """

    def get_headers(self):
        return ["IdealEntropy"]

    def drill(self, line):
        length = len(line)
        prob = 1.0 / length
        entropy = -1.0 * length * prob * math.log(prob) / math.log(2.0)
        return [entropy]
