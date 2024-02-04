import os
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))
path = Path(dir_path)
parent_path = path.parent.parent.parent.absolute()
readme_path = f"{parent_path}/README.md"
output_path = f"{path}/output.md"


readme_text = """
# Hello there ( ´◔ ω◔`) ノシ

I'm a Data Scientist and I love learning about Statistics.

## So here's some data about me (☞ﾟヮﾟ)☞

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="">
  <source media="(prefers-color-scheme: light)" srcset="">
  <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="">
</picture>

"""

with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write(readme_text)

print(readme_text)