from random import randint,choice
from string import ascii_uppercase,ascii_lowercase
import sqlite3
from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import join_room,leave_room,send,SocketIO
import database_funcients as database

def random_letters(wachtwoord_items:list) -> list:
    """
    Deze functie is een onderdeel van de sterk_wachtwoord functie.
    """
    for _ in range(randint(1,99)):
        if randint(1,2) == 1:
            wachtwoord_items.append(choice(ascii_uppercase))
            if randint(1,2) == 1:
                wachtwoord_items.append(choice(ascii_uppercase))
            else:
                wachtwoord_items.append(choice(ascii_lowercase))
        else:
            wachtwoord_items.append(choice(ascii_lowercase))
            if randint(1,2) == 1:
                wachtwoord_items.append(choice(ascii_uppercase))
            else:
                wachtwoord_items.append(choice(ascii_lowercase))
    return wachtwoord_items

# functie om de secret key te generaten
def sterk_wachtwoord() -> str:
    """
    Deze functie maakt een random secret key.
    """
    wachtwoord:str = ''
    wachtwoord_items:list = []

    for _ in range(randint(1,999)):
        random_letters(wachtwoord_items)

    for _ in range(8):
        random_letters(wachtwoord_items)

    if randint(1,10) > 7:
        random_letters(wachtwoord_items)

    for _ in range(5):
        random_letters(wachtwoord_items)

    if randint(1,20) == randint(1,20):
        random_letters(wachtwoord_items)

    for _ in range(5):
        random_letters(wachtwoord_items)

    if randint(1,2) == 1:
        random_letters(wachtwoord_items)

    for _ in range(11):
        random_letters(wachtwoord_items)

    wachtwoord_items.append(str(randint(1,999999999)))

    for _ in range(3):
        random_letters(wachtwoord_items)

    for wachtwoord_item in wachtwoord_items:
        wachtwoord += wachtwoord_item

    return wachtwoord

app = Flask(__name__)
app.config["SECRET_KEY"] = sterk_wachtwoord()
socketio = SocketIO(app)

rooms:dict = {}

def generate_unique_code(length:int) -> str:
    """
    Args:
        length (int)
    
    Deze functie geeft een random room code die nog niet bestaat in de rooms lijst.

    Returns:
        code (int)
    """
    while True:
        code:str = ""
        for _ in range(length):
            code += choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@app.route("/login", methods=["POST","GET"])
def login():
    session.clear()
    if request.method == "POST":
        naam:str = request.form.get("naam")
        wachtwoord:str = request.form.get("wachtwoord")

        conn:sqlite3.Connection = database.connect_to_database()
        cur:sqlite3.Cursor = conn.cursor()

        cur.execute("SELECT * FROM gebruikers WHERE naam=? AND wachtwoord=?",(naam,wachtwoord))

        database_wachtwoord:tuple = cur.fetchone()
        database_wachtwoord:str = database.query_to_wachtwooord(database_wachtwoord)

        if database_wachtwoord == wachtwoord:
            session["naam"] = naam
            database.close_connection(conn)

        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/create_acount", methods=["POST","GET"])
def create_acount():
    session.clear()
    if request.method == "POST":
        naam:str = request.form.get("gebruikersnaam")
        wachtwooord:str = request.form.get("wachtwoord")

        # email:str = request.form.get("email")
        # verzend verfie email
        # wanneer link in de email is geclickt dan:
        conn = database.connect_to_database()

        # if verfie email send succesfull:
          # database.voeg_email_toe(conn,email)
        # als op de link in de email wordt geclickt dan:

        database.voeg_gebruikers_toe(conn,naam,wachtwooord)
        database.close_connection(conn)

    return render_template('create_acount.html')

@app.route("/")
def redirect_route():
    """Redirect logica om niet ingelogde gebruikers naar de login pagina te redirecten."""
    if session is not None:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        naam:str = request.form.get("naam")
        code:str = request.form.get("code")
        room_id:str = request.form.get("room_id")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if naam == "":
            try:
                naam = session["naam"]
            except ValueError:
                return render_template("home.html", error="Please enter a naam.", code=code, name=naam)

        if not naam:
            return render_template("home.html", error="Please enter a naam.", code=code, name=naam)
        if join is not False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=naam)

        room = code

        if create is not False:
            if room_id == "":
                room = generate_unique_code(4)
            else:
                room = room_id

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
    return render_template('doc.html')

@app.route("/room")
def room():
    room = session.get("room")

    if room is None or session.get("naam") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")

    if room not in rooms:
        return

    content = {
        "naam": session.get("naam"),
        "message": data["data"]
    }

    send(content, to=room)

    rooms[room]["messages"].append(content)

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
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
    room = session.get("room")
    naam = session.get("naam")

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"naam": naam, "message": "has left the room"}, to=room)

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",debug=True)
