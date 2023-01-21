#!/usr/bin/python3
"""returns JSON status ok"""
from flask import jsonify, request
from api.v1.views import app_views

@app_views.route("/status", methods=['GET'])
def status():
    if request.method == 'GET':
        return jsonify({"status": "OK"}) 
