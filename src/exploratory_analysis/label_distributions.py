import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from utils.utils import load_label_distribution


def label_distribution_stacked_bar_plot(
	label_distribution: dict, save_path: str = os.path.join("plots", "label_distribution_stacked_bar_plot.pdf")
):
	data = []
	for quality, labels in label_distribution.items():
		for label, count in labels.items():
			data.append({"Quality": quality, "Label": label, "Count": count})
	df = pd.DataFrame(data)

	df_pivot = df.pivot(index="Label", columns="Quality", values="Count").fillna(0)

	df_pivot["Total"] = df_pivot.sum(axis=1)
	df_pivot = df_pivot.sort_values(by="Total", ascending=False)
	totals = df_pivot["Total"]
	df_pivot = df_pivot[["Bronze", "Silver", "Gold", "Platinum"]]

	sns.set_theme(style="ticks")

	qualities = df_pivot.columns
	labels = df_pivot.index
	x = np.arange(len(labels))
	bottom = np.zeros(len(labels))

	palette = sns.color_palette("magma", n_colors=4, desat=1)

	plt.figure(figsize=(14, 7))
	for i, quality in enumerate(qualities):
		counts = df_pivot[quality].values
		plt.bar(x, counts, bottom=bottom, color=palette[i], edgecolor="black", linewidth=0.5, label=quality)
		bottom += counts

	for idx, total in enumerate(totals):
		ratio = total / totals.sum()
		plt.text(
			x[idx],
			total + total * 0.01,
			f"{ratio:.2%}",
			ha="center",
			va="bottom",
			fontsize=12,
			color="black",
		)

	plt.xlabel("Label", fontsize=14)
	plt.ylabel("Count", fontsize=14)
	plt.xticks(x, labels, rotation=45, ha="right", fontsize=12)
	plt.yticks(fontsize=12)
	plt.legend(title="Quality", fontsize=12, title_fontsize=14)

	sns.despine()
	plt.tight_layout()
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	plt.savefig(save_path, format="pdf")


if __name__ == "__main__":
	label_distribution_stacked_bar_plot(
		label_distribution=load_label_distribution(),
		save_path=os.path.join("plots", "exploratory_analysis", "entity_label_distribution.pdf"),
	)
	label_distribution_stacked_bar_plot(
		label_distribution=load_label_distribution(
			file_path=os.path.join("data", "metadata", "relation_label_distribution.json"),
		),
		save_path=os.path.join("plots", "exploratory_analysis", "relation_label_distribution.pdf"),
	)
