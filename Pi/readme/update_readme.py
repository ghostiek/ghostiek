import json
import os
from pathlib import Path
from datetime import datetime
from Pi.readme.visualisation import get_data, light_plot, dark_plot

dir_path = os.path.dirname(os.path.realpath(__file__))
path = Path(dir_path)
pi_path = path.parent.absolute()
root_path = path.parent.parent.absolute()
readme_path = f"{root_path}/README.md"
output_path = f"{path}/output.md"

graphs_path = "graphs"

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

light_image_url = f"{graphs_path}/light-plot-{datetime.today().strftime('%Y-%m-%d')}.png"
dark_image_url = f"{graphs_path}/dark-plot-{datetime.today().strftime('%Y-%m-%d')}.png"




readme_text = f"""
# Hello there ( ´◔ ω◔`) ノシ

I'm a Data Scientist and I love learning about Statistics.

## So here's some data about me (☞ﾟヮﾟ)☞


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{dark_image_url}">
  <source media="(prefers-color-scheme: light)" srcset="{light_image_url}">
  <img alt="Shows a black logo in light color mode and a white one in dark color mode."src="{light_image_url}">
</picture>
"""

with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write(readme_text)
    print("File Written Successfully")

# print(readme_text)
