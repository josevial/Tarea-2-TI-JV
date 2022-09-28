class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://tstsrcmspltysg:064ec7b99640826fb85e77f08d7daa850d36a514ac0d70311328caa7c1d9e63f@ec2-35-170-146-54.compute-1.amazonaws.com:5432/deah8ikg1f54rj'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
}