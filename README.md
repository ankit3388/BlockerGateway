# Django Gateway Interface

## Overview

**Django Gateway Interface** is a Django application designed to provide a user-friendly web interface for configuring Nginx settings for set request limit and IP block. This package enables users to easily manage gateway configurations, specifically to set request limits and block IP addresses at any endpoint for security purposes. It supports both Windows and Linux environments, allowing for seamless integration and efficient configuration management based on user input.
**Make sure Selected Operating System is same as your working environment** 

## Features

- User-friendly interface for gateway configuration.
- Integration with Nginx to apply and manage configurations.
- Easy installation via PyPI.
- Support Windows and Linux even in WSL

## Installation

You can install the Django Gateway Interface package from PyPI using pip. Make sure you have Python 3.8 or higher and Django 3.0 or higher installed.

```bash
pip install gatapp
```
## Requirement
Make sure your django app is running on http://127.0.0.1:8000
, needed some modification in setting.py for template and css and follow configuration 

## Configuration 
Add to Installed Apps:
Add 'gateapp' to your INSTALLED_APPS in your Django settings.py:

```
import os
```

```
INSTALLED_APPS = [
    ...
    'gateapp',
    ...
]
```
```
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        ...
    },
]
```

```
# Optionally include additional static file directories
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  
  
]
```
**Database Migrations**:
Run the following command to apply database migrations for the Django app:
```
python manage.py migrate
```

**Static Files:**
Collect static files for the Django app:

```
python manage.py collectstatic
```

**URL Configuration**:
Include the URLs for the Gateway Interface in your Django project urls.py:

```
from django.urls import path, include
urlpatterns = [
    # Other URL patterns
    path('configure/', include('gateapp.urls'))
]
```
**Nginx Configuration:**
Configure Nginx to serve your Django application. Here’s a basic Nginx configuration example for windows:

```
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/static/files/;
    }

    location /media/ {
        alias /path/to/your/media/files/;
    }
}
```
Replace yourdomain.com and file paths with your specific details.

**Usage**

Run the Django Development Server:
Start the Django development server to test your installation:

```
python manage.py runserver
```

**Access the Interface**:
Open your web browser and navigate to http://localhost:8000/configure to access the Gateway Interface.

## Configure Gateway Settings:
Use the web interface to fill in and submit configuration details for the gateway.

## Contributing
Contributions are welcome! To contribute to the Django Gateway Interface:

**Fork the repository on GitHub**
Create a new branch for your changes.
Make your changes and test them.
Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.



**Thank you for using Django Gateway Interface! If you encounter any issues or have suggestions, please feel free to open an issue on GitHub or contact us directly.**
