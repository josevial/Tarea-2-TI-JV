from flask import Flask, request
from flask import jsonify
from config import config
from models import db
from models import Airport, Flight
import requests


def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

enviroment = config['development']
app = create_app(enviroment)

@app.route('/')
def hello_world():
    return '<h1>API REST</h1>'

@app.route('/airports', methods=['GET']) #LISTO
def get_airports():
    airports = Airport.query.all()
    airports = list(map(lambda airport: airport.mostrar(), airports))

    return jsonify(airports), 200


@app.route('/airports', methods=['POST']) 
def create_airport(): #se pone algo que recibe?
    json = request.get_json(force=True)

    #Missing parameters
    if json.get('name') is None:
        return jsonify({"error": "Missing parameter: name"}), 400

    if json.get('country') is None:
        return jsonify({"error": "Missing parameter: country"}), 400
    
    if json.get('city') is None:
        return jsonify({"error": "Missing parameter: city"}), 400

    if json.get('position')['lat'] is None:
        return jsonify({"error": "Missing parameter: position"}), 400
    

    # Revisar las posiciones
    if json.get('position')['lat'] > 90 or json.get('position')['lat'] < -90:
        return jsonify({"error": "Latitude must be between -90 and 90"}), 400

    if json.get('position')['long'] > 180 or json.get('position')['long'] < -180:
        return jsonify({"error": "Longitude must be between -180 and 180"}), 400


    #revisar que no exista el mismo id
    if Airport.query.filter_by(id=json.get('id')).first() is not None:
        id = json.get('id')
        return jsonify({"error": f"Airport with id {id} already exists"}), 409 #poner el id

    #revisa que tenga len > 3 el id
    if len(json.get('id')) >= 3:
        airport = Airport.create(json['id'], json['name'], json['country'], json['city'], json['position']['lat'], json['position']['long'])
        airport.save()

        return jsonify(airport.json()), 201
    
    


@app.route('/airports/<id>', methods=['GET']) #VER QUE NO SE SUBAN EN ORDEN ALFABETICO Y LOS MISING PARAMETRS SON PARA TODOS?
def get_airport_id(id):
    airport = Airport.query.filter_by(id=id).first()
    if airport is None:
        return jsonify({"error": f"Airport with id {id} not found"}), 404 #como se pone el id entre medio
    
    return jsonify(airport.json()), 200


@app.route('/airports/<id>', methods=['PATCH']) #LISTO
def update_airport(id):
    
    json = request.get_json(force=True)
    
    if type(json.get('name')) is not str:
        return jsonify({"error": "Field name must be a string"}), 400
    
    #revisa que exista el id
    if Airport.query.filter_by(id=id).first() is None:
        return jsonify({"error": f"Airport with id {id} not found"}), 404

    #si existe el id, se actualiza
    airport = Airport.query.filter_by(id=id).first()
    #cambiar el nombre 
    airport.name = request.json['name']
    airport.update()

    return ('', 204)

@app.route('/airports/<id>', methods=['DELETE']) #COMO VEO LOS VUELOS QUE ESTAN EN PROGRESO? FALTA PROBAR ESTO
def delete_airport(id):
    #buscar si existe el id
    if Airport.query.filter_by(id=id).first() is None:
        return jsonify({"error": f"Airport with id {id} not found"}), 404

    #FALTA VER SI HAY VUELOS EN PROGRESOS
    for flight in Flight.query.all():
        if flight.destination_id == id:
            return jsonify({"error": f"Airport with id {id} has flights in progress"}), 409

    #si existe el id se elimina de la base de datos
    airport = Airport.query.filter_by(id=id).first()
    airport.delete()

    return ('', 204)

#FLIGHTS API

@app.route('/flights', methods=['GET']) #LISTO
def get_flights():
    flights = Flight.query.all()
    flights = list(map(lambda flight: flight.mostrar(), flights))

    return jsonify(flights), 200

