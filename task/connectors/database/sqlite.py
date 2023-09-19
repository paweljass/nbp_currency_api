from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///mydatabase.db')
Base = declarative_base()

class CurrencyData(Base):
    __tablename__ = 'currency_data'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    rate = Column(Float)
    price_in_pln = Column(Float)
    date = Column(Date)
    price_in_source_currency = Column(Float)

Session = sessionmaker(bind=engine)
session = Session()

def upload_new_data(data):
    session.add(data)
    session.commit()