from pipelines import (
    etl,
    generate_dataset
)
from datetime import datetime as dt
from pathlib import Path
from typing import Any
import yaml

def load_config(path: str):
    with open(path, "r") as f:
        config_dict = yaml.safe_load(f)

    return config_dict["parameters"]
def main():
    root_dir = Path(__file__).resolve().parent.parent
    '''
    pipeline_args = load_config(root_dir / "configs" / "etl.yaml")
  
    print(pipeline_args)
    etl_instance = etl(**pipeline_args)
    '''
    generate_dataset_pipeline_args = load_config(root_dir / "configs" / "generate_dataset.yaml")
    generate_dataset(**generate_dataset_pipeline_args)

if __name__ == "__main__":
    main()