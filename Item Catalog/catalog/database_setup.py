import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declartive import declartive_base
from sqlalchemy.orm import relationship

Base = declartive_base()


class CPU(Base):
    __tablename__ = "cpu"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class GPU(Base):
    __tablename__ = "gpu"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)




engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
