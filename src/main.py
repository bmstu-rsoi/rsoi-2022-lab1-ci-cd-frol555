import os
from flask import Flask, request, Response
from DataBase import DataBase

app = Flask(__name__)


@app.route('/')
def hello_world():
    statement = 'Hello World!'
    return statement


@app.route("/api/v1/persons/", methods=['GET'])
def get_all_persons():
    personDB = DataBase()
    result = personDB.db_read()
    personDB.db_disconnect()
    return result, 200


@app.route("/api/v1/persons/<int:personID>", methods=['GET'])
def get_person(personID):
    personDB = DataBase()
    try:
        result = personDB.db_read(person_id=personID)[0]
    except IndexError:
        personDB.db_disconnect()
        return Response(status=404)

    personDB.db_disconnect()
    print(request.host)
    return result, 200


@app.route("/api/v1/persons/", methods=['POST'])
def post():
    insert_data = request.json

    personDB = DataBase()

    insert_data_tuple = (insert_data['name'], insert_data['address'], insert_data['work'], insert_data['age'])
    new_person_id = personDB.db_write(insert_data_tuple)

    personDB.db_disconnect()

    return app.redirect(f"{request.host}/api/v1/persons/{new_person_id[0]}", code=201)


@app.route("/api/v1/persons/<int:personID>", methods=['PATCH'])
def patch(personID):
    personDB = DataBase()
    try:
        result = personDB.db_update(personID, request.json)
    except TypeError:
        personDB.db_disconnect()
        return Response(status=404)
    personDB.db_disconnect()
    print(result)
    return result, 200


@app.route("/api/v1/persons/<int:personID>", methods=['DELETE'])
def delete(personID):
    personDB = DataBase()
    try:
        personDB.db_delete(personID)
    except TypeError:
        personDB.db_disconnect()
        return Response(status=404)
    personDB.db_disconnect()
    return Response(status=204)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host="0.0.0.0")
