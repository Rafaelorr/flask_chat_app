from random import randint,choice
from string import ascii_uppercase,ascii_lowercase,punctuation
from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import join_room,leave_room,send,SocketIO


def random_letters(wachtwoord_items:list) -> list:
    """
    Deze functie is een onderdeel van de sterk_wachtwoord functie.
    """
    for _ in range(randint(1,99)):
        if randint(1,2) == 1:
            wachtwoord_items.append(choice(ascii_uppercase))
            if randint(1,2) == 1:
                wachtwoord_items.append(choice(ascii_uppercase))
            if randint(1,2) == 2:
                wachtwoord_items.append(choice(ascii_lowercase))
            if randint(1,3) == 3:
                wachtwoord_items.append(choice(punctuation))
        elif randint(1,2) == 2:
            wachtwoord_items.append(choice(ascii_lowercase))
            if randint(1,2) == 1:
                wachtwoord_items.append(choice(ascii_uppercase))
            if randint(1,2) == 2:
                wachtwoord_items.append(choice(ascii_lowercase))
            if randint(1,3) == 3:
                wachtwoord_items.append(choice(punctuation))
        else:
            wachtwoord_items.append(choice(punctuation))
            if randint(1,2) == 1:
                wachtwoord_items.append(choice(ascii_uppercase))
            if randint(1,2) == 2:
                wachtwoord_items.append(choice(ascii_lowercase))
            if randint(1,3) == 3:
                wachtwoord_items.append(choice(punctuation))
            wachtwoord_items.append(choice(punctuation))
    return wachtwoord_items

def sterk_wachtwoord() -> str:
    """
    Deze functie maakt een random secret key.
    """
    wachtwoord:str = ''
    wachtwoord_items:list = []

    for _ in range(randint(1,999)):
        random_letters(wachtwoord_items)

    wachtwoord_items.append(str(randint(1,999999999)))
    for _ in range(7):
        random_letters(wachtwoord_items)

    if randint(1,10) > 7:
        random_letters(wachtwoord_items)

    for _ in range(4):
        random_letters(wachtwoord_items)

    wachtwoord_items.append(str(randint(1,999999999)))

    if randint(1,20) == randint(1,20):
        random_letters(wachtwoord_items)
        wachtwoord_items.append(str(randint(1,999999999)))

    wachtwoord_items.append(str(randint(1,999999999)))

    for _ in range(4):
        random_letters(wachtwoord_items)

    if randint(1,2) == 1:
        random_letters(wachtwoord_items)
        wachtwoord_items.append(str(randint(1,999999999)))

    for _ in range(10):
        wachtwoord_items.append(str(randint(1,999999999)))

    for _ in range(7):
        random_letters(wachtwoord_items)

    for _ in range(8):
        random_letters(wachtwoord_items)

    wachtwoord_items.append(str(randint(1,999999999)))

    for _ in range(3):
        random_letters(wachtwoord_items)

    for wachtwoord_item in wachtwoord_items:
        wachtwoord += wachtwoord_item

    return wachtwoord

app:Flask = Flask(__name__)
app.config["SECRET_KEY"] = sterk_wachtwoord()
socketio:SocketIO = SocketIO(app)

rooms:dict = {}

def generate_unique_code(length:int) -> str:
    """
    Deze functie genereert een unikie code die dient als room id als de gebruik geen room id heeft geven bij het maken van een room.
    """
    while True:
        code:str = ""
        for _ in range(length):
            code += choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

def overwrite_memory() -> None:
    """
    Deze functie wordt gebruikt om de rooms dict uit het geheugen van de server te halen.
    """
    a:list = []
    b:list = []
    for i in range(1,99999):
        if randint(1,2) ==  1:
            a.append(randint(1,9999) + i)
        b.append(randint(1,999999999999) + 2 * i)

@app.route("/")
def redrict():
    """
    Dit is de backend code voor de redrict route.
    Die functie wordt gebruik om de gebruiker de redricten naar de home route.
    """
    if session != session.clear():
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/home", methods=["POST", "GET"])
def home():
    """
    Dit is de backend code voor de home pagina.
    """
    if request.method == "POST":
        code:str = request.form.get("code")
        room_id:str = request.form.get("room_id")
        join:bool|str = request.form.get("join", False)
        create:bool|str = request.form.get("create", False)

        naam:str = "anymous"

        if join is not False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=naam)

        room:str = code

        if create is not False:
            if room_id == "":
                room:str = generate_unique_code(4)
            else:
                room:str = room_id
            if room not in rooms:
                rooms[room] = {"members": 0, "messages": []}
            elif room in rooms:
                return render_template("home.html", error="Room already exist.", code=code, name=naam)
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=naam)

        session["room"] = room
        session["naam"] = naam

        return redirect(url_for("room"))
    return render_template("home.html")

@app.route("/doc")
def doc():
    """
    Dit is de backend code voor de documentatie pagina.
    """
    return render_template('doc.html')

@app.route("/room")
def room():
    """
    Dit is de backend code van de room route.
    """
    room:str = session.get("room")

    if room is None or session.get("naam") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    """
    Deze methode wordt gebruikt om een bericht te verzenden.
    """
    room:str = session.get("room")

    if room not in rooms:
        return

    content:dict[str:any] = {
      "naam": session.get("naam"),
      "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)

@socketio.on("connect")
def connect(auth):
    """
    De methode wordt gebruikt om de gebruiker te verbinden.
    """
    room:str = session.get("room")
    naam:str = session.get("naam")

    if not room or not naam:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"naam": naam, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1

@socketio.on("disconnect")
def disconnect():
    """
    Deze methode wordt gebruikt om de gebruiker zijn verbinding te sluiten.
    """
    room:str = session.get("room")
    naam:str = session.get("naam")

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"naam": naam, "message": "has left the room"}, to=room)

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",debug=True)
    for _ in range(10):
        overwrite_memory()
