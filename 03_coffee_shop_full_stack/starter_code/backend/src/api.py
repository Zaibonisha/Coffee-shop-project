from http.client import NETWORK_AUTHENTICATION_REQUIRED
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS


from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
@requires_auth("drinks")
def get_drinks():
    drinks = [drink.short() for drink in Drink.query.order_by(Drink.id).all()]
   


    return jsonify(
            {
                "success": True,
                "drinks": drinks,
                "total_drinks": len(Drink.query.all()),
            }
        ), 200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail():
        drinks = [drink.long() for drink in Drink.query.order_by(Drink.id).all()]
        

        if len(drinks) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "drinks": drinks,
                "total_drinks": len(Drink.query.all()),
            }
        ), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def post_drinks():
    body = request.get_json()
    new_name = body.get("name", None)
    new_ingredients = body.get("ingredient", None)
        
    try:
        drink = Drink(name=new_name, ingredient=new_ingredients)
        drink.insert()

        drinks = [drink.long() for drink in Drink.query.order_by(Drink.id).all()]
        

        return jsonify(
            {
                "success": True,
                "created": drink.id,
                "drinks": drinks,
                "total_drinks": len(Drink.query.all()),
            }
        ),200

    except:
        abort(422)


        

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drinks(drink_id):

        body = request.get_json()

        try:
            drink = [drink.long() for drink in Drink.query.filter(Drink.id == drink_id).one_or_none()]
            if drink is None:
                abort(404)

            if "ingredients" in body:
                drink.ingredients = int(body.get("ingredients"))

            drink.update()

            return jsonify({"success": True, "drinks": drink}), 200

        except:
            abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(drink_id):
        try:
            drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

            if drink is None:
                abort(404)

            drink.delete()
            Drink = Drink.query.order_by(Drink.id).all()
            

            return jsonify(
                {
                    "success": True,
                    "delete": id,
                    "total_drinks": len(Drink).query.all(),
                }
            )

        except:
            abort(422)
  
        

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404                   

'''

         
'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                  "success": False,
                  "error": 404,
                  "message": "resource not found"
                  }), 404

@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422 
    )        


@app.errorhandler(405)
def not_found(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405,
    )    


        
                
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
#Auth0 error handler