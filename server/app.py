from __future__ import annotations

import os
import sys

# ensure parent module is tracked for environment / models python resolving
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from environment import LegalContractAuditorEnv
from models import Action, ActionType

app = FastAPI(
    title="LegalContractAuditor",
    description=(
        "Reinforcement Learning Environment for Automated Contract Compliance Review. "
        "An AI agent audits real commercial contracts from the CUAD dataset, "
        "identifying legal issues, proposing fixes, and submitting compliance audits."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

env = LegalContractAuditorEnv()


class ResetRequest(BaseModel):
    task_id: str = "task_easy"


class StepRequest(BaseModel):
    action: Action

@app.get("/health")
def health() -> Dict[str, str]:
    return {
        "status": "ok",
        "environment": "LegalContractAuditor",
        "description": "RL Environment for Automated Contract Compliance Review",
        "version": "1.0",
    }


@app.get("/")
def validate() -> Dict[str, Any]:
    return {
        "version": "1.0",
        "endpoints": ["/reset", "/step", "/state",  "/tasks", "/health"]
    }


@app.get("/tasks")
def get_tasks() -> Dict[str, Any]:
    return env.get_tasks()


@app.post("/reset")
def reset(req: Optional[ResetRequest] = None) -> Dict[str, Any]:
    try:
        task_id = req.task_id if req else "task_easy"
        obs = env.reset(task_id=task_id)
        return obs.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step")
def step(req: StepRequest) -> Dict[str, Any]:
    try:
        result = env.step(req.action)
        return {
            "observation": result.observation.model_dump(),
            "reward": result.reward.model_dump(),
            "done": result.done,
            "info": result.info,
        }
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.get("/state")
def state() -> Dict[str, Any]:
    return env.state()


def main():
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    main()