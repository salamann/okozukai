import yaml


def read_config(file_name) -> dict:
    with open(file_name, "r", encoding="utf-8") as f:
        configs = yaml.safe_load(f)
    return configs
