from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import User, Category, Item



engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.add_all([Category(name = "CPU"),
                 Category(name = "GPU"),
                 Category(name = "RAM"),
                 Category(name = "SSD"),
                 Category(name = "HDD"),
                 Category(name = "MB")])

session.commit()
