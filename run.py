# run.py
from project import create_app

app = create_app()

if __name__ == '__main__':
    # This command starts your Flask web server
    app.run(debug=True)