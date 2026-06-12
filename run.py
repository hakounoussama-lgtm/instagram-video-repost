import os
import logging
from app import create_app, db

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

logging.info(f'Creating app with config: {config_name}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
