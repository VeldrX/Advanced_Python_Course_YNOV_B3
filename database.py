import mysql.connector
# On importe le connecteur MySQL pour permettre à Python de communiquer avec la base de données.

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="magasin",
        port=3306
    )