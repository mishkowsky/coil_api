from sqlalchemy import Column, Integer, DateTime, Identity
from sqlalchemy import text
from sqlalchemy.orm import declarative_base

# https://dbdiagram.io/d/Coil_DB-651d9b23ffbf5169f009a95c

Base = declarative_base()


class Coil(Base):
    """
    Class for instagram_logins table of instaparserdb representation.
    """
    __tablename__ = "coil"

    id = Column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
                primary_key=True)
    length = Column(Integer)
    weight = Column(Integer)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    deleted_at = Column(DateTime)
