#!/usr/bin/env python
# coding: utf-8

# In[1]:


print('hi')


# In[ ]:


from fastapi import FastAPI, HTTPException, Request
from httpx import AsyncClient, HTTPError, ReadTimeout  # Add import for ReadTimeout
from pydantic import BaseModel
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StartRequest(BaseModel):
    pong_time: int

app = FastAPI()
client = AsyncClient()

pong_time_ms = 1000
is_running = False

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return {"detail": "Internal server error"}, 500

@app.get("/ping")
async def ping(target: str):
    global is_running
    if is_running:
        try:
            response = await client.get(f"http://{target}/ping?target=localhost:8000")
            response.raise_for_status()  # Raise HTTPError for non-2xx status codes
            return {"message": response.json()}
        except HTTPError as e:
            if isinstance(e, httpx.ReadTimeout):
                logger.error(f"Read timeout occurred: {e}")
                raise HTTPException(status_code=500, detail="Read timeout occurred while waiting for response from the target server")
            else:
                logger.error(f"HTTP error occurred: {e}")
                raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            logger.error(f"An error occurred during ping request: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    else:
        raise HTTPException(status_code=400, detail="Game not running")


@app.post("/start")
async def start_game(request: StartRequest):
    global pong_time_ms, is_running
    pong_time_ms = request.pong_time
    is_running = True
    return {"message": "Game started"}

@app.post("/pause")
async def pause_game():
    global is_running
    is_running = False
    return {"message": "Game paused"}

@app.post("/resume")
async def resume_game():
    global is_running
    is_running = True
    return {"message": "Game resumed"}

@app.post("/stop")
async def stop_game():
    global is_running
    is_running = False
    return {"message": "Game stopped"}

