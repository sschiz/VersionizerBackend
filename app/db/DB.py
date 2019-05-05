import motor.motor_asyncio


class DataBase:
    def __init__(self, server, port):
        self.date_base = motor.motor_asyncio.AsyncIOMotorClient(server, port)["VersionizerDB"]

    async def get_products_collection(self):
        return self.date_base["products"]