@app.route('/flights', methods=['POST']) #QUE PASA CON LA DISTANCIA Y LOS DEMAS PARAMETROS?
def create_flight():
    json = request.get_json(force=True)

    #Missing parameters
    if json.get('id') is None:
        return jsonify({"error": "Missing parameter: id"}), 400

    if json.get('departure') is None:
        return jsonify({"error": "Missing parameter: departure"}), 400
    
    if json.get('destination') is None:
        return jsonify({"error": "Missing parameter: destination"}), 400
    
    if json.get('departure') == json.get('destination'):
        return jsonify({"error": "Departure and Destination airports must be different"}), 400
    

    #revisar si existe el id de los aeropuertos
    #buscar en los aeropuertos si existe el id de departure
    if Airport.query.filter_by(id=json.get('departure')).first() is None:
        return jsonify({"error": f"Airport with id {id} does not exists"}), 404
    else:
        #encontrar en la base de datos el aeropuerto con ese id
        departure = Airport.query.filter_by(id=json.get('departure')).first()
        #guardar el id del aeropuerto
        departure_id = departure.id
        #guardar el name del aeropuerto
        departure_name = departure.name
        #guardar la latitud y longitud del aereopuerto
        departure_lat = departure.lat
        departure_long = departure.lon

    
    #buscar en los aeropuertos si existe el id de destination
    if Airport.query.filter_by(id=json.get('destination')).first() is None:
        return jsonify({"error": f"Airport with id {id} does not exists"}), 404
    else:
        #encontrar en la base de datos el aereopuerto con ese id
        destination = Airport.query.filter_by(id=json.get('destination')).first()
        #guardar el id del aeropuerto
        destination_id = destination.id
        #guardar el name del aeropuerto
        destination_name = destination.name
        #guardar la latitud y longitud del aereopuerto
        destination_lat = destination.lat
        destination_long = destination.lon


    #revisar que no exista el mismo id
    if Flight.query.filter_by(id=json.get('id')).first() is not None:
        return jsonify({"error": f"Flight with id {id} already exists"}), 409
    else:
        if len(json.get('id')) >= 10:
            #seguir editando aca 
            response = requests.get(f'https://tarea-2.2022-2.tallerdeintegracion.cl/distance?initial={str(departure_lat)},{str(departure_long)}&final={str(destination_lat)},{str(destination_long)}')
            print(response)
            print(response.json())
            if response.status_code == 200:
                total_distance = response.json()['distance']
                flight = Flight.create(json['id'], departure_id, departure_name, destination_id, destination_name, total_distance, 0, 0, departure_lat, departure_long)
                flight.save()
                return jsonify(flight.json()), 201

            else:
                return ('', 404)



@app.route('/flights/<id>', methods=['GET']) #DEBERIA ESTAR LISTO PERO HAY QUE REVISARLO
def get_flight_id(id):
    flight = Flight.query.filter_by(id=id).first()
    if flight is None:
        return jsonify({"error": f"Flight with id {id} not found"}), 404
    
    return jsonify(flight.json()), 200

@app.route('/flights/<id>', methods=['DELETE'])
def delete_flight(id):
    #buscar si existe el id
    if Flight.query.filter_by(id=id).first() is None:
        return jsonify({"error": f"Flight with id {id} not found"}), 404

    #eliminar el vuelo
    flight = Flight.query.filter_by(id=id).first()
    flight.delete()

    return ('', 204)

@app.route('/flights/<id>/position', methods=['POST'])
def update_flight_position(id):
    #Missing parameters
    if request.json.get('lat') is None:
        return jsonify({"error": "Missing parameter: lat"}), 400
    
    if request.json.get('long') is None:
        return jsonify({"error": "Missing parameter: long"}), 400
    
    #revisa que la longitud y latitud esten dentro de los limites
    if request.json.get('lat') > 90 or request.json.get('lat') < -90:
        return jsonify({"error": "Latitude must be between -90 and 90"}), 400
    
    if request.json.get('long') > 180 or request.json.get('long') < -180:
        return jsonify({"error": "Longitude must be between -180 and 180"}), 400
    
    #revisa que exista el id
    if Flight.query.filter_by(id=id).first() is None:
        return jsonify({"error": f"Flight with id {id} not found"}), 404
    
    #si existe el id, se actualiza
    flight = Flight.query.filter_by(id=id).first()
    #cambiar la posicion
    flight.lat = request.json['lat']
    flight.lon = request.json['long']

    db.session.commit()

    #retornar la informacion del vuelo
    return jsonify(flight.json()), 200

#ESTADO DE LA API
@app.route('/status', methods=['GET'])
def get_status():
    return('',204)

#resetear el estado de la bdd

@app.route('/data', methods=['DELETE'])
def reset():
    db.drop_all()
    db.create_all()
    return('',200)



if __name__ == '__main__':
    app.run(debug=True)