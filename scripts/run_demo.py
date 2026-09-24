import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from learning_experiment_platform.core import assign, cohens_d

print('Randomized assignment:', assign(range(10)))
print(f"Cohen d: {cohens_d([8,9,10,9],[6,7,7,8]):.3f}")
print('Note: this is a synthetic demonstration, not an empirical finding.')
