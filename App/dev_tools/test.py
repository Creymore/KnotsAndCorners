# Tested how to import Used CodeX since it is not the logic part of my code, it is just to make it work 

from pathlib import Path
import sys

# Support running this file directly (python App/dev_tools/test.py)
# and as a module inside the App package.
if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    from App.utils.ChatGBTs_utils import print_dict
else:
    from ..utils.ChatGBTs_utils import print_dict
