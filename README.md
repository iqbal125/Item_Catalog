# Item_Catalog

Prerequisites:<br>
Using this code requires basic knowledge of Vagrant, Python, flask and sqlAlchemy<br>
You must have Python, flask and sqlAlchemy installed <br>
You must also have Vagrant installed and ready for use with VM box <br>
If you are not fimiliar with Vagrant visit https://www.vagrantup.com/docs/getting-started/ for more details <br>
For more details on VM box visit https://www.virtualbox.org/<br>
Python can be found at https://www.python.org/<br>
Flask at http://flask.pocoo.org/<br>
sqlAlchemy can be found at https://www.sqlalchemy.org/<br>
<br>
Running the App:
1. Open up your terminal
2. cd into your Vagrant directory
3. Run the vagrant up command
4. Run the vagrant ssh command
5. cd into the project directory /vagrant/catalog
6. SSH into Vagrant
7. Run python database_setup.py in the terminal to set up the initial structure of the database
8. Run python db_start.py in the terminal to populate the database
9. Run python main.py in the terminal to load the templates and run the app
10. Go to http://localhost:9000 in your browser to go to the front page.
