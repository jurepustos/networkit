from _NetworKit import KatzIndex, CommonNeighborsIndex, JaccardIndex, PreferentialAttachmentIndex, AdamicAdarIndex, UDegreeIndex, VDegreeIndex, AlgebraicDistanceIndex, NeighborhoodDistanceIndex, TotalNeighborsIndex, NeighborsMeasureIndex, SameCommunityIndex, AdjustedRandIndex, ResourceAllocationIndex, RandomLinkSampler, ROCMetric, PrecisionRecallMetric, MissingLinksFinder, LinkThresholder, PredictionsSorter
from .graph import Graph

from .support import MissingDependencyError
import numpy as np
import warnings

try:
	import sklearn
except ImportError:
	have_sklearn = False
else:
	have_sklearn = True

def trainClassifier(trainingSet, trainingGraph, classifier, *linkPredictors):
	""" Trains the given classifier with the feature-vectors generated by the given linkPredictors.

	Parameters
	----------
	trainingSet : vector[pair[node, node]]
		Vector of node-pairs to generate features for,
	trainingGraph : networkit.Graph
		Training graph containing all edges from the training set.
	classifier:
		Scikit-learn classifier to train.
	linkPredictors:
		Predictors used for the generation of feature-vectors.
	"""
	# Make sure the set is sorted because the samples will be sorted by node-pairs (asc.)
	# and the labels would be sorted by the initial order. That would lead to an incorrect
	# matching between labels and samples.
	if not have_sklearn:
		raise MissingDependencyError("sklearn")
	trainingSet.sort()
	trainingLabels = getLabels(trainingSet, trainingGraph)
	trainingFeatures = getFeatures(trainingSet, *linkPredictors)
	classifier.fit(trainingFeatures, trainingLabels)

def getFeatures(nodePairs, *linkPredictors):
	""" Returns a numpy-array containing the generated scores from the predictors for the given node-pairs.

	Parameters
	----------
	nodePairs : vector[pair[node, node]]
		Node-pairs to get the samples for.
	*linkPredictors
		List of link predictors to use for sample-generation.

	Returns
	-------
	A numpy-array of shape (#nodePairs, #linkPredictors) containing the generated scores
	from the predictors for the given node-pairs.
	"""
	return np.column_stack(([list(zip(*p.runOn(nodePairs)))[1] for p in linkPredictors]))

def getLabels(nodePairs, G):
	""" Returns a numpy-array containing the labels of the given node-pairs.

	The labels are defined as follows: 1 = link, 0 = absent link.

	Parameters
	----------
	nodePairs : vector[pair[node, node]]
		Node-pairs to get the labels for.
	G : networkit.Graph
		Graph which provides ground truth for the labels.

	Returns
	-------
	A numpy-array containing the labels of the given node-pairs.
	"""
	return np.array(list(map(lambda p: 1 if G.hasEdge(p[0], p[1]) else 0, nodePairs)))
