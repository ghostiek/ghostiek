import os
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))
path = Path(dir_path)
parent_path = path.parent.parent.parent.absolute()
readme_path = f"{parent_path}/README.md"

with open(readme_path, "r") as readme_file:
    readme_text = readme_file.read()

print(readme_text)