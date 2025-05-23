import torch
import numpy as np
import random


def seed_everything(seed):
	"""
	Seed all the possible sources of randomness to ensure reproducibility.

	Args:
	    seed (int): The seed value to set.
	"""
	random.seed(seed)

	np.random.seed(seed)

	torch.manual_seed(seed)
	torch.cuda.manual_seed(seed)
	torch.cuda.manual_seed_all(seed)

	torch.backends.cudnn.deterministic = True
	torch.backends.cudnn.benchmark = False
