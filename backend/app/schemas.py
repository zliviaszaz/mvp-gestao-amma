from datetime import date
from pydantic import BaseModel, ConfigDict, Field

class ParticipanteIn(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    data_nascimento: date | None = None
    telefone: str | None = Field(default=None, max_length=30)

class ParticipanteOut(ParticipanteIn):
    model_config = ConfigDict(from_attributes=True)
    id: str
    status: str

class AtividadeIn(BaseModel):
    nome: str = Field(min_length=2, max_length=120)
    descricao: str | None = Field(default=None, max_length=500)
    data_inicio: date
    status: str = "ativa"

class AtividadeOut(AtividadeIn):
    model_config = ConfigDict(from_attributes=True)
    id: str

class InscricaoIn(BaseModel):
    participante_id: str
    atividade_id: str

class InscricaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    participante_id: str
    atividade_id: str
    data_inscricao: date
    status: str

class FrequenciaIn(BaseModel):
    inscricao_id: str
    data_registro: date
    presente: bool

class FrequenciaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    inscricao_id: str
    data_registro: date
    presente: bool
