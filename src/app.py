"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

initial_members = [
    {"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
    {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
    {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
]

for member in initial_members:
    jackson_family.add_member(member)
    

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        response_body = {
            "family": member
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"error": "Member not found"}), 404

@app.route('/members', methods=['POST'])
def add_member():
    member = request.json
    if not member or 'first_name' not in member:
        return jsonify({"error": "Missing required fields"}), 400
    new_member = jackson_family.add_member(member)
    response_body = {
        "family": new_member
    }
    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    new_data = request.json
    if not new_data:
        return jsonify({"error": "No data provided"}), 400
    updated_member = jackson_family.update_member(member_id, new_data)
    if updated_member:
        response_body = {
            "family": updated_member
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"error": "Member not found"}), 404


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    was_deleted = jackson_family.delete_member(member_id)
    if was_deleted:
        return jsonify({"success": "Member was deleted"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
