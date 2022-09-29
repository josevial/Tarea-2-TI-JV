class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://wyzkrrlxmuynko:c9c27c1c2badb39df09d20b0cc6f8e1f050c7738d10bb599be52e010704504da@ec2-35-170-146-54.compute-1.amazonaws.com:5432/d4ebh3pjev8hq0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
}