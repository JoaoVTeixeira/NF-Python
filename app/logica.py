from sqlalchemy.orm import Session
from .models import Estacionamentos,  Reservas


def get_all_reservas(db: Session):
    return db.query(Reservas).all()

def create_reserva(db: Session, estacionamento_id: int, placa_cliente, telefone_cliente, hora_reserva: str, hora_saida: str):
    reserva = Reservas(estacionamento_id=estacionamento_id, placa_cliente=placa_cliente, telefone_cliente=telefone_cliente, hora_reserva=hora_reserva, hora_saida=hora_saida)
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva



def configurar_estacionamento(db: Session, id: int, nome: str, tarifaHora: int, vagas: int):
    estacionamento = Estacionamentos(id=id, nome=nome, tarifaHora=tarifaHora, vagas=vagas)
    db.add(estacionamento)
    db.commit()
    db.refresh(estacionamento)
    return estacionamento
    