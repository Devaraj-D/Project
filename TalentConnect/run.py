import subprocess
import os

# Run the flask app in one process
flask_process = subprocess.Popen(['python', 'project2/app.py'])

# Run the django app in another process
django_process = subprocess.Popen(['python', 'manage.py', 'runserver', '8000'])
# Wait for both processes to finish (optional, if you want the script to wait until they're closed)
django_process.wait()
flask_process.wait()
