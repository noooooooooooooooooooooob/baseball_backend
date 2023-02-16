from app.api import user
from config import app
from app.swagger import user_api


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

