from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import *
from database_setup import CPU, GPU
from sqlalchemy.orm import sessionmaker
import Base from database_setup

#Create a session and connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

GPU1 = GPU(name="Nvidia GTX 1060")
session.add(GPU1)
session.commit()

CPU1 = CPU(name="Intel 7700K")
session.add(CPU1)
session.commit()
