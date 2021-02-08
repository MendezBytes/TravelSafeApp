from sqlalchemy import Column, create_engine, ForeignKey, Integer, DateTime, Sequence, String, Boolean, Float, func, \
    ForeignKeyConstraint
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Drivers(Base):
    __tablename__ = "drivers"
    driver_id = Column(Integer, Sequence('driver_seq'), primary_key=True)
    driver_uuid = Column(String(100))
    firstname = Column(String(30))
    lastname = Column(String(30))
    license_plate = Column(String(7))
    contact_num = Column(String(12))
    vehicle_color = Column(String(40))
    vehicle_brand = Column(String(40))
    vehicle_make = Column(String(40))
    added_date = Column(DateTime)
    qr_data = Column(String(400))
    ip_address = Column(String(100))
    id_picture_path = Column(String(300))
    user_agent = Column(String(300))
