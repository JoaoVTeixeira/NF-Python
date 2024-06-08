from sqlalchemy import Column, Integer, String, ForeignKey, Float ;
from .db import Base
from sqlalchemy.orm import relationship

class Estacionamentos(Base):
    __tablename__ = 'Estacionamentos'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    tarifaHora = Column(Integer)
    vagas = Column(Integer)
    
    reservas = relationship("Reservas", back_populates="estacionamento")
    
class Reservas(Base):
    __tablename__ = 'Reservas'
    
    id = Column(Integer, primary_key=True, index=True)
    estacionamento_id = Column(Integer, ForeignKey('Estacionamentos.id'))
    placa_cliente = Column(String)
    telefone_cliente = Column(String)
    hora_reserva = Column(Float)   
    hora_saida = Column(Float)   

    
    estacionamento = relationship("Estacionamentos", back_populates="reservas")
 