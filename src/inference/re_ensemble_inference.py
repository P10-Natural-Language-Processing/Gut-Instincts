import argparse
from collections import defaultdict
import os
import json
import math
from utils.utils import load_config, subtask_string, load_json_data


class EnsembleREInference:
	def __init__(self, re_predictions_paths, test_data_path, subtask, save_path=None):
		self.test_data_path = test_data_path
		self.save_path = save_path
		self.subtask = subtask
		self.predictions = [load_json_data(path) for path in re_predictions_paths]

	def perform_relation_level_inference(self):
		subtask_name = subtask_string(self.subtask)
		relation_votes = defaultdict(list)
		ensemble_results = defaultdict(lambda: {subtask_name: []})

		for model_predictions in self.predictions:
			for paper_id, content in model_predictions.items():
				for relation in content[subtask_name]:
					if self.subtask == "6.2.1":
						key = (paper_id, relation["subject_label"], relation["object_label"])
					elif self.subtask == "6.2.2":
						key = (paper_id, relation["subject_label"], relation["predicate"], relation["object_label"])
					elif self.subtask == "6.2.3":
						key = (
							paper_id,
							relation["subject_text_span"],
							relation["subject_label"],
							relation["predicate"],
							relation["object_text_span"],
							relation["object_label"],
						)
					else:
						raise ValueError(f"Unsupported subtask: {self.subtask}")

					relation_votes[key].append(relation)

		for key, votes in relation_votes.items():
			if len(votes) >= math.ceil(len(self.predictions) / 2):
				ensemble_results[key[0]][subtask_name].append(votes[0])

		if self.save_path:
			os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
			with open(self.save_path, "w") as f:
				json.dump(dict(ensemble_results), f, indent=4)
		else:
			return dict(ensemble_results)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Run ensemble relation inference.")
	parser.add_argument("--config", type=str, required=True, help="Path to the YAML configuration file")
	args = parser.parse_args()

	config = load_config(args.config)

	ensemble_re_inference = EnsembleREInference(
		re_predictions_paths=config["prediction_paths"],
		test_data_path=os.path.join("data", "Annotations", "Dev", "json_format", "dev.json"),
		subtask=config["subtask"],
		save_path=os.path.join(
			config["prediction_paths"][0].split(os.sep)[0],
			f"{len(config['prediction_paths'])}-ensemble_results",
			f"{config['prediction_paths'][0].split(os.sep)[1]}.json",
		),
	)

	ensemble_re_inference.perform_relation_level_inference()
