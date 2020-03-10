from libc.stdint cimport uint64_t
from libcpp.vector cimport vector
from libcpp cimport bool as bool_t

ctypedef uint64_t count
ctypedef uint64_t index
ctypedef index node
ctypedef double edgeweight

from .helpers cimport *
from .graph cimport _Graph, Graph
from .structures cimport _Partition, Partition

cdef extern from "<networkit/matching/Matching.hpp>":

	cdef cppclass _Matching "NetworKit::Matching":
		_Matching() except +
		_Matching(count) except +
		void match(node, node) except +
		void unmatch(node, node) except +
		bool_t isMatched(node) except +
		bool_t areMatched(node, node) except +
		bool_t isProper(_Graph) except +
		count size(_Graph) except +
		index mate(node) except +
		edgeweight weight(_Graph) except +
		_Partition toPartition(_Graph) except +
		vector[node] getVector() except +

cdef class Matching:
	cdef _Matching _this
	cdef setThis(self,  _Matching& other)
