import unittest
from app.product.product import Product
import asyncio
import motor.motor_asyncio


class TestProductRegisterMethod(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.product = "testing"
        self.secret = "test11"

    def test_just_register_product(self):
        response = self.loop.run_until_complete(Product.register_product(self.product, self.secret))
        c = motor.motor_asyncio.AsyncIOMotorClient()["VersionizerDB"]["products"]
        id = self.loop.run_until_complete(c.find_one({"name": self.product}))["_id"].binary.hex()

        self.loop.run_until_complete(c.delete_one({"name": self.product}))

        self.assertEqual({"result": id}, response)
    
    def test_register_existing_product(self):
        self.loop.run_until_complete(Product.register_product(self.product, self.secret))
        response = self.loop.run_until_complete(Product.register_product(self.product, self.secret))
        self.loop.run_until_complete(motor.motor_asyncio.AsyncIOMotorClient()["VersionizerDB"]["products"]
                                     .delete_one({"name": self.product}))

        self.assertEqual({"failure": True, "message": "No old_secret and secret params"}, response)
    
    def test_wrong_product_name(self):
        for name in ("a", "aaaaaaaaaaaaaaaaaaaaa", "11111", "AAAAA"):
            with self.subTest(name=name):
                self.assertEqual({
                    "failure": True,
                    "message": "Wrong name"
                }, self.loop.run_until_complete(Product.register_product(name, "12345")))
    
    def test_wrong_password(self):
        for password in ("a", "aaaaaaaaaaaaaaaaaaaaa"):
            with self.subTest(password=password):
                self.assertEqual(
                    {
                        "failure": True,
                        "message": "Wrong password"
                    }, self.loop.run_until_complete(Product.register_product("testing", password)))
