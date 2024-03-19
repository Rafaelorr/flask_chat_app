from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import join_room,leave_room,send,SocketIO
from random import randint,choice
from string import ascii_uppercase,ascii_lowercase,punctuation

def random_letters(wachtwoord_items:list) -> list:
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
    elif randint(1,3) == 3:
      wachtwoord_items.append(choice(punctuation))
      if randint(1,2) == 1:
        wachtwoord_items.append(choice(ascii_uppercase))
      if randint(1,2) == 2:
        wachtwoord_items.append(choice(ascii_lowercase))
      if randint(1,3) == 3:
        wachtwoord_items.append(choice(punctuation))
  return wachtwoord_items

# functie om de secret key te generaten
def sterk_wachtwoord() -> str:
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
  wachtwoord_items.append(choice(['snelle','trage','vuile','grappige']))
  wachtwoord_items.append(str(randint(1,999999999)))
  if randint(1,20) == randint(1,20):
    random_letters(wachtwoord_items)
    wachtwoord_items.append(str(randint(1,999999999)))
  wachtwoord_items.append(str(randint(1,999999999)))
  for _ in range(4):
    random_letters(wachtwoord_items)
  wachtwoord_items.append(choice(['blauwe','groene','gele','witte','zwarte']))
  if randint(1,2) == 1:
    random_letters(wachtwoord_items)
    wachtwoord_items.append(str(randint(1,999999999)))
  for _ in range(10):
    wachtwoord_items.append(str(randint(1,999999999)))
  for _ in range(7):
    random_letters(wachtwoord_items)
  wachtwoord_items.append(choice(['panda','held','nijlpaard','man','pikachu']))
  for _ in range(8):
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
  while True:
    code:str = ""
    for _ in range(length):
      code += choice(ascii_uppercase)
    if code not in rooms:
      break
  return code

def overwrite_memory() -> None:
  a:list = []
  b:list = []
  for i in range(1,9999999999):
    if randint(1,2) ==  1:
      a.append(randint(1,9999) + i)
    b.append(randint(1,999999999999) + 2 * i)

@app.route("/")
def redrict():
  if session != session.clear():
    return redirect(url_for("home"))
  return redirect(url_for("login"))

@app.route("/home", methods=["POST", "GET"])
def home():
  if request.method == "POST":
    naam:str = request.form.get("naam")
    if naam == "":
      return render_template("home.html", error="Please enter a naam.", code=code, name=naam)
    code:str = request.form.get("code")
    room_id:str = request.form.get("room_id")
    join = request.form.get("join", False)
    create = request.form.get("create", False)
    if not naam:
      return render_template("home.html", error="Please enter a naam.", code=code, name=naam)
    if join != False and not code:
      return render_template("home.html", error="Please enter a room code.", code=code, name=naam)
    room = code
    if create != False:
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
    "message": data["data"]}
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
  del rooms
  overwrite_memory()