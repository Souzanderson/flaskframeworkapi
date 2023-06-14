from os import environ
'''ENVIRONMENT APP'''
ENVIRONMENT = environ.get("FLASK_ENV") or "production"

SERVER_NAME = "FLASK PATTERN"
SERVER_VERSION = "1.0.0"

'''DATABASE SETTINGS'''
DB_SETTINGS = {
    "development": {
        "host": "localhost",
        "port": "3306",
        "user": "root",
        "passwd": "12345",
        "database": "test_table"
    },
    "production": {
        "host": "localhost",
        "port": "3306",
        "user": "root",
        "passwd": "12345",
        "database": "test_table"
    }
}