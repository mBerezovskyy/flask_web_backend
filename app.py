import json

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
mysql = MySQL(app)
CORS(app)


with open('credentials.json') as credentials:
    credentials_data = json.load(credentials)
    MYSQL_HOST = credentials_data['MYSQL_HOST']
    PORT = credentials_data['PORT']
    MYSQL_USER = credentials_data['MYSQL_USER']
    MYSQL_PASSWORD = credentials_data['MYSQL_PASSWORD']
    MYSQL_DB = credentials_data['MYSQL_DB']
    MYSQL_CURSORCLASS = credentials_data['MYSQL_CURSORCLASS']

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['PORT'] = PORT
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = MYSQL_CURSORCLASS


@app.route('/switchblade', methods=['GET'])
def get_all_switchblades():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM switchblade')
    all_switchblades = cursor.fetchall()

    return jsonify(all_switchblades), 200


@app.route('/switchblade/<id>', methods=['GET'])
def get_single_switchblade(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM switchblade WHERE id =%s',
        [id])
    switchblade = cursor.fetchone()

    return jsonify(switchblade), 200


@app.route('/switchblade', methods=['POST'])
def add_switchblade():
    cursor = mysql.connection.cursor()

    json_data = request.json
    name_of_product = json_data['name_of_product']
    price_in_uah = json_data['price_in_uah']
    producing_country = json_data['producing_country']
    quantity_in_one_package = json_data['quantity_in_one_package']

    cursor.execute(
        'INSERT INTO switchblade(name_of_product, price_in_uah, producing_country, quantity_in_one_package)'
        ' VALUES(%s, %s, %s, %s)', [name_of_product, price_in_uah, producing_country, quantity_in_one_package])
    mysql.connection.commit()

    return jsonify(
        {'name_of_product': name_of_product, 'price_in_uah': price_in_uah, 'producing_country': producing_country,
         'quantity_in_one_package': quantity_in_one_package}), 201


@app.route('/switchblade/<id>', methods=['PUT'])
def update_axe(id):
    cursor = mysql.connection.cursor()

    json_data = request.json
    name_of_product = json_data['name_of_product']
    price_in_uah = json_data['price_in_uah']
    producing_country = json_data['producing_country']
    quantity_in_one_package = json_data['quantity_in_one_package']

    cursor.execute(
        'UPDATE switchblade SET name_of_product = %s, price_in_uah = %s, producing_country = %s, '
        'quantity_in_one_package = %s WHERE id = %s',
        [name_of_product, price_in_uah, producing_country, quantity_in_one_package, id])
    mysql.connection.commit()

    return jsonify(
        {'name_of_product': name_of_product, 'price_in_uah': price_in_uah, 'producing_country': producing_country,
         'quantity_in_one_package': quantity_in_one_package}), 200


@app.route('/switchblade/<id>', methods=['DELETE'])
def delete_axe(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM switchblade WHERE id = %s', [id])
    mysql.connection.commit()

    return jsonify(), 204


if __name__ == '__main__':
    app.run(debug=True)
