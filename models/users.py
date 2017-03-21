from openedoo_project import db
from openedoo_project import config

database_prefix = config.database_prefix


def dump_datetime(val):
    """Deserialize datetime object into string form for JSON processing."""
    if val is None:
        raise ValueError("Your datetime is wrong!.")
    return [val.strftime("%Y-%m-%d"), val.strftime("%H:%M:%S")]


class User(db.Model):
    __tablename__ = '{db_prefix}_user'.format(db_prefix=database_prefix)
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.Text())
    fullname = db.Column(db.Text())
    nip = db.Column(db.BigInteger())
    access_token = db.Column(db.Text())
    public_key = db.Column(db.Text())
    private_key = db.Column(db.Text())
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime())
    last_login = db.Column(db.DateTime())

    def __init__(self, user={}):
        if not user:
            raise ValueError('user is supplied with wrong data!')

        self.username = user['username']
        self.password = user['password']
        self.fullname = user['fullname']
        self.nip = user['nip']
        self.created = user['created']
