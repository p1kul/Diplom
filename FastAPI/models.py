from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///./FastAPI.db')

session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

class Randomaizer(Base):
    __tablename__ = 'Randomaizer'
    id = Column(Integer, primary_key=True)
    something = Column(String)


Base.metadata.create_all(bind=engine)

