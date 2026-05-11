import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from draft_tracker_system.db.models import Base, Role


TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    # create tables
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    player_role = Role(role_name="player")
    admin_role = Role(role_name="admin")

    session.add_all([player_role, admin_role])
    session.commit()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)