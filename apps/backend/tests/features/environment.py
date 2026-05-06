import os
import shutil
from app.modules.persistence.database import DatabaseManager, FALLBACK_FILE

TEST_DB = "data/test_benchmarker.sqlite"

def before_scenario(context, scenario):
    if os.path.exists(TEST_DB):
        # We need to ensure it's writable in case a previous scenario left it readonly
        os.chmod(TEST_DB, 0o777)
        os.remove(TEST_DB)
    # Remove WAL/SHM if they exist
    for ext in ['-wal', '-shm']:
        if os.path.exists(TEST_DB + ext):
            os.remove(TEST_DB + ext)
            
    if os.path.exists(FALLBACK_FILE):
        os.remove(FALLBACK_FILE)
        
    context.db_manager = DatabaseManager(db_path=TEST_DB)
    context.db_manager.initialize_schema()

def after_scenario(context, scenario):
    if os.path.exists(TEST_DB):
        os.chmod(TEST_DB, 0o777)
        os.remove(TEST_DB)
    for ext in ['-wal', '-shm']:
        if os.path.exists(TEST_DB + ext):
            os.remove(TEST_DB + ext)
    if os.path.exists(FALLBACK_FILE):
        os.remove(FALLBACK_FILE)
