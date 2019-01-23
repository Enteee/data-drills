# vim: set fenc=utf8 ts=4 sw=4 et :
from math import log, ceil
from hashlib import sha256
from bitstring import BitArray

HASH_FUNCTION = sha256

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

class BloomFilter(bytearray):
    """A simple Bloom Filter implementation
    Calculating optimal filter size: 
                Where:
                m is: self.bitcount (how many bits in self.filter)
                n is: the number of expected values added to self.filter
                k is: the number of hashes being produced
                false positive probability: (1 - math.exp(-float(k * n) / m)) ** k 
    http://en.wikipedia.org/wiki/Bloom_filter
    """

    def __init__(self, array_size=(1 * 1024), hashes=13):
        """Initializes a BloomFilter() object:
            Expects:
                array_size (in bytes): 4 * 1024 for a 4KB filter
                hashes (int): for the number of hashes to perform"""
        super().__init__(array_size)

        self.__bitcount = array_size * 8                            # Bits in the filter
        self.__address_size = int(ceil(log(self.__bitcount, 2)))    # Number of bits used to address the whole filter 
        self.__hashes = hashes                                      # The number of hashes to use
        self.__max_bit = self.__bitcount * ((2 ** self.__address_size) // self.__bitcount) - 1

    def __str__(self):
        return ''.join('{:02x}'.format(b) for b in self)

    def _hash(self, value):
        """Creates a hash of an int and yields a generator of hash functions
        Expects:
            value: value to hash 
        Yields:
            bits to flip"""

        value = bytes(repr(value), 'utf-8')
        digest = BitArray()
        rehash = 0
        for _ in range(self.__hashes):
            # Loop until we've got a valid address bit:
            # We're not always using modulo here by design.
            # Always using modulo would not result in a 
            # uniform distribution which is needed here.
            bit = self.__max_bit + 1
            while bit > self.__max_bit:
                # ensure that there are enoguh bits in hash buffer to pop
                while len(digest) < self.__address_size:
                    digest.append(
                        HASH_FUNCTION(
                            value + int_to_bytes(rehash)
                        ).digest()
                    )
                    rehash += 1
                bit = digest[:self.__address_size].uint
                digest = digest[self.__address_size:]
            yield bit % self.__bitcount

    def append(self, value):
        """Bitwise OR to add value(s) into the self.filter
        Expects:
            value: generator of digest ints()
        """
        for bit in self._hash(value):
            self[(bit // 8)] |= (2 ** (bit % 8))

    def query(self, value):
        """Bitwise AND to query values in self.filter
        Expects:
            value: value to check filter against (assumed int())"""
        # If all() hashes return True from a bitwise AND (the opposite 
        # described above in self.add()) for each digest returned from 
        # self._hash return True, else False
        return all(self[(digest // 8)] & (2 ** (digest % 8)) 
            for digest in self._hash(value))
