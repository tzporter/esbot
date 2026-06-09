import os

# Force a local SQLite database for Behave tests before any application code is imported
os.environ["DATABASE_URL"] = "sqlite:///./behave_test.db"

from database import engine
from sqlmodel import SQLModel
# Import models to ensure they are registered with SQLModel.metadata

def before_all(context):
    # Ensure a fresh database for tests
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def after_all(context):
    # Clean up the test database file
    SQLModel.metadata.drop_all(engine)
    if os.path.exists("./behave_test.db"):
        os.remove("./behave_test.db")
