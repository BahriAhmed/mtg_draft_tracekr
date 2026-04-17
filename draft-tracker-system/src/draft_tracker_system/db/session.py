from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(db_url):

    return create_engine(
        db_url,
        pool_pre_ping=True
    )

def get_session(engine):
    return sessionmaker(bind=engine)()