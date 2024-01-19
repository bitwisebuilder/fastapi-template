# FastAPI Skeleton

## Table of Contents

- [Getting the skeleton up and running](#getting-the-skeleton-project-up-and-running)
- [API Versioning](#api-versioning)
- [Healthcheck Endpoints](#healthcheck-endpoints)
- [SQLAlchemy Integration](#sqlalchemy-integration)
- [Alembic Integration](#alembic-integration)
- [Celery](#celery)
- [Pre-Commit Integration](#pre-commit-integration)
- [Dockerfile](#dockerfile)

## Getting the skeleton project up and running

This section covers the initial setup for the FastAPI skeleton, including the installation
of necessary tools and starting the server.

### Installing Poetry

Poetry is used for dependency management in this project. To install Poetry:
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### Installing Docker and docker compose

Docker and Docker Compose are required to containerize the application and its services.
Follow the instructions on the official Docker website to install them on your machine.

### Starting the DB and RabbitMQ

```shell
docker compose up
```

### Running the FastAPI server

#### Using Uvicorn

```shell
uvicorn main:app --reload
```

#### Using Gunicorn
```shell
gunicorn -c gunicorn_config.py main:app
```

> Running the server via `gunicorn` won't reload the server on code change.

### Running the celery task

```shell
celery -A conf._celery.app.celery_app worker --loglevel=info
```

### Adding a new dependency

To add a new dependency to the project:
```shell
poetry add <package-name>
```

### Removing a dependency

To remove a new dependency from the project:
```shell
poetry remove <package-name>
```

### Adding a new dev dependency

To add a new dependency to the project:
```shell
poetry add -G dev <package-name>
```

### Removing a dev dependency
To remove a new dependency from the project:
```shell
poetry remove <package-name>
```

## API Versioning

### cms

The directory `cms` represents a resource in the backend server. By **resource**,
I mean collection of tables that are somehow related from the business context.

For the requirements the endpoints have been made such as `/api/v1/videos/` else it would
have made more sense to have endpoints like `/cms/v1/videos/`, `/cms/v2/videos/`.

### Model

A table in the database is termed as a model. All related helpers and the util functions
have been kept in a single directory. For example, `cms/videos` contains all the related
utils, helpers and DB related methods in a single directory `videos`.

#### crud.py

CRUD houses methods to perform all kind of DB operations in the API Server related to
that specific model i.e. all the related DB operations have been put in `/cms/videos/crud.py`

#### helpers.py

All the helper methods are housed in `helpers.py`. For this skeleton, I have put methods to
upload the file in the s3 bucket.

#### models.py

All the related tables are defined here in the `models.py`. A question might be, why it is
`models.py` and not `model.py`. The primary reason for it, is to allow us to define more
closely related models together. Ex. if we had to store the video likes as well, having
another directory as `/cms/video_likes/` won't make more sense, as it is not big of a
functionality, rather we can define the model `VideoLike` in the same `models.py` itself.

#### tasks.py

As the name suggests, all the background tasks, or async jobs that has to run via `celery`
will be put here. In this skeleton we have a single dummy job `process.file`.

Let's head to the `v1` directory.

In this skeleton we are versioning the `routes` and the `schemas`. Let's have a look at them.

### v1

#### routes.py

All the routes are defined here in this file related to the version `v1`. It is important to
note that the endpoint methods are relatively smaller, and readable. They are deliberately made
small to make the endpoints readable. As we don't have options such as defining the routes only
together in the `routes.py` like **Django**. Hence we need a solution that helps anyone reading
the code for the first time to understand it easily. So e have segrated DB related methods in
`crud.py` enabling us to reuse the methods and keep the endpoints/routes smaller and more readable.

#### schemas.py

All the schemas related with the endpoints are defined here. In all the endpoints we have a
response model attached with it. We have defined individual schemas for most of the unique
endpoints based on the usecase.

> A question might be why `get_video_or_raise_exception` is defined in the `routes.py` and
> not in the `crud.py`. So in the said method we are raising an **HTTP Exception**, since
> to have a clear saperation between what handles what, the `crud.py` should not raise any
> HTTP Exception as it's  job is to get the data from the DB and return it. Although it may
> raise and handle some DB related exceptions but not the HTTP ones.

### What to put in `v1` and what not to?

Usually with API versioning the request body and the response changes. Hence routes and schemas
are put in `v1` so if we want to extend it further, we should easily be able to do it.

#### What about `crud.py`

The basic thought behind putting this in `videos` and not in `v1` was that the methods defining
the crud operations usually won't change with the API versions.

#### What about `tasks.py`

Again, going with the same philosophy, have not put `tasks.py` in the `v1`.

> There is no hard and fast rules for putting things in `v1` and not putting it. But we have to
> ensure that we follow a guideline that is clear and defines what we want to version and what
> we don't want to. There is no one stopping us to do so based on our usecase. Also, `models.py`
> can never be versioned as the alembic will be confused on what the original version of the
> model is.

## Healthcheck Endpoints

A simple healthcheck endpoint is defined in `healthcheck/routes.py`. Based on our usecase we
can add more such endpoints.

## SQLAlchemy Integration

All the configurations related to the SQLAlchemy is hosted at `conf/db/`.

### models.py

We have defined `SessionLocal` and the `Model`. As per the usual convention we call it `Base`.
But for the sake of understanding it I have called it a `Model` and not a `Base` as `Model`
is more definitive and gives a sense of it being related with the `Model` from `MVC` or `MVT`
pattern.

### dependencies.py

Have defined two methods which are dependencies for either the endpoints/routes or the
celery workers.

#### get_db()

`get_db()` is used as a dependency in the endpoints to allow it to interact with the DB.
It creates a DB connection when the endpoint is called and closes the connection upon the
connection termination. It is often used as below.

```python
db: Session = Depends(get_db)
```

#### with_db_session()

`with_db_session()` is used as a decorator in the celery tasks to allow it to interact with
the DB. It creates a DB connection when the tasks is pulled from the `RabbitMQ` and closes
the connection upon the task execution. It is often used as below.

```python
@celery_app.task(bind=True, name="process.file")
@with_db_session
def task_name(self, video_id: int, db: Session):
    pass
```

We have passed `bind=True` to allow the possibility of implementing retries and hence the
first argument is `self` and not the param `video_id`, the last param is `db` which is
injected via this decorator. It is not passed when calling the celery task.

We call the celery task as below:

```python
task_name.delay(2)
```

And celery puts the task in `RabbitMQ` and a separate worker pulls it from the queue for
executing it.

> We cannot pass an active DB connection object to a celery task, as it only accepts the
> primitive data types.

## Alembic Integration

The directory `migrations` and `alembic.ini` contain the configurations related with the
`alembic`.

### Creating New Migration

```shell
alembic revision -m "Add new column to videos table"
```

The above command  will generate a new file under `migrations` directory. And we have to
add the operation in `upgrade()` method and the `downgrade()` method.

#### `upgrade()`

We define what change we want in the new migration.

```python
def upgrade() -> None:
    pass
```

#### `downgrade()`

We define how it may be reverted.

```python
def downgrade() -> None:
    pass
```

### Applying New Migration

```shell
alembic upgrade head
```

Running the above command in the terminal will actually run the migration
defined above.

## Celery

All the configurations related to the SQLAlchemy is hosted at `conf/_celery/`.

### app.py

We have defined the `celery_app` in this file itself. We have to use the same `celery_app`
when defining a celery task.

## Pre-Commit Integration

`pre-commit` hook has been added in the skeleton. To enable it run the  bellow command.

```shell
pre-commit install
```

After running the above command, whenever we will run `git commit ...` the `pre-commit`
hook will automatically try to lint the project. And it will also try to fix a few of
the issues based on the rules defined in the `.pre-commit-config.yaml`.

We also export the non-development related dependencies from poetry to `requirements.txt`

## Dockerfile

It is a two stage based dockerfile. The first stage installs the dependencies and the
second stage simply copies the dependencies from the first stage and makes it runable.

Have added a template of multistage so that later we can update the first stage to
build smaller docker images and fasten the whole process.

> It is worth noting that we are not using poetry in the `Dockerfile` as to fasten the
> process by installing the dependencies and keep the generated image smaller.
>
> PS: It is tested in production :P
