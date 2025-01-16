import os
from pathlib import Path




list_of_files = [
    'src/mongodb/connect.py',
    'tests/unit/unit_test.py',
    'tests/integration/integration_test.py',
    'README.md',
    'requirements.txt',
    'setup.py',
    'pyproject.toml',
    'LICENSE',
    '.gitignore',
    'tox.ini',
    'template.py',
]



for file in list_of_files:

    file_path = Path(file)
    file_dir, file_name = os.path.split(file_path)

    if not file_dir == "":
        os.makedirs(file_dir, exist_ok=True)

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass