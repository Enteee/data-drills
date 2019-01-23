# vim: set fenc=utf8 ts=4 sw=4 et :
import re

from master.drill import Drill

class YearDrill(Drill):
    """
    Tries to find dates in data.

    Returns
    ---
    Ratio found dates / input length
    """

    def get_headers(self):
        return ["Years/Length"]

    def drill(self, line):
        data = []
        
        if(len(line) == 0):
            data = [str(0)]
        else:
            data += [str(len(
                re.findall(
                    '(?:^|[^\d])(?:(19[56789]\d)|(20[12]\d)|([5678912]\d))(?:[^\d]|$)',
                    line
                )
            )/len(line))]

        return data
