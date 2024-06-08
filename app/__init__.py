 
from .db import get_db, engine, Base
from .models import Estacionamentos, Reservas
from .logica import create_reserva

Base.metadata.create_all(bind=engine)
