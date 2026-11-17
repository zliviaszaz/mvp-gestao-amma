import uuid
from datetime import date
from sqlalchemy import String, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def new_id() -> str:
    return str(uuid.uuid4())

class Participante(Base):
    __tablename__ = "participantes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(12), nullable=False, default="ativo")
    inscricoes: Mapped[list["Inscricao"]] = relationship(back_populates="participante")

class Atividade(Base):
    __tablename__ = "atividades"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(500), nullable=True)
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(12), nullable=False, default="ativa")
    inscricoes: Mapped[list["Inscricao"]] = relationship(back_populates="atividade")

class Inscricao(Base):
    __tablename__ = "inscricoes"
    __table_args__ = (UniqueConstraint("participante_id", "atividade_id", name="uq_inscricao_participante_atividade"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    participante_id: Mapped[str] = mapped_column(ForeignKey("participantes.id"), nullable=False)
    atividade_id: Mapped[str] = mapped_column(ForeignKey("atividades.id"), nullable=False)
    data_inscricao: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    status: Mapped[str] = mapped_column(String(12), nullable=False, default="ativa")
    participante: Mapped[Participante] = relationship(back_populates="inscricoes")
    atividade: Mapped[Atividade] = relationship(back_populates="inscricoes")
    frequencias: Mapped[list["Frequencia"]] = relationship(back_populates="inscricao")

class Frequencia(Base):
    __tablename__ = "frequencias"
    __table_args__ = (UniqueConstraint("inscricao_id", "data_registro", name="uq_frequencia_inscricao_data"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    inscricao_id: Mapped[str] = mapped_column(ForeignKey("inscricoes.id"), nullable=False)
    data_registro: Mapped[date] = mapped_column(Date, nullable=False)
    presente: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    inscricao: Mapped[Inscricao] = relationship(back_populates="frequencias")
