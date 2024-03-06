from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.config import DB_PATH

engine = create_engine(f'sqlite:///{DB_PATH}')
Base = declarative_base()

class RiskData(Base):
    __tablename__ = 'risk_data'
    vehicle_id = Column(String, primary_key=True)
    action = Column(String, primary_key=True)
    risk_level = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)