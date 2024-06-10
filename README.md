# inventory_management

Tek bir kullanıcıya özel oluşturulan bu uygulama, bir e-ticaret satıcısının  farklı satış kanalları üzerinden ürün kaydı, stok takibi  gibi işlemleri yapabilmesi amacıyla oluşturulmuştur.
Projeyi çalıştırmak için;
* venv oluşturulmalı
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* python manage.py collectstatic
* python manage.py createsuperuser (Yalnızca DjangoAdmin ekranından verileri görüntülemek ve işlem yapmak için gerekli.)
* python manage.py runserver

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
