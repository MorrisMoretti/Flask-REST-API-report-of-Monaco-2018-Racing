import os


class Config:
    DEBUG = os.getenv("DEBUG", True)
