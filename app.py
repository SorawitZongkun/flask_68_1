from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'flower_shop_68_1_db'
}

# Secret key for session management
app.config['SECRET_KEY'] = '54d52q2w546s574d6i7f6452s3654du65if76gad25s346d57'

@app.route('/home', methods=['GET'])
def home():
    # return "Welcome to the Home Page!"
    # from flask import jsonify
    # return jsonify({"message": "Welcome to the Home Page!"})
    name = "Anya"
    age = 10
    my_dict = {"name": "Yor", "age": "25"}
    # from flask import render_template
    return render_template('home.html', name=name, age=age, my_dict=my_dict)

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/store', methods=['POST'])
def store():
    if request.method == 'POST':
        flower_name = request.form['flowerName']
        flower_price = float(request.form['flowerPrice'])
        flower_place = request.form['flowerPlace']
        flower_description = request.form['flowerDescription']

        # Connect to MySQL database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert data into the database
        query = "INSERT INTO flowers (flower_name, flower_price, flower_place, flower_description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (flower_name, flower_price, flower_place, flower_description))

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

        # Set success message in session
        session['alert_status'] = 'success'
        session['alert_message'] = 'Flower added successfully!'
        return redirect('/')
    else:
        session['alert_status'] = 'error'
        session['alert_message'] = 'Invalid request method.'
        return redirect('/')

@app.route('/', methods=['GET'])
def index():
    # Connect to MySQL database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # Fetch all flowers from the database
    cursor.execute("SELECT * FROM flowers")
    flowers = cursor.fetchall()

    print(flowers)  # Debugging: Print fetched flowers to console

    # Close connection
    cursor.close()
    conn.close()

    # Show alert message if exists
    if 'alert_status' in session and 'alert_message' in session:
        alert_message = {
            'status': session['alert_status'],
            'message': session['alert_message']
        }
        del session['alert_status']
        del session['alert_message']
    else:
        alert_message = {
            'status': None,
            'message': None
        }
        
    return render_template('index.html', flowers=flowers, alert_message=alert_message)

@app.route('/edit/<int:flower_id>', methods=['GET'])
def edit(flower_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # Fetch the flower from the database
    cursor.execute("SELECT * FROM flowers WHERE id = %s", (flower_id,))
    flower = cursor.fetchone()

    # Close connection
    cursor.close()
    conn.close()

    return render_template('edit.html', flower=flower)

@app.route('/update/<int:flower_id>', methods=['POST'])
def update(flower_id):
    if request.method == 'POST':
        flower_name = request.form['flowerName']
        flower_price = float(request.form['flowerPrice'])
        flower_place = request.form['flowerPlace']
        flower_description = request.form['flowerDescription']

        # Connect to MySQL database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Update the flower in the database
        query = "UPDATE flowers SET flower_name = %s, flower_price = %s, flower_place = %s, flower_description = %s WHERE id = %s"
        cursor.execute(query, (flower_name, flower_price, flower_place, flower_description, flower_id))

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

        # Set success message in session
        session['alert_status'] = 'success'
        session['alert_message'] = 'Flower updated successfully!'
        return redirect('/')
    else:
        session['alert_status'] = 'error'
        session['alert_message'] = 'Invalid request method.'
        return redirect('/')
    
@app.route('/delete/<int:flower_id>', methods=['GET'])
def delete(flower_id):
    # Connect to MySQL database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # Delete the flower from the database
    query = "DELETE FROM flowers WHERE id = %s"
    cursor.execute(query, (flower_id,))

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

    # Set success message in session
    session['alert_status'] = 'success'
    session['alert_message'] = 'Flower deleted successfully!'
    return redirect('/')


if __name__ == '__main__':
    # app.run() # production
    app.run(debug=True) # development