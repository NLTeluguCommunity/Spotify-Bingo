import os

def load_env_from_file(file_path):
    """
    Reads a text file with key=value pairs and sets them as environment variables.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Environment file '{file_path}' not found.")

    with open(file_path, "r") as file:
        for line in file:
            # Ignore comments and empty lines
            line = line.strip()
            if line and not line.startswith("#"):
                if "=" not in line:
                    raise ValueError(f"Invalid line in environment file: {line}")
                key, value = line.split("=", 1)
                os.environ[key] = value
