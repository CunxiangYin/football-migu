#!/usr/bin/env python
"""Minimal FastAPI app for Railway testing."""

import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Railway!", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)