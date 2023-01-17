import config
from web_report.app import app

if __name__ == '__main__':
    app.config.from_object(config.Config)
    app.run()
