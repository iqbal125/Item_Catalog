from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import User, Category, Item



engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

session.add_all([Category(name = "CPU"),
                 Category(name = "Graphics Card"),
                 Category(name = "RAM"),
                 Category(name = "Solid State Drive"),
                 Category(name = "Hard Drive"),
                 Category(name = "Mother Board")])


CPU1 = Item(name="Intel i7 7700k", description="4 core processor with 8 hyperthreads",
                     price="350", category_id=1)
session.add(CPU1)
session.commit()

CPU2 = Item(name="Intel i7 6850k", description="6 core processor with 12 hyperthreads",
                     price="550", category_id=1)
session.add(CPU2)
session.commit()

CPU3 = Item(name="Intel Extreme Edition 6950X", description="10 core processor with 20 hyperthreads",
                     price="1500", category_id=1)
session.add(CPU3)
session.commit()

GPU1 = Item(name="Nvidia GTX 1070", description="The best per dollar graphics card, 2700 CUDA cores",
                     price="375", category_id=2)
session.add(GPU1)
session.commit()

GPU2 = Item(name="Nvidia GTX 1080", description="The best graphics card for 4K, 3200 CUDA cores",
                     price="550", category_id=2)
session.add(GPU2)
session.commit()

GPU3 = Item(name="Nvidia GTX Titan X", description="The best current graphics card, 3500 CUDA cores",
                     price="1600", category_id=2)
session.add(GPU3)
session.commit()

RAM1 = Item(name="Kingston HyperX FURY", description="Great DDR3 Ram 16GB",
                     price="130", category_id=3)
session.add(RAM1)
session.commit()

RAM2 = Item(name="Corsair Vengeance", description="Great DDR4 Ram 32GB",
                     price="260", category_id=3)
session.add(RAM2)
session.commit()

RAM3 = Item(name="Corsair Dominator", description="The Best Ram 64GB",
                     price="480", category_id=3)
session.add(RAM3)
session.commit()

SSD1 = Item(name="Samsung 850 EVO", description="The most popular SSD. 250GB",
                     price="99", category_id=4)
session.add(SSD1)
session.commit()

SSD2 = Item(name="Samsung 850 Pro", description="The best SSD. 512GB",
                     price="320", category_id=4)
session.add(SSD2)
session.commit()

SSD3 = Item(name="Samsung 960 EVO", description="New SSD Technology. 1TB",
                     price="540", category_id=4)
session.add(SSD3)
session.commit()

HDD1 = Item(name="Western Digital Blue", description="The most popular hard drive. 1TB.",
                     price="50", category_id=5)
session.add(HDD1)
session.commit()

HDD2 = Item(name="Seagate Barracuda", description="Great and reliable hard drive. 4TB",
                     price="120", category_id=5)
session.add(HDD2)
session.commit()

HDD3 = Item(name="Seagate IronWolf", description="Huge and reliable hard drive. 10TB",
                     price="320", category_id=5)
session.add(HDD3)
session.commit()

MB1 = Item(name="MSI Gaming B150", description="Great Mother Board, with SLI",
                     price="95", category_id=6)
session.add(MB1)
session.commit()

MB2 = Item(name="ASUS ROG STRIX Z270E", description="Great Mother Board with RGB and SLI",
                     price="190", category_id=6)
session.add(MB2)
session.commit()


MB3 = Item(name="ASUS ROG Maximus IX", description="The best Mother Board",
                     price="280", category_id=6)
session.add(MB3)
session.commit()
