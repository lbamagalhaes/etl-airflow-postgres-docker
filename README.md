## Project Description
- This repository contains the code and configuration files for the Airflow workflow management system. The system utilizes several key services, each serving a specific purpose within the workflow orchestration process:

### PostgreSQL
- PostgreSQL is used as the backend database for Airflow. It stores metadata related to workflows, task states, execution logs, and other relevant information.

### pgAdmin
- pgAdmin is an administration and development tool used to manage the PostgreSQL database. It provides a graphical interface for tasks such as querying the database, configuring settings, monitoring performance, and managing users.

### Redis
- Redis is an in-memory data structure store used as a message broker in the Airflow setup. It facilitates the exchange of messages between different components of Airflow.

### Celery
- Celery is a distributed task queue system used as the task execution engine in Airflow. It allows for the asynchronous and parallel execution of tasks across multiple workers. Celery workers retrieve tasks from the task queue and execute them independently.

### Airflow
- Airflow is an open-source platform for orchestrating and managing workflows. It allows users to define, schedule, and monitor workflows as Directed Acyclic Graphs (DAGs). Airflow comprises several key components:

##### Airflow Scheduler
- The Airflow Scheduler is responsible for determining when tasks should be executed based on their dependencies and schedules. It interacts with the Airflow database and message broker to trigger task execution.

##### Airflow Webserver
- The Airflow Webserver provides a web-based user interface to monitor and control workflow executions. It fetches information from the Airflow database, such as DAG definitions, task states, and execution logs, to display the current status of workflows and tasks.

##### Airflow Worker
- Airflow Workers are responsible for executing tasks. They retrieve tasks from the task queue (managed by Celery) and execute them independently. Workers communicate with the Airflow database and message broker to update task status and results.

##### Airflow Triggerer
- The Airflow Triggerer is responsible for triggering workflow executions based on defined schedules or external events. It interacts with the Airflow Scheduler to initiate workflow runs.

### Metabase
- Metabase is an open-source business intelligence tool used for visualizing and analyzing data. It can be integrated with Airflow to provide insights and reports on workflow execution, task performance, and other relevant metrics.

## Workflow Description
- The Airflow Scheduler, running as part of the Airflow infrastructure, communicates with the Airflow database, Redis (message broker), and Celery to orchestrate task execution.

- When a workflow is scheduled to run, the Airflow Scheduler adds task messages to the Celery task queue. These messages contain information about the tasks and their dependencies.

- Celery workers, connected to the Celery task queue, retrieve task messages and execute tasks asynchronously. Workers communicate task progress, status updates, and results to Redis.

- The Airflow Worker component listens to task updates in Redis, retrieves the information, and updates the Airflow database with task statuses and results.

- The Airflow Webserver fetches data from the Airflow database to provide a graphical interface where users can monitor workflow execution, view task logs, and manage workflows.

- The Airflow Triggerer component, based on predefined schedules or external triggers, communicates with the Airflow Scheduler to initiate workflow runs and trigger task execution.

- PostgreSQL, as the backend database, stores and retrieves workflow metadata, task states, execution logs, and other relevant information.

- pgAdmin provides a graphical interface to manage the PostgreSQL database, allowing administrators and developers to interact with the database, configure settings, and monitor performance.

- Metabase, when integrated with PostgreSQL, can be used for visualizing and analyzing data related to workflow execution.

### Prerequisites
Before running the project, ensure that you have the following installed:

- Docker
- Docker Compose

### Getting Started
To get started with the project, follow these steps:

1. Clone the repository:

   ```shell
   git clone [https://github.com/your-username/repository-name.git](https://github.com/lbamagalhaes/etl-airflow-postgres-docker.git)
   ```
   
2. Change into the project directory:

   ```shell
   cd etl-airflow-postgres-docker
   ```
  
3. Start Docker
  
4. Initiate airflow

   ```shell
   docker-compose up airflow-init
   ```

5. Build and start the containers:

   ```shell
   docker-compose up 
   ```

6. Access Airflow Web UI:

* [http://localhost:8080](http://localhost:8080/)

7. Create a PostgresSQL connection in the Airflow Web UI:

* Admin > Connections > Add a New Record

   * Connection Id: postgres
   * Connection Type: postgres
   * Host: postgres
   * Schema: postgres
   * Login: airflow
   * Password: airflow
   * Port: 5432

8. Access PostgresSQL through pdAdmin:

* [http://localhost:5050](http://localhost:5050/)

* Register > Server...

   * Name: **choose a server name**
   * Host: postgres
   * Port: 5432
   * Maintenance database: airflow
   * Login: airflow
   * Password: airflow

9. Access Metabase through pdAdmin:

* [http://localhost:3000](http://localhost:3000/)

   * Host: postgres
   * Port: 5432
   * Maintenance database: airflow
   * Login: airflow
   * Password: airflow

10. For shutting down the container:

   ```shell
   docker-compose down --volumes --rmi all
   ```













