# vim: set fenc=utf8 ts=4 sw=4 et :

from master.drill import Drill

class RawDrill(Drill):
    """
    Appends the raw data.
    @author Ente
    """

    def get_headers(self):
        return ["Raw"]

    def drill(self, line):
        return [line]
