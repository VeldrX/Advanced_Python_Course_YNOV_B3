from database import get_connection


def get_all_products():
    connexion = get_connection()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT id, nom, prix, stock FROM produits")
    produits = curseur.fetchall()
    curseur.close()
    connexion.close()
    return produits
    

def get_product_by_id(product_id):
    connexion = get_connection()
    curseur = connexion.cursor(dictionary=True)
    sql = "SELECT id, nom, prix, stock FROM produits WHERE id = %s"
    curseur.execute(sql, (product_id,))
    produit = curseur.fetchone()
    curseur.close()
    connexion.close()
    return produit


def create_product(nom, prix, stock):
    connexion = get_connection()
    curseur = connexion.cursor()
    sql = "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)"
    valeurs = (nom, prix, stock)
    curseur.execute(sql, valeurs)
    connexion.commit()
    new_id = curseur.lastrowid
    curseur.close()
    connexion.close()
    return new_id


def update_product(product_id, nom, prix, stock):
    connexion = get_connection()
    curseur = connexion.cursor()
    sql = "UPDATE produits SET nom = %s, prix = %s, stock = %s WHERE id = %s"
    valeurs = (nom, prix, stock, product_id)
    curseur.execute(sql, valeurs)
    connexion.commit()
    lignes_modifiees = curseur.rowcount
    curseur.close()
    connexion.close()
    return lignes_modifiees


def delete_product(product_id):
    connexion = get_connection()
    curseur = connexion.cursor()
    sql = "DELETE FROM produits WHERE id = %s"
    curseur.execute(sql, (product_id,))
    connexion.commit()
    lignes_supprimees = curseur.rowcount
    curseur.close()
    connexion.close()
    return lignes_supprimees
