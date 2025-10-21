#!/usr/bin/env python
"""Simple test server for Railway deployment."""

import os
import sys
sys.path.insert(0, 'backend')

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Railway!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "football-migu"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)