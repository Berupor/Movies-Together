import json
import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis
from pydantic.json import pydantic_encoder

from core.config import settings
from chat_service.src.db import redis_cache
from redis.asyncio import Redis
from models.chat import Chat, Messege

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="API for group chat",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

active_connections = set()
redis_conn = Redis



@app.websocket("/api/v1/groups/ws/chat/{link_id}")
async def websocket_endpoint(websocket: WebSocket):
    redis_conn = await aioredis.Redis(
        host=settings.redis.host, port=settings.redis.port, decode_responses=True
    )
    await websocket.accept()
    active_connections.add(websocket)

    # create chat id from websocket link
    chat_id_raw = str(websocket.url).split(sep='/')
    link_index = chat_id_raw.index('chat') + 1
    chat_id = chat_id_raw[link_index]
    chat_id = chat_id.join('chat')
    chat = Chat(id=chat_id)
    # get chat history, if there is a history, send history to joined user"""
    history = await redis_conn.get(chat.id)
    if history:
        chat.messeges = json.loads(history)
        for message in chat.messeges:
            message = Messege(**message)
            await websocket.send_text(f"{message.timestamp}: User_{message.user}: {message.data}")

    try:
        while True:
            data = await websocket.receive_json()
            message = Messege(**data)
            message.timestamp = datetime.now().time().replace(microsecond=0)
            for connection in active_connections:
                await connection.send_text(f"{message.timestamp}: User_{message.user}: {message.data}")
                # update and record chat history into cache storage (redis)
                chat.messeges.append(message)
                history = chat.messeges
                history = json.dumps(history, default=pydantic_encoder)
                await redis_conn.set(chat.id, history)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    if redis_cache.redis_conn is not None:
        await redis_cache.redis_conn.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.chat_service.host,
        port=settings.chat_service.port,
        reload=True,
    )
