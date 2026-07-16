import os


class Config:
    """
    Base configuration for the CoProT application.
    """

    # Secret key used for sessions and security
    SECRET_KEY = "coprot-secret-key"

    # SQLite database location
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/coprot.db"

    # Disable unnecessary tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False