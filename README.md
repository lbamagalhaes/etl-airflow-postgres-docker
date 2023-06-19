# Project Title

This repository contains the source code and configuration files for the project.
The project utilizes Docker Compose to set up a containerized environment for running Airflow with PostgreSQ, Redis and DBT dependencies.

## Prerequisites

Before running the project, ensure that you have the following installed:

- Docker
- Docker Compose
- pgAdmin

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:

   ```shell
   git clone [https://github.com/your-username/repository-name.git](https://github.com/lbamagalhaes/etl-airflow-postgres-docker.git)
   
2. Change into the project directory:

  ```shell
  cd repository-name
  
3. Start Docker
  
4. Initiate airflow

```shell
docker-compose up airflow-init

4. Build and start the containers:

```shell
docker-compose up airflow-init

5. Access Airflow Web UI:

[http://localhost:8080](http://localhost:8080/)

6. Create a PostgresSQL connection in the Airflow Web UI:

Admin > Connections > Add a New Record

Connection Id: postgres
Connection Type: postgres
Host: postgres
Schema: postgres
Login: airflow
Password: airflow
Port: 5432

6.Connect pgAdmin to PostgresSQL:

Create > Server Group...
Register > Server...

Name: **choose a server name**
Host: localhost
Port: 5431
Maintenance database: airflow
Login: airflow
Password: airflow

7. For shutting down the container:

```shell
docker-compose down --volumes --rmi all













