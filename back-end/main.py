from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from models.template import Template
from models.message import Message
from models.platform import Platform
from models.sender import Sender
import asyncpg, logging

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


@app.get("/platforms", response_model=List[Platform])
async def get_platforms():
    async with app.state.pool.acquire() as connection:
        query = "SELECT * FROM platform"
        rows = await connection.fetch(query)
    platforms = [Platform(id=row["id"], name=row["name"]) for row in rows]
    return platforms


@app.get("/senders", response_model=Dict[Platform, List[Sender]])
async def get_senders():
    async with app.state.pool.acquire() as connection:
        try:
            query = """SELECT s.id as s_id, s.name as s_name, s.platform as s_platform, p.id as p_id, p.name as p_name 
                        FROM sender s 
                        JOIN platform p ON p.id = s.platform;"""
            rows = await connection.fetch(query)
            result = {}
            for row in rows:
                platform = Platform(id=row["p_id"], name=row["p_name"])
                sender = Sender(id=row["s_id"], name=row["s_name"], platform=row["s_platform"])
                if platform not in result:
                    result[platform] = [sender]
                else:
                    result[platform].append(sender)
            return result
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/templates", response_model=List[Template])
async def get_templates():
    async with app.state.pool.acquire() as connection:
        query = "SELECT * FROM template"
        rows = await connection.fetch(query)
    templates = [
        Template(id=row["id"], name=row["name"], template=row["template"])
        for row in rows
    ]
    return templates


@app.post("/send-message")
async def send_message(message: Message):
    async with app.state.pool.acquire() as connection:
        try:
            query = """INSERT INTO message (platform, receiver, url_receiver, message_content, already_connected, change_position, follow_candidate) 
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        RETURNING id, platform, receiver, url_receiver, message_content, already_connected, change_position, follow_candidate"""
            record = await connection.fetchrow(
                query,
                message.platform,
                message.receiver,
                message.url_receiver,
                message.message_content,
                message.already_connected,
                message.change_position,
                message.follow_candidate,
            )
            print("Record:", record)
            if not record:
                raise HTTPException(status_code=500, detail="Failed to insert item.")
            return Message(
                id=record["id"],
                platform=record["platform"],
                receiver=record["receiver"],
                urlReceiver=record["url_receiver"],
                messageContent=record["message_content"],
                alreadyConnected=record["already_connected"],
                changePosition=record["change_position"],
                followCandidate=record["follow_candidate"],
            )
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-template")
async def create_template(template: Template):
    async with app.state.pool.acquire() as connection:
        try:
            query = """INSERT INTO template (name, template)
                        VALUES ($1, $2)
                        RETURNING id, name, template"""
            record = await connection.fetchrow(query, template.name, template.template)
            return Template(
                id=record["id"], name=record["name"], template=record["template"]
            )
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))


@app.put("/edit-template/{template_id}")
async def update_template(template_id: int, new_template: Template):
    async with app.state.pool.acquire() as connection:
        try:
            query = """UPDATE template
                       SET name = $1, template = $2
                       WHERE id = $3
                       RETURNING id, name, template"""
            record = await connection.fetchrow(
                query, new_template.name, new_template.template, template_id
            )
            if not record:
                raise HTTPException(status_code=404, detail="Template not found.")
            return Template(
                id=record["id"], name=record["name"], template=record["template"]
            )
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))
