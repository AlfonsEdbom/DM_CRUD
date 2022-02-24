from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# function for connecting to db
def connectToDB():
    connectionString = 'dbname=lab2 user=postgres port=5432 host=localhost'
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

# first page, "home page"
@app.route("/")
def home():
    return render_template("index.html")

#########################################################
####### display pages for all or individual pages #######
#########################################################

# display all tables in db etc
@app.route("/all_tables")
def all_tables():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM people')
        results = dict_cur.fetchall()
        dict_cur.execute('SELECT * FROM snacks')
        results1 = dict_cur.fetchall()
        dict_cur.execute('SELECT * FROM snacks_at_home')
        results2 = dict_cur.fetchall()
        dict_cur.close()
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
    #results = dict_cur.fetchall()
    return render_template("all_tables.html", people=results, snacks=results1, snacks_at_home=results2)


# display categories table etc
@app.route("/people")
def people():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM people')
        results = dict_cur.fetchall()
        dict_cur.close()
    except:
        print('could not execute query')
    #results = dict_cur.fetchall()
    finally:
        if conn is not None:
            conn.close()
    return render_template("people.html", people=results)


@app.route("/snacks")
def snacks():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM snacks')
        results = dict_cur.fetchall()
        dict_cur.close()
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
    return render_template("snacks.html", snacks=results)


@app.route("/snacks_at_home")
def snacks_at_home():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT * FROM snacks_at_home')
        results = dict_cur.fetchall()
        dict_cur.close() 
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
    return render_template("snacks_at_home.html", snacks_at_home=results)

###########################################
####### functions for adding tuples #######
###########################################

@app.route("/people/add", methods=["POST"])
def add_people():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        dict_cur.execute("INSERT INTO people (fname, lname, email) VALUES (%s, %s, %s)",
        (fname, lname, email))
        
        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/people")

@app.route("/snacks/add", methods=["POST"])
def add_snacks():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        snack_name = request.form['snack_name']
        cost = request.form['cost']

        dict_cur.execute("INSERT INTO snacks (snack_name, cost) VALUES (%s, %s)",
        (snack_name, cost))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/snacks")

@app.route("/snacks_at_home/add", methods=["POST"])
def add_snacks_at_home():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        person = int(request.form['person'])
        snack = int(request.form['snack'])
        amount = int(request.form['amount'])

        dict_cur.execute("INSERT INTO snacks_at_home (person, snack, amount) VALUES (%s, %s, %s)",
        (person, snack, amount))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/snacks_at_home")

#############################################
####### functions for updating tuples #######
#############################################

@app.route("/people/update", methods=["POST"])
def update_people():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        person_id = int(request.form['person_id'])
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        dict_cur.execute("UPDATE people SET fname = %s, lname = %s, email = %s WHERE person_id = %s", 
        (fname, lname, email, person_id))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/people")

@app.route("/snacks/update", methods=["POST"])
def update_snacks():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        snack_id = int(request.form['shipper_id'])
        snack_name = request.form['company_name']
        cost = request.form['phone']

        dict_cur.execute("UPDATE snacks SET snack_name = %s, cost = %s WHERE snack_id = %s", 
        (snack_name, cost, snack_id))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/snacks")


@app.route("/snacks_at_home/update", methods=["POST"])
def update_snacks_at_home():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        person = int(request.form['person'])
        snack = request.form['snack']
        amount = request.form['amount']

        dict_cur.execute("UPDATE snacks_at_home SET snack = %s, amount = %s WHERE person = %s", 
        (snack, amount, person))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/snacks_at_home")
    
#############################################
####### functions for deleting tuples #######
#############################################

@app.route("/shippers/delete", methods=["POST"])
def delete_shipper():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        shipper_id = request.form['shipper_id']

        dict_cur.execute("DELETE FROM shippers WHERE shipper_id = %s", 
        (shipper_id,))

        conn.commit()
        dict_cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return redirect("/shippers")

#####################################
####### look at state regions #######
#####################################

@app.route("/us_states/query", methods=['POST'])
def query_us_states():
    conn = None
    try:
        conn = connectToDB()
        dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        state_region = request.form['state_region']
        print(state_region)
        if state_region == ('all') or state_region == ('All'):
            dict_cur.execute("SELECT * FROM us_states")
            results = dict_cur.fetchall()
            dict_cur.close()
        else:
            dict_cur.execute("SELECT * FROM us_states WHERE state_region = %s", (state_region,))
            results = dict_cur.fetchall()
            dict_cur.close()
    except:
        print('could not execute query')
    finally:
        if conn is not None:
            conn.close()
            
    return render_template("us_states.html", us_states=results)


if __name__ == "__main__":
    app.run(debug=True)