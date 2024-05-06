# HappyHours Backend(DRF) 
# Server : http://16.170.203.161/
## Overview
HappyHours is a novel platform designed to enhance customer engagement for restaurants and cafes during their off-peak hours through the concept of "happy hours." This system allows participating businesses to offer free beverages during specified hours, addressing the drop in customer traffic typically experienced midday and between the end of lunch service and the start of dinner. By leveraging a subscription-based model, HappyHours aims to increase foot traffic and revenue for these venues, transforming how these businesses attract customers during less busy times.

## Features
- **User Management**: Handles different roles like clients, partners, and admins.
- **Establishment Profiles**: Partners can manage details about their establishments.
- **Beverage Management**: Manage a detailed list of beverages offered by establishments.
- **Order System**: Allows clients to place orders directly within the platform.

## Models
- **User**: Represents clients, partners, and admins with fields like email, role, etc.
- **Establishment**: Represents details like location, name, description of the establishments.
- **Beverage**: Contains information about the drinks available including name, category, and price.
- **Order**: Records transactions of beverages ordered by users at establishments.

## APIs
Endpoints are provided for each entity (Users, Establishments, Beverages, Orders) supporting CRUD operations along with specific filters and authentication methods to ensure data security.

## Installation and Setup
The project uses Docker and Docker Compose to streamline the deployment and management of its services, ensuring consistency across environments. Below are the instructions to build and run the application using Docker.

### Prerequisites
- Docker
- Docker Compose

### Building and Running with Docker Compose
1. **Clone the repository**: `git clone git@github.com:kaganatreviro/backend.git`
2. **Navigate into the project directory**: `cd backend`
3. **Environment Variables**:
Create a `.env` file in the project root and fill it with the necessary environment variables as per `docker-compose.yml`:

- DB_NAME=yourdbname
- DB_USER=yourdbuser
- DB_PASSWORD=yourdbpassword
- ALLOWED_HOSTS=yourdomain.com
- SECRET_KEY=yoursecretkey
- GMAIL_USER=yourgmailusername
- GMAIL_PASSWORD=yourgmailpassword

4. **Build the Docker images**:
This step builds the Docker images for the web service and sets up the database.
`docker-compose build`
5. **Run the containers**:
This command starts all services defined in your docker-compose.yml file.
`docker-compose up -d`
6. **Collect statics and run migrations**:
`docker-compose exec web py manage.py collectstatic`
`docker-compose exec web py manage.py migrate`
### Services Defined in Docker Compose
- **Web Service**: Runs the Django application using Gunicorn as the WSGI server.
- **Database Service**: Uses a PostgreSQL database.
- **Nginx Service**: Serves static files and acts as a reverse proxy to handle client requests.

This setup ensures that the application is ready to handle requests after Docker containers are successfully started.

## Accessing the Application
Once the containers are running, the application is accessible at `http://localhost:8000` for API interactions, or `http://localhost` if accessing through configured Nginx at ports 80 or 443.