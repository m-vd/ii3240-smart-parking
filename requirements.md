# Smart Parking Services

"Smart Parking Services" is a system of services intented to realize smart campus concept, especially in parking management. The services is made by several IST students from ITB as a project for one of their courses: II3240: Information Systems and Technology Engineering.

---

## How to Run

To run the services, go to the root folder of services (location of manage.py) and run the code below.

```bash
python manage.py runserver [IP address]:[Port]
```

To run the server, for example use 0.0.0.0:80 to run at whatever IP address the computer have at its interface.
If IP address and port is not defined, the server will be run at localhost:8000 (default)

## How to Create Superuser

To create a superuser for accessing `/admin`, go to the root folder of services and run the code below.

```bash
python manage.py createsuperuser
```