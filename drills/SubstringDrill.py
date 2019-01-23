# vim: set fenc=utf8 ts=4 sw=4 et :
from master.drill import Drill
from utils.bloomfilter import BloomFilter

BLOOM_FILTER_SIZE = 512

class SubstringDrill(Drill):
    """
    Calculates ratio unique substrings / substring count
    @author Ente
    """

    def get_headers(self):
        return [
            "UniqueSubstrings/Substrings",
            "SubstringBloomFilter"
            ]

    def drill(self, line):

        def chunks():
            for i in range(0, len(line)):
                for n in range(1, len(line) + 1):
                    ret = line[i:i+n]
                    if(len(ret) == n):
                        yield ret

        substrs = [ s for s in chunks() ]
        unique_substrs = set(substrs)

        bloom_filter = BloomFilter(BLOOM_FILTER_SIZE)
        for s in unique_substrs:
            bloom_filter.append(s)

        return (
            ([len(unique_substrs)/len(substrs)] if len(substrs) != 0 else [-1])
            + [bloom_filter]
        )

