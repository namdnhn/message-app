from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "sentry-trace", "baggage"],
)

DATABASE_URL = "postgresql://postgres:12341234@localhost:5432/messageapp"


async def create_connection_pool():
    return await asyncpg.create_pool(DATABASE_URL)


@app.on_event("startup")
async def startup_event():
    app.state.pool = await create_connection_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.pool.close()


@app.get("/platforms")
async def read_platforms():
    async with app.state.pool.acquire() as connection:
        query = "SELECT * FROM platform"
        rows = await connection.fetch(query)
        return [row["name"] for row in rows]


@app.get("/senders")
async def get_senders():
    async with app.state.pool.acquire() as connection:
        query = "SELECT s.name as s_name, p.name as p_name FROM sender s JOIN platform p ON p.id = s.platform;"
        rows = await connection.fetch(query)
        result = {}
        for row in rows:
            platform = row["p_name"]
            sender = row["s_name"]
            if platform not in result:
                result[platform] = [sender]
            else:
                result[platform].append(sender)
        return result


@app.get("/templates")
async def get_templates():
    async with app.state.pool.acquire() as connection:
        query = "SELECT * FROM template"
        rows = await connection.fetch(query)
        return [row["name"] for row in rows]
