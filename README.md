## Environment Configuration

This project uses environment variables to manage configuration settings. The sensitive data is stored in two `.env` files: `.env/.env` for local development and `.env/.env.prod` for production.

### `.env`

This file contains environment variables for local development.

```plaintext
# Secret key for Django's cryptographic signing, should be kept secure
SECRET_KEY='your-secret-key'

# Hosts allowed to access the Django application
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis settings for caching and task queue management
REDIS_HOST='localhost'
REDIS_PORT='6380'

# PostgreSQL database connection settings
SQL_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=your-database-name
POSTGRES_USER=your-database-user
POSTGRES_PASSWORD=your-database-password
SQL_HOST=localhost
SQL_PORT='5433'

# Celery settings for background task management
CELERY_BROKER_URL='redis://localhost:6380/0'
CELERY_RESULT_BACKEND='redis://localhost:6380/0'

# Debug mode
DEBUG=True
```

### `.env.prod`

This file contains environment variables for the production environment.

```plaintext
# Secret key for Django's cryptographic signing, should be kept secure
SECRET_KEY='your-secret-key'

# Hosts allowed to access the Django application
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis settings for caching and task queue management
REDIS_HOST='redis'
REDIS_PORT='6379'

# PostgreSQL database connection settings
SQL_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=your-database-name
POSTGRES_USER=your-database-user
POSTGRES_PASSWORD=your-database-password
SQL_HOST=postgres
SQL_PORT='5432'

# Celery settings for background task management
CELERY_BROKER_URL='redis://redis:6379/0'
CELERY_RESULT_BACKEND='redis://redis:6379/0'

# Debug mode
DEBUG=True
```

### Important Notes

- **SECRET_KEY**: This key is critical for the security of your Django application. Ensure it is kept secret and is not shared publicly.
- **ALLOWED_HOSTS**: This is a list of IP addresses or domain names that are allowed to access the Django application.
- **Database Settings**: PostgreSQL is used as the database backend. Adjust the settings according to your database configuration.

[//]: # (- **Redis Settings**: Redis is used for caching and as a message broker for Celery tasks.)
