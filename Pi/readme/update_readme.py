import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from Pi.readme.visualisation import get_data, light_plot, dark_plot
from git import Repo

dir_path = os.path.dirname(os.path.realpath(__file__))
path = Path(dir_path)
pi_path = path.parent.absolute()
root_path = path.parent.parent.absolute()
readme_path = f"{root_path}/README.md"
graphs_path = "Pi/readme/graphs"
line_graphs = f"{graphs_path}/lineplot"
bar_graphs = f"{graphs_path}/barplot"

yesterdays_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
git_repo_path = f"{root_path}/.git"

try:
    with open(f"{pi_path}/pi_info.json", "r") as pi_info_file:
        pi_info = json.load(pi_info_file)
    is_pi = os.uname().nodename == pi_info["hostname"]
except FileNotFoundError:
    is_pi = False
    data = get_data(is_pi)

data = get_data(is_pi)
light_plot(data, is_pi)
dark_plot(data, is_pi)

light_line_graph_name = f"light-plot-{yesterdays_date}.png"
light_line_graph_url = f"{line_graphs}/{light_line_graph_name}"
light_bar_graph_url = f"{bar_graphs}/{light_line_graph_name}"


dark_line_graph_name = f"dark-plot-{yesterdays_date}.png"
dark_line_graph_url = f"{line_graphs}/{dark_line_graph_name}"
dark_bar_graph_url = f"{bar_graphs}/{dark_line_graph_name}"


readme_text = f"""
# Hello there ( ´◔ ω◔`) ノシ

I'm a Data Scientist and I love learning about Statistics.

## So here's some data about me (☞ﾟヮﾟ)☞


### Distance from the sensor hooked to my desk throughout the day
<figure>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{dark_line_graph_url}">
    <source media="(prefers-color-scheme: light)" srcset="{light_line_graph_url}">
    <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="{light_line_graph_url}">
  </picture>
  <figcaption>Fig 1. Sensor Data from {yesterdays_date}</figcaption>
</figure>



### Aggregate Time Spent on the PC
<figure>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="{dark_bar_graph_url}">
    <source media="(prefers-color-scheme: light)" srcset="{light_bar_graph_url}">
    <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="{light_bar_graph_url}">
  </picture>
  <figcaption>Fig 2. Percentage of Time Spent on the PC on {yesterdays_date}</figcaption>
</figure>
"""

with open(readme_path, "w", encoding="utf-8") as output_file:
    output_file.write(readme_text)
    print("File Written Successfully")

if is_pi:
    plots_path = f"{dir_path}/graphs/"
    data_path = f"{dir_path}/data.json"
    files = [readme_path, plots_path, data_path]
    commit_message = "Automated Update"
    repo = Repo(git_repo_path)
    repo.git.add(files)
    repo.index.commit(commit_message)
    origin = repo.remote(name="origin")
    origin.push()
