from app.core.database import db 

async def init_db():
    await db.user.create_index("email", unique = True)