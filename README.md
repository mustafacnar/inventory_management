# inventory_management

##
This application, designed specifically for a single user, enables an e-commerce seller to manage tasks such as product registration and stock tracking across various sales channels.
	
## Running project
Clone project to your computer

	https://github.com/mustafacnar/inventory_management.git
 
Install require packages

	pip install -r requirements.txt

Make migrations

	python manage.py makemigrations

Migrate project

	python manage.py migrate

Collect static files

	python manage.py collectstatic

Create super user for Django Admin

	python manage.py createsuperuser
		
Run your server on your localhost

	python manage.py runserver
