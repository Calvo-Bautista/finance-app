from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

class Database:
    client: AsyncIOMotorClient = None

    def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        print("✅ Conectado a MongoDB")

    def close(self):
        if self.client:
            self.client.close()
            print("🛑 Conexión a MongoDB cerrada")

    def get_db(self):
        return self.client[settings.DATABASE_NAME]

db = Database()

# Función auxiliar para obtener la colección (útil para inyección de dependencias más adelante)
async def get_database():
    return db.get_db()