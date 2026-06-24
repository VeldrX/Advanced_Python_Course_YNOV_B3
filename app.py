from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from logger_config import get_logger


from product_repository import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)

import sentry_sdk
from dotenv import load_dotenv
import os

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("DSN"),
    send_default_pii=True,
)

logger = get_logger("API_logger")
logger.info("API is Running Successfully")


app = Flask(__name__)
CORS(app)

api = Api(
    app,
    version="1.0",
    title="API Produits",
    description="API Python Flask connectée à MySQL/phpMyAdmin",
    doc="/swagger",
)

product_namespace = api.namespace(
    "products",
    description="Gestion des produits",
)

product_model = api.model(
    "Product",
    {
        "nom": fields.String(required=True, description="Nom du produit", example="Clavier"),
        "prix": fields.Float(required=True, description="Prix du produit", example=49.99),
        "stock": fields.Integer(required=True, description="Stock disponible", example=10),
    },
)

product_response_model = api.model(
    "ProductResponse",
    {
        "id": fields.Integer(description="Identifiant du produit", example=1),
        "nom": fields.String(description="Nom du produit", example="Clavier"),
        "prix": fields.Float(description="Prix du produit", example=49.99),
        "stock": fields.Integer(description="Stock disponible", example=10),
    },
)


@api.route("/")
class Home(Resource):
    def get(self):
        logger.info("Route GET / appelée")
        return {"message": "API Python connectée à MySQL avec Swagger"}


@product_namespace.route("")
class ProductList(Resource):
    @product_namespace.marshal_list_with(product_response_model)
    def get(self):
        return get_all_products()

    @product_namespace.expect(product_model)
    def post(self):
        data = api.payload
        nom = data.get("nom")
        prix = data.get("prix")
        stock = data.get("stock")

        logger.info("Tentative de création produit : %s", data)
        if not nom or prix is None or stock is None:
            logger.warning("Création refusée : données manquantes")
            return {"error": "nom, prix et stock sont obligatoires"}, 400

        new_id = create_product(nom, prix, stock)
        logger.info("Produit créé : nom=%s prix=%s stock=%s", nom, prix, stock)
        return {"message": "Produit créé", "id": new_id}, 201


@product_namespace.route("/<int:product_id>")
class ProductItem(Resource):
    @product_namespace.marshal_with(product_response_model)
    def get(self, product_id):
        produit = get_product_by_id(product_id)

        if produit is None:
            api.abort(404, "Produit introuvable")

        return produit

    @product_namespace.expect(product_model)
    def put(self, product_id):
        data = api.payload
        nom = data.get("nom")
        prix = data.get("prix")
        stock = data.get("stock")

        if not nom or prix is None or stock is None:
            return {"error": "nom, prix et stock sont obligatoires"}, 400

        lignes_modifiees = update_product(product_id, nom, prix, stock)

        if lignes_modifiees == 0:
            api.abort(404, "Produit introuvable")

        return {"message": "Produit modifié"}

    def delete(self, product_id):
        lignes_supprimees = delete_product(product_id)

        if lignes_supprimees == 0:
            api.abort(404, "Produit introuvable")

        return {"message": "Produit supprimé"}


if __name__ == "__main__":
    app.run(debug=True)
