#!/usr/bin/env python3
from flask import Flask, render_template
import draft

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    foil_cards, cards = draft.generate_pack("ktk")
    return render_template('pack.html', foil_cards=foil_cards, cards=cards)

if __name__ == '__main__':
    app.run()
