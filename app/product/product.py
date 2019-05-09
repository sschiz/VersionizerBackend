from app.db import DB
import re
import bcrypt


class Product:
    pattern_of_passwords = re.compile("^.{5,20}$")
    pattern_of_name_of_product = re.compile("^[a-z,_]{5,20}$")

    @staticmethod
    async def register_product(name, password):
        if not Product.pattern_of_name_of_product.match(name):
            return {
                "failure": True,
                "message": "Wrong name"
            }
        elif not Product.pattern_of_passwords.match(password):
            return {
                "failure": True,
                "message": "Wrong password"
            }

        date_base = DB.DataBase("localhost", 27017)
        products = await date_base.get_products_collection()

        if await products.count_documents({"name": name}) > 0:
            return {
                "failure": True,
                "message": "No old_secret and secret params"
            }

        result = await products.insert_one({"name": name, "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')})
        id = result.inserted_id.binary.hex()

        return {"result": id}
