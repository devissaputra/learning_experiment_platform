"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from learning_experiment_platform import core
outputs={'Cohen d: [2,3,4] vs [1,2,3]': core.cohens_d([2,3,4],[1,2,3]), 'raw mean difference': 3-2}
result={'kind':'illustrative_calculation','note':'Synthetic independent groups; not an intervention estimate.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
