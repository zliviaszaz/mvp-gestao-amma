from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MVP Gestão AMMA", version="0.1.0",
              description="API inicial para participantes, atividades, inscrições e frequência.")

# Para desenvolvimento local. Restringir origens antes de publicar.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "projeto": "MVP Gestão AMMA"}

@app.post("/api/participantes", response_model=schemas.ParticipanteOut, status_code=201)
def criar_participante(payload: schemas.ParticipanteIn, db: Session = Depends(get_db)):
    item = models.Participante(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@app.get("/api/participantes", response_model=list[schemas.ParticipanteOut])
def listar_participantes(q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(models.Participante).order_by(models.Participante.nome)
    if q:
        stmt = stmt.where(models.Participante.nome.ilike(f"%{q}%"))
    return db.scalars(stmt).all()

@app.put("/api/participantes/{participante_id}", response_model=schemas.ParticipanteOut)
def atualizar_participante(participante_id: str, payload: schemas.ParticipanteIn, db: Session = Depends(get_db)):
    item = db.get(models.Participante, participante_id)
    if not item:
        raise HTTPException(404, "Participante não encontrado.")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@app.post("/api/atividades", response_model=schemas.AtividadeOut, status_code=201)
def criar_atividade(payload: schemas.AtividadeIn, db: Session = Depends(get_db)):
    item = models.Atividade(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@app.get("/api/atividades", response_model=list[schemas.AtividadeOut])
def listar_atividades(db: Session = Depends(get_db)):
    return db.scalars(select(models.Atividade).order_by(models.Atividade.data_inicio)).all()

@app.post("/api/inscricoes", response_model=schemas.InscricaoOut, status_code=201)
def criar_inscricao(payload: schemas.InscricaoIn, db: Session = Depends(get_db)):
    if not db.get(models.Participante, payload.participante_id):
        raise HTTPException(404, "Participante não encontrado.")
    if not db.get(models.Atividade, payload.atividade_id):
        raise HTTPException(404, "Atividade não encontrada.")
    item = models.Inscricao(**payload.model_dump())
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Já existe inscrição para este participante e atividade.")
    db.refresh(item)
    return item

@app.get("/api/inscricoes", response_model=list[schemas.InscricaoOut])
def listar_inscricoes(db: Session = Depends(get_db)):
    return db.scalars(select(models.Inscricao)).all()

@app.post("/api/frequencias", response_model=schemas.FrequenciaOut, status_code=201)
def registrar_frequencia(payload: schemas.FrequenciaIn, db: Session = Depends(get_db)):
    if not db.get(models.Inscricao, payload.inscricao_id):
        raise HTTPException(404, "Inscrição não encontrada.")
    item = models.Frequencia(**payload.model_dump())
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "A frequência desta inscrição já foi registrada nessa data.")
    db.refresh(item)
    return item

@app.get("/api/frequencias", response_model=list[schemas.FrequenciaOut])
def listar_frequencias(inscricao_id: str | None = None, db: Session = Depends(get_db)):
    stmt = select(models.Frequencia)
    if inscricao_id:
        stmt = stmt.where(models.Frequencia.inscricao_id == inscricao_id)
    return db.scalars(stmt.order_by(models.Frequencia.data_registro.desc())).all()
