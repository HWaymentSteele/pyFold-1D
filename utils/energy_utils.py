import numpy as np

class Parameters(object):

	def __init__(self, epsilon=-2, delta=1, sigma=-1, gnm=True):
		'''
		Class to hold energy parameters for Toyfold-1D model.

		Energy options:
		delta: penalty for bends (default +1)
		epsilon: bonus for base pairs (default -2)
		sigma:  bonus for stacking (default -1)
		gnm (bool): include free energy calculation for gaussian-network-model fluctuations. (how to normalize?)
		'''

		self.epsilon = epsilon
		self.delta = delta
		self.sigma = sigma
		self.gnm = gnm

def score_bends(d):

#	Take a bunch of conformations and score the number of bends in each
# conformation. For use in determining bending energy penalty ('Delta' in
# toyfold notes).
#
# INPUT
#
# d = [Nbeads x Nconformations] input directions
#
# OUTPUT
#
# num_bends = [num_conformations] number of bends
	return np.sum((d[:-1] != d[1:]),axis=0)

def score_pairs(p):
# Take a bunch of pairing patterns and return number of pairs,
#  needed for scoring.
#
# INPUT
#
#  p = [Nbeads x Nconformations] partners  (-1 if bead is unpaired,
#        otherwise index of partner from 0,... Nbeads-1 )
#
# OUTPUT
#
# num_bends = [num_conformations] number of pairs
	return np.sum((p>=0),axis=0)/2

def score_stacks(stems_list):

# Take list of stems from conformations, return number of stacked stems
#
# INPUT
#
# stems_list: list (length num_conformations) of lists (length variable) of stems.
#
# OUTPUT
# 
# num_stacks [num_conformations]: number of stacked stems (i.e. more than one bp in stem)
	
	return np.array([np.sum([len(stem) - 1 for stem in stems]) for stems in stems_list])

def score_fluctuations(matrices):
# Take list of connectivity matrices (A) from conformations, return array with free energy of Gaussian network model
#
# If Gamma is connectivity matrix:
#
# Lambda_ij = -Gamma_ij            if i != j
#			 = sum_{k!=i} Gamma_ik if i=j
#
# Then free energy due to elastic modes of network is 3/2 kT \sum \log (eig_i), where eig_i are the eigenvalues of Lambda.
#
# INPUT
#
# matrices: list (length num_conformations) of connectivity matrices.
#
# OUTPUT
# 
# elastic energy [num_conformations]

	#ugly routine, beautify later

	return_vec = []
	N = len(matrices[0])
	for mat in matrices:

		lambda_mat = np.zeros([N,N])

		for i in range(N):
			lambda_mat[i,i] += np.sum(mat[i]) # to get diagonal elts

		lambda_mat -= mat # to get negative off-diagonal elts

		eigenvals = np.linalg.eig(lambda_mat)[0]

		# zeroth eigenval corresponds to rigid translation mode, remove
		nonzero_eigenvals = eigenvals[np.where(eigenvals != 0)] 

		return_vec.append(-1.5*np.nansum(np.log(nonzero_eigenvals)))

	return return_vec

