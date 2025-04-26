import json
a_json = "scripts\exp_data\loco\difftraj_step_rewards.json"
b_json = "scripts\exp_data\loco\wham_original_step_rewards.json"

with open(a_json) as f:
    a_data = json.loads(f.read())
    
with open(b_json) as f:
    b_data = json.loads(f.read())
    
import numpy as np

import pandas as pd

apd = pd.DataFrame(a_data)
apd.to_excel(a_json.replace(".json", ".xlsx"))


pd.DataFrame(b_data).to_excel(b_json.replace(".json", ".xlsx"))


"""
uv run python -c "import numpy"
"""