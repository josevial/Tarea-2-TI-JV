from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Airport(db.Model):
    __tablename__ = 'airports'
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def mostrar(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def create(cls, id, name, country, city, lat, lon):
        airport = Airport(id=id, name=name, country=country, city=city, lat=lat, lon=lon)
        return airport

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return self
        except:
            return False

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'position': {'lat':self.lat,'long':self.lon}
        }
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False

    def update(self):
        self.save()

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.String, primary_key=True)
    departure_name = db.Column(db.String(100), nullable=False)
    departure_id = db.Column(db.String(100), db.ForeignKey('airports.id'), nullable=False)
    destination_id = db.Column(db.String(100), db.ForeignKey('airports.id'), nullable=False)
    destination_name = db.Column(db.String(100), nullable=False)
    total_distance = db.Column(db.Float, nullable=False)
    traveled_distance = db.Column(db.Float, nullable=False)
    bearing = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    @classmethod
    def create(cls, id,departure_id, departure_name, destination_id,destination_name, total_distance, traveled_distance, bearing, lat, lon):
        flight = Flight(id=id,departure_id=departure_id, departure_name=departure_name, destination_id=destination_id,destination_name=destination_name, total_distance=total_distance, traveled_distance=traveled_distance, bearing=bearing, lat=lat, lon=lon)
        return flight
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return self
        except:
            return False
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False
    
    def json(self):
        return {
            'id': self.id,
            'departure': {'id': self.departure_id, 'name': self.departure_name},
            'destination':{'id': self.destination_id, 'name':self.destination_name},
            'total_distance': self.total_distance,
            'traveled_distance': self.traveled_distance,
            'bearing': self.bearing,
            'position': {'lat':self.lat,'long':self.lon}
        }

    def mostrar(self):
        return {
            'id': self.id,
            'departure': self.departure_id,
            'destination': self.destination_id
        }
    



