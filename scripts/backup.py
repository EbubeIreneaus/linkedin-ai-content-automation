import os
import shutil
from datetime import datetime

DATA_PATH = "data/"

path_exist = os.path.exists(DATA_PATH)

if not path_exist:
    print("path does not exist")
else:
    zip_file = shutil.make_archive(f'{datetime.now()}-backup', 'zip', DATA_PATH)
    shutil.move(zip_file, '.backups/')