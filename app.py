#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
from collections import deque
import draft

app = Flask(__name__)
app.debug = True

open_packs = {  "ktk": {},
                "war": {}}

working_pack = {}
picks = {}

def append_pack(set_id, pick_number, pack):
    try:
        open_packs[set_id][pick_number].append(pack)
    except:
        open_packs[set_id][pick_number] = deque()
        open_packs[set_id][pick_number].append(pack)

def get_pack(set_id, pick_number):
    return open_packs[set_id][pick_number].popleft()

@app.route("/<set_id>/new")
def new_draft(set_id):
    if set_id not in open_packs:
        return "Set not supported"

    pick_number = 1
    pack = draft.generate_pack(set_id)
    working_pack[1] = pack
    append_pack(set_id, pick_number, pack)
    return redirect("/{}/pick/{}".format(set_id, pick_number))

@app.route("/<set_id>/pick/<pick_number>", methods=['GET', 'POST'])
def pick(set_id, pick_number):
    pick_number = int(pick_number)
    if working_pack.get(1) and request.form.get("pick"):
        selected = int(request.form["pick"])
        pick = working_pack[1][selected]
        picks[pick_number] = pick
        del working_pack[1][selected]
        if not working_pack[1]:
            return redirect("/{}/picks".format(set_id))

        append_pack(set_id, pick_number, working_pack[1])

    working_pack[1] = get_pack(set_id, pick_number)
    return render_template("pack.html", set_id=set_id, pick_number=pick_number, pack=working_pack[1])

@app.route("/<set_id>/picks")
def view_picks(set_id):
    return render_template("")


#@app.route("/")
#def index():
#    set_id = "war"
#    pick_number = 15
#    foil_cards, cards = draft.generate_pack(set_id)
#    return render_template('pack.html', foil_cards=foil_cards, cards=cards)



if __name__ == '__main__':
    app.run()
