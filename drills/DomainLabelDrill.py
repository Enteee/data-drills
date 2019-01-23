# vim: set fenc=utf8 ts=4 sw=4 et :
from master.drill import Drill
from utils.bloomfilter import BloomFilter
from .EntropyDrill import EntropyDrill

SPLIT='.'
MAX_LABELS=3
BUCKETS=1024
BLOOM_FILTER_SIZE=2**6  # 2**6 * 8 = m, with (k=13, n=10) -> P=0.16 (err probability) 
ENTROPY_DRILL = EntropyDrill()

class DomainLabelDrill(Drill):
    """
    Classifies domain labels
    @author Ente
    """

    def get_headers(self):
        return (
            [ "LabelsCount" ]
            + [ "Label{}Entropy".format(i) for i in range(MAX_LABELS) ]
            + [ "Label{}Length".format(i) for i in range(MAX_LABELS) ]
            + ["LabelsBloomFilter"]
        )

    def drill(self, line):
        line = line.rstrip('.')
        labels = line.split(SPLIT)

        # get the top most MAX_LABELS
        top_labels = labels[-MAX_LABELS:]
        top_labels = ['' for i in range(MAX_LABELS - len(top_labels))] + top_labels

        bloom_filter = BloomFilter(BLOOM_FILTER_SIZE)
        [bloom_filter.append(l) for l in labels]

        return (
            [len(labels)]
            + ([ENTROPY_DRILL.drill(l)[0] for l in reversed(top_labels)])
            + ([len(l) for l in reversed(top_labels)])
            + [bloom_filter]
        )
