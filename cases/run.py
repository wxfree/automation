import pytest
import time
import shutil

if __name__ == '__main__':
    pytest.main()
    time.sleep(2)
    shutil.copy('environment.properties', 'reports')
    shutil.copy('categories.json', 'reports')
    shutil.copy('executor.json', 'reports')

