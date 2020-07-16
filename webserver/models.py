from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class EnergyModel(db.Model):
    __tablename__ = 'energy'

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(250), nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False)

    voltage = db.Column(db.Numeric(precision=8, scale=6), nullable=False)
    frequency = db.Column(db.Numeric(precision=8, scale=6), nullable=False)
    real_energy = db.Column(db.Numeric(precision=8, scale=6), nullable=False)

    def __repr__(self):
        s = (
            f'<id: {self.id}, device_id:{self.device_id},'
            f' timestamp:{self.timestamp},'
            f' freq:{self.frequency}, voltage:{self.voltage}, real_energy: {self.real_energy}>'
        )
        return s

    def as_json_friendly_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'timestamp': self.timestamp.timestamp(),
            'voltage': float(self.voltage),
            'frequency': float(self.frequency),
            'real_energy': float(self.real_energy),
        }
