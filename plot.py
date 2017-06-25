import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(color_codes=True, context="poster")
sns.set_style("white", {'font.family': 'serif', 'font.serif': 'Times New Roman'})
sns.set_palette("Set2", 8)


results = pd.DataFrame()
for seed in range(1, 31):
    this_run = pd.read_csv("results_{}.csv".format(seed))
    results = pd.concat([results, this_run])

f, axes = plt.subplots(1, 1, figsize=(7, 6))

g = sns.tsplot(data=results, value="Time", condition="Group", unit="Run", time="Interval", ax=axes, estimator=np.median)

sns.despine(ax=axes)
plt.tight_layout()
plt.savefig("plots/results.pdf", bbox_inches='tight')
