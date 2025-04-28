import yaml

def save_yaml(data, file_path):
    """
    Save data to a YAML file.

    Args:
        data (dict): Data to save.
        file_path (str): Path to the YAML file.
    """
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def load_yaml(file_path):
    """
    Load data from a YAML file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Loaded data.
    """
    with open(file_path, 'r') as f:
        info = yaml.safe_load(f)
        
    return info