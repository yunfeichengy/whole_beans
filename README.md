# Whole Beans Marketplace ☕️🌿

## Installing dependencies
### Ubuntu
django version: 3.0.3\
```sudo apt-get install libssl-dev```\
```python -m pip install -U channels```\
```sudo apt-get install redis-server```\
```python -m pip install channels_redis```\
### macOS
```brew install openssl```\
```python3 -m pip install -U channels```\
```brew install redis```\
```python3 -m pip install channels_redis```\
```brew services start redis```\
```pip install stripe```\

## To get things started
Run ```python manage.py runserver``` in root directory to start the server. <br />
Then connect to ```localhost:8000``` <br />
<u><b>Important Note: </b></u> Settings are not changed. will not run on deployment environment 

### Database
* to make changes to database: "python manage.py makemigrations"
* to migrate: "python manage.py migrate"
* username and password of admin is "username" & "password"
* a random user that you can use is username=pikachu & password=123

### Superuser
connect to ```localhost:8000/admin``` <br />
username: ```beanmaster``` <br />
password: ```welovebeans``` <br />

### Notes
* Ignore .idea directory in root directory. .idea is for IDE specific use.
