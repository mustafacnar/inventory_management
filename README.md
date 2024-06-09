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
