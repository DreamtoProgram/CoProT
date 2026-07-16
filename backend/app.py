from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Database object
db = SQLAlchemy()


def create_app():
    """
    Creates and configures the Flask application.
    """

    app = Flask(__name__)

    # Configuration
    app.config.from_object(Config)

    # Connect database with Flask
    db.init_app(app)

    # Temporary home route
    @app.route("/")
    def home():
        return {
            "message": "Welcome to CoProT Backend 🚀",
            "status": "Backend Running"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)