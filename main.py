from flask import Flask
from data_model import Base
from actions_data import engine

Base.metadata.create_all(bind=engine)

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)