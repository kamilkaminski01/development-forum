# Development Forum

This project is aimed at developers that can create and discuss
within rooms about a development topic or problem.<br />
Users can:<br />
- register and login,<br />
- create rooms and assign an available topic or create one,<br />
- discuss in the room about the assigned topic,<br />
- search for rooms by a topic, room name or description,<br />
- edit their profile.

## Running from sources

### Clone the repository

```bash
git clone https://github.com/kamilkaminski01/development-forum
cd development-forum/
```

### Create a virtual environment
```bash
pip install virtualenv
virtualenv venv
```

### Activate the virtual environment
- #### If you are a Windows user:
    ```bash
    venv\scripts\activate
    ```
- #### If you are a Linux/MacOS user:
    ```bash
    source venv/bin/activate
    ```

### Install the dependencies and make migrations
```bash
pip install -r requirements.txt
cd app/
python manage.py migrate
```

### Run the App
```bash
python manage.py runserver
```

The app will be available at `localhost:8000` and `127.0.0.1:8000`

## Makefile

[`Makefile`](Makefile) contains common commands that UNIX users can use to make migrations,
run and test the project. The most important commands include:
- `run`: runs the project.
- `check`: performs static code checks.
- `pytest`: runs backend unit tests.
- `pytest-module module={module_name}`: runs backend unit tests in passed module
- `flush`: clears the database's data.
- `initial-data`: initializes the database with mock data.

When using a local Python environment, [`pre-commit`](https://pre-commit.com/)
should be installed and ran on staged files to ensure that the code
quality standards are met.

### Application setup

After running the application, the following actions can be executed: <br />

Stop the server with `ctrl + c` if it's running <br />
If you are a UNIX user run:
```bash
make initial-data
```
If you are a Windows user: <br />
make sure you are in the `app/` directory

```bash
python manage.py initialize_data
```
Next run the server with `python manage.py runserver`

To initialize the database with example data including:

- global superuser (admin@admin.com)
- moderator (moderator@moderator.com)
- regular users including:
  - kamil (kamil@user.com)
  - adam (adam@user.com)
  - mateusz (mateusz@user.com)
  - dorota (dorota@user.com)
  - hubert (hubert@user.com)
  - tomasz (tomasz@user.com)
- topics, rooms and replies in rooms

Every user can be logged in with its associated email and password which is by
default `Admin-123`

## Code quality standards

### Backend

All backend code must be formatted and verified by `black`, `flake8`,
`mypy` and `isort` tools. Their configurations can be found in the
[setup.cfg](app/setup.cfg) file. Additionally, `pre-commit`
[checks](.pre-commit-config.yaml) should be performed in order to verify
whitespaces, credentials, etc.

Custom functions and methods should use **type hints** to improve IDE code
completions, prevent from type errors and extend code documentation.

### Frontend

All frontend code must be formatted and verified by the `prettier`
tool.
