import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import BaseConfig

from models.db_models import Base, Drivers
engine = create_engine(BaseConfig.DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db_session.commit()



if __name__ == "__main__":
    init_db()

