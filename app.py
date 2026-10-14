"""Небольшой Flask API для практики GitHub Actions и Docker."""
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(message="VPe04: GitHub Actions + Docker", endpoints=["/health"])


@app.get("/health")
def health():
    return jsonify(status="ok")
