def start():
    import os
    config = globals()
    os.environ['DATABASE_URL'] = 'postgresql://postgres@localhost/suite'
    config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
start()
del start
