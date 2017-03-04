from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import *
from database_setup import User, Category, Item
from sqlalchemy.orm import sessionmaker
from database_setup import Base

#Create a session and connect to database
# engine = create_engine('sqlite:///catalog.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
#
# GPU1 = GPU(name="Nvidia GTX 1060")
# session.add(GPU1)
# session.commit()
#
# CPU1 = CPU(name="Intel 7700K")
# session.add(CPU1)
# session.commit()
#
# RAM1 = RAM(name="Corsair Vengence 16 GB")
# session.add(RAM1)
# session.commit()
#
# SSD1 = SSD(name="Samsung EVO 850")
# session.add(SSD1)
# session.commit()
#
# CPU2 = CPU(name="Intel 6950X")
# session.add(CPU2)
# session.commit()
