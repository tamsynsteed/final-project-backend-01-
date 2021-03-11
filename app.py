from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


con = sqlite3.connect("database.db")
print("Database opened successfully")
con.execute("CREATE TABLE IF NOT EXISTS hotels (id INTEGER PRIMARY KEY AUTOINCREMENT, hotel_name TEXT NOT NULL, description TEXT NOT NULL, image1 TEXT NOT NULL, image2 TEXT NOT NULL, image3 TEXT NOT NULL, price INTEGER NOT NULL, stars INTEGER NOT NULL)")
print("hotels table created successfully")

con.execute("CREATE TABLE IF NOT EXISTS users (person_id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, mobile_number INTEGER, email TEXT, password TEXT)")
print("hotels table created successfully")


con.execute("CREATE TABLE IF NOT EXISTS bookings(booking_id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, hotel_id INTEGER, fullname TEXT, email TEXT, hotel_name TEXT, checkin TEXT, checkout TEXT, days TEXT, guests TEXT, rooms TEXT, price INTEGER, total_cost INTEGER)")

print("bookings table created successfully")





@app.route('/add-user/', methods=["POST"])
def new_user():
    if request.method == "POST":
        msg = None
        try:
            data = request.get_json()
            fullname = data['fullname']
            mobile_number = data['mobile_number']
            email = data['email']
            password = data['password']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT into users (fullname,mobile_number,email,password) VALUES (?,?,?,?)",
                            (fullname,mobile_number,email,password))
                con.commit()
                msg = fullname + " " + "was succcessfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred:" + str(e)
        finally:
            con.close()
            return jsonify(msg=msg)

@app.route("/show-users/")
def showusers():
    data= []
    try:
        con = sqlite3.connect("database.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("select * from users")
        data = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("error fetching data")
    finally:
        con.close()
        return jsonify(data)

@app.route("/sign-in/", methods=["POST"])
def signin():

    if request.method=='POST':
        post_data = request.get_json()
        email = post_data['email']
        password = post_data['password']

        connection = sqlite3.connect('database.db')
        connection.row_factory = dict_factory
        cursor=connection.cursor()
        getResult = []
        try:
            query = "SELECT * FROM users WHERE email='{0}' AND password='{1}'".format(email, password)
            cursor.execute(query)
            getResult = cursor.fetchone()
        except Exception as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            connection.close()
        finally:
            connection.close()
            return jsonify(getResult)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails/", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            post_data = request.get_json()
            hotel_name = post_data["hotel_name"]
            description = post_data["description"]
            image1 = post_data["image1"]
            image2 = post_data["image2"]
            image3 = post_data["image3"]
            price = post_data["price"]
            stars = post_data["stars"]

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into hotels (hotel_name, description, image1, image2, image3, price, stars) values (?,?,?,?,?,?,?)", (hotel_name, description, image1, image2, image3, price, stars))
                con.commit()
                msg = "Hotel successfully Added"
        except:
            con.rollback()
            msg = "We can not add the hotel to the list"
        finally:
            con.close()
            return jsonify(post_data)


@app.route("/view/")
def view():
    data= []
    try:
        con = sqlite3.connect("database.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("select * from hotels")
        data = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("error fetching data")
    finally:
        con.close()
        return jsonify(data)


@app.route('/show-hotel-item/<int:data_id>/', methods=['GET'])
def show_hotel_item(data_id):
    data = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM hotels WHERE id=" + str(data_id))
            data = cur.fetchone()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return jsonify(data)


@app.route("/delete")
def delete():
    return render_template("delete.html")




@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("database.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from hotels where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return jsonify(msg)


@app.route("/update")
def update():
    return render_template("update.html")


@app.route("/updaterecord", methods=["POST"])
def updaterecord():
    id = request.form["id"]
    with sqlite3.connect("database.db") as con:
        try:
            cur = con.cursor()
            cur.execute("UPDATE hotels SET image1 = 'http://127.0.0.1:5500/assets/images/cards/card.jpeg' WHERE id = ?", id)
            msg = "record successfully updated"
        except:
            msg = "can't be updated"
        finally:
            return render_template("update.html", msg=msg)


@app.route('/show-booking/', methods=["GET"])
def show_booking():
    data = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute('SELECT * FROM bookings')
            data = cur.fetchall()
            print("booking added added")

    except Exception as e:
        con.rollback()
        print("There was an error fetching bookings:" + str(e))

    finally:
        con.close()
        return jsonify(data)


@app.route('/add-booking/', methods=["POST"])
def new_booking():
    if request.method == "POST":
        msg = None
        try:
            data = request.get_json()

            person_id = data['user_id']
            hotel_id = data['hotel_id']
            fullname = data['fullname']
            email = data['email']
            hotel = data['hotel']
            checkin = data['checkin']
            checkout = data['checkout']
            days= data['days_stay']
            guests = data['guests']
            rooms = data['rooms']
            price = data['price']
            total_cost = data['total_cost']


            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT into bookings (person_id,hotel_id, fullname, email, hotel_name, checkin, checkout, days, guests, rooms, price, total_cost) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                            (person_id, hotel_id, fullname, email, hotel, checkin, checkout, days, guests, rooms, price, total_cost))
                con.commit()
                msg = "Booking was successfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred:" + str(e)
        finally:
            con.close()
            return jsonify(msg=msg)


@app.route('/delete-data/<int:data_id>/', methods=["GET"])
def delete_data(data_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM hotels WHERE id=" + str(data_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
    return jsonify(msg)




if __name__ == '__main__':
    app.run(debug=True)
