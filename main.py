from flask import Flask
from data_model import Base
from actions_data import engine
from routes import app as routes_app

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.register_blueprint(routes_app)


if __name__ == "__main__":
    app.run(debug=True)