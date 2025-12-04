from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def flip():
    return "HEADS" if random.random() > 0.5 else "TAILS"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
