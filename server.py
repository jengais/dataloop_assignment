from fastapi import FastAPI, Request, HTTPException
import httpx
import asyncio
from httpx import AsyncClient

from pydantic import BaseModel

class StartRequest(BaseModel):
    pong_time: int
        
        
app = FastAPI()
client = AsyncClient()

pong_time_ms = 1000
is_running = False

@app.get("/ping")
async def ping(target: str):
    global is_running
    if is_running:
        await asyncio.sleep(pong_time_ms / 1000)
        try:
            response = await client.get(f"http://{target}/ping?target=localhost:8000")
            return {"message": response.json()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"message": "game not running"}

@app.post("/start")
async def start_game(request: StartRequest):
    global pong_time_ms, is_running
    pong_time_ms = request.pong_time
    is_running = True
    return {"message": "game started"}

@app.post("/pause")
async def pause_game():
    global is_running
    is_running = False
    return {"message": "game paused"}

@app.post("/resume")
async def resume_game():
    global is_running
    is_running = True
    return {"message": "game resumed"}

@app.post("/stop")
async def stop_game():
    global is_running
    is_running = False
    return {"message": "game stopped"}