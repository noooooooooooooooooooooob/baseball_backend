from flask_cors import CORS
from app.api import user
from config import app

app.register_blueprint(user.userBlueprint)

CORS(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

