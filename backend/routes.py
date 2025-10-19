from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))



######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200 

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):

    for dic in data: 
        if dic["id"] == id: 
            return jsonify(dic), 200 
    
    return jsonify({"message":'No valid number'}), 404

    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    
    userData = request.get_json()
    for dic in data: 
        if dic['id'] == userData['id']: 
            userData['Message'] = f"picture with id {userData['id']} already present"
            return jsonify(userData), 302

    data.append(userData)
    with open(json_url, 'w') as a: 
        json.dump(data, a)    
    return jsonify(userData), 201 

    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    userData = request.get_json()
    for dic in data: 
        if dic['id'] == id: 
            dic["event_state"] = userData["event_state"]
            # Guardar cambios en el archivo
            with open(json_url, 'w') as f:
                json.dump(data, f)
            return jsonify(dic), 200  
    userData['message'] = 'picture not found'
    return jsonify(userData), 404  

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for dic in data: 
        if dic['id'] == id: 
            data.remove(dic)
            with open(json_url, 'w') as a: 
                json.dump(data, a)
            return '', 204  # ← El return aquí sale del loop automáticamente
    return jsonify({"message": "picture not found"}), 404
