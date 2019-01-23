# vim: set fenc=utf8 ts=4 sw=4 et :
from master.drill import Drill

class LengthDrill(Drill):
    """
    Mines length
    @author Ente
    """

    def get_headers(self):
        return ["Length"]

    def drill(self, line):
        return [len(line)]
