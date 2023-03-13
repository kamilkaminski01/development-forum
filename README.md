# Development Forum

This project is aimed at developers that can create and discuss
within rooms about a development topic or problem.
Users can:
- register and login,
- create rooms about a chosen development topic,
- discuss in the room,
- search rooms about a desired topic.

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

### Install the dependencies
```bash
pip install -r requirements.txt
```

### Run the App
```bash
cd app/
python manage.py runserver
```

The app will be available at `localhost:8000` and `127.0.0.1:8000`
