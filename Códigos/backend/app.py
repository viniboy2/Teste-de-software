from flask import Flask
from database.db import db
from routes.auth_routes import auth_bp
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)