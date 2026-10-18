import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

#location for testing DB
SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

# Creates the SQLAlchemy engine for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
# It's okay for this connection to be used from another thread (execution path). This is commonly used with FastAPI's TestClient.
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

#Creates a test version of SessionLocal.
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Look at all the models registered with Base and create their tables in this database if they don't already exist.
Base.metadata.create_all(bind=engine)

# Defines a replacement for your normal get_db() dependency.
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creates a fake version of your authentication dependency.
def override_get_current_user():
    return {'username': 'tester', 'user_id': 1, 'user_role': 'admin'}

# Creates a client that can communicate with your FastAPI application.
client = TestClient(app)

'''
1. The fixture creates a Todo with predefined values.
2. A database session (TestingSessionLocal) is created for the test DB.
3. The Todo is added to that session.
4. db.commit() saves the Todo to the test DB.
5. yield todo gives the created Todo to the test that requested the fixture. The fixture pauses here while the test runs.
6. After the test finishes, execution resumes after yield.
7. engine.connect() creates a database connection.
8. It executes a SQL statement which deletes every Todo from the todos table.
9. connection.commit() permanently commits that deletion.
10. The test database is now clean.
'''
@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn every day!",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
# Yield => Give this value to the test, let the test finish, and then come back here and continue executing.
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username="tester",
        email="tester@localhost.com",
        first_name="tester",
        last_name="tester",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    # Yield => Give this value to the test, let the test finish, and then come back here and continue executing.
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()