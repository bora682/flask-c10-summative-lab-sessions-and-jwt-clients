from config import create_app
from models import db  # ensures models are registered when app loads

app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
