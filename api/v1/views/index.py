#!/usr/bin/python3
"""returns JSON status ok"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage

@app_views.route("/status", methods=['GET'])
def status():
    if request.method == 'GET':
        return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    function to return the count of all class objects
    """
    if request.method == 'GET':
        return jsonify({cls.__name__: storage.count(cls) for cls in storage.all().values()})
