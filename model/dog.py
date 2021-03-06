from model.base import BaseModel, db
from datetime import datetime

class Dog(BaseModel, db.Model):

    __tablename__ = "dogs"
    
    name = db.Column(db.String(255), nullable = False)
    bread = db.Column(db.String(255), nullable = False)
    birth = db.Column(db.DateTime, nullable = False)
    gender = db.Column(db.String(255), nullable = False)
    weight = db.Column(db.Float, nullable = False)
    height = db.Column(db.Integer, nullable = False)
    photo_path = db.Column(db.String(255), nullable = True)
    observations = db.relationship('DogObservation', backref = 'dog', lazy = 'dynamic', cascade = "all, delete-orphan")
    sessions = db.relationship('Session', backref = 'dog', lazy = 'dynamic', cascade = "all, delete-orphan")

    def __init__(self, name, bread, birth, gender, weight, height, photo_path = ""):
        super(Dog, self).__init__()
        self.name = name
        self.bread = bread
        try:
            self.birth = datetime.strptime(birth, "%Y/%m/%d")
        except:
            self.birth = datetime.now()
        self.gender = gender
        self.weight = weight
        self.height = height
        self.photo_path = photo_path

    def update(self, name, bread, birth, gender, weight, height):
        self.name = name
        self.bread = bread
        try:
            self.birth = datetime.strptime(birth, "%Y/%m/%d")
        except:
            self.birth = datetime.now()
        self.gender = gender
        self.weight = weight
        self.height = height

    def jsonOutput(self):
        return {
            'id': self.id ,'name' : self.name, 'bread': self.bread, 
            'birth' : self.birth.timestamp() * 1000,
            'gender' : self.gender, 
            'weight': self.weight, 
            'height' : self.height,
            'photo_path' : self.photo_path,
            'created_at': self.created_at.timestamp() * 1000,
            'updated_at': self.updated_at.timestamp() * 1000,
            }

    def jsonOutputComplete(self):
        return {
            'id': self.id ,'name' : self.name, 'bread': self.bread,
            'birth' : self.birth.timestamp() * 1000,
            'gender' : self.gender,
            'weight': self.weight,
            'height' : self.height,
            'photo_path' : self.photo_path,
            'created_at': self.created_at.timestamp() * 1000,
            'updated_at': self.updated_at.timestamp() * 1000,
            'observations': [ observation.jsonOutput() for observation in self.observations.all() ],
            'sessions': [ session.jsonOutput() for session in self.sessions.all() ],
            }

    def folderOutput(self):
        return "dogFolder-" + str(self.id)

    def photoOutput(self):
        return 'photo-dog-' + str(self.id)

    @classmethod
    def getDogById(cls, id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def getDogByName(cls, name):
        return cls.query.filter_by(name = name).all()

    @classmethod
    def getDogsByName(cls, name):
        search = "%{}%".format(name)
        query = cls.query.filter(cls.name.like(search))
        return query.all()

    @classmethod
    def getDogs(cls):
        return cls.query.all()

class DogObservation(BaseModel, db.Model):

    __tablename__ = "dogs_observations"

    observation = db.Column(db.String(512), nullable = False)
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable = False)

    def __init__(self, dog_id, observation):
        self.observation = observation
        self.dog_id = dog_id

    def jsonOutput(self):
        return {'id': self.id, 'observation': self.observation, 'dog_id' : self.dog_id}

    @classmethod
    def getObservationById(cls, id):
        return cls.query.filter_by(id = id).first()