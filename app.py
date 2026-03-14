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

if __name__ == '__main__':
    # app.run() # production
    app.run(debug=True) # development