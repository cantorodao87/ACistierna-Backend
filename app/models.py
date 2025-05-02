from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Trabajador(Base):
    __tablename__ = "trabajadores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=False, index=True)
    puesto = Column(String, unique=False, index=True)

class TurnoDia(Base):
    __tablename__ = "turnos_dia"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, unique=True, nullable=False)

    # 6 campos de trabajador, todos opcionales
    manana_id = Column(Integer, ForeignKey("trabajadores.id"), nullable=True)
    sc_manana_id = Column(Integer, ForeignKey("trabajadores.id"), nullable=True)
    tarde_id = Column(Integer, ForeignKey("trabajadores.id"), nullable=True)
    sc_tarde_id = Column(Integer, ForeignKey("trabajadores.id"), nullable=True)
    int_manana_id = Column(Integer, ForeignKey("trabajadores.id"), nullable=True)
    int_tarde_id = Column(Integer, ForeignKey("trabajadores.id"), nullable=True)

    # Relaciones para poder acceder a los trabajadores directamente
    manana = relationship("Trabajador", foreign_keys=[manana_id])
    sc_manana = relationship("Trabajador", foreign_keys=[sc_manana_id])
    tarde = relationship("Trabajador", foreign_keys=[tarde_id])
    sc_tarde = relationship("Trabajador", foreign_keys=[sc_tarde_id])
    int_manana = relationship("Trabajador", foreign_keys=[int_manana_id])
    int_tarde = relationship("Trabajador", foreign_keys=[int_tarde_id])