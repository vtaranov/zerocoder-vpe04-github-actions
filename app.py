"""Небольшой Flask API для практики GitHub Actions и Docker."""
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(message="VPe04: GitHub Actions + Docker", endpoints=["/health", "/time"])


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/time")
def server_time():
    return jsonify(time=datetime.now(timezone.utc).isoformat(), timezone="UTC")
