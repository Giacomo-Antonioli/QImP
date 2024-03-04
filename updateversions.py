import os

import toml


def update_version(toml_file: str) -> None:
    """
    Update the version in the __init__.py file based on the version specified
    in the given .toml file.

    Args:
        toml_file (str): The path to the .toml file.

    Returns: None
    """
    # Parse the .toml file
    data = toml.load(toml_file)
    version = data.get("tool", {}).get("poetry", {}).get("version", None)

    if version is None:
        print(f"No version found in {toml_file}")
        return

    # Walk the directory structure
    for root, _, files in os.walk(os.path.dirname(toml_file)):
        if "__init__.py" in files and "qimp" in root.split(os.sep):
            init_file = os.path.join(root, "__init__.py")
            with open(init_file, "r") as f:
                lines = f.readlines()

            # Update the version line
            for i, line in enumerate(lines):
                if line.startswith("__version__"):
                    lines[i] = f"__version__ = '{version}'\n"
                    break
            else:
                # If no version line was found, add one
                lines.append(f"__version__ = '{version}'\n")

            # Write the file back out
            with open(init_file, "w") as f:
                f.writelines(lines)

            print(f"Updated version in {init_file} to {version}")


# Start the process
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".toml"):
            update_version(os.path.join(root, file))
