"""Consultas do Buscador de Grupos com SQLAlchemy 2.0 (rode depois do seed).

Uso:
    export DATABASE_URL="postgresql+psycopg://usuario:senha@host:5432/banco"
    python consultas.py
"""
import os

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from models import Grupo, Materia, Participacao, Usuario

engine = create_engine(os.environ["DATABASE_URL"])

with Session(engine) as session:
    # 1. Vagas por grupo: o mesmo resultado do módulo 11 (join, count e group by)
    consulta = (
        select(
            Grupo.nome_grupo,
            Grupo.max_participantes,
            func.count(Participacao.usuario_id).label("participantes"),
        )
        .join(Participacao, Participacao.grupo_id == Grupo.grupo_id, isouter=True)
        .group_by(Grupo.grupo_id)
        .order_by(Grupo.nome_grupo)
    )
    print("--- grupos e participantes")
    for nome, limite, participantes in session.execute(consulta):
        print(f"{nome:<26} {participantes}/{limite}")

    # 2. Os grupos de uma pessoa, navegando pelos relacionamentos (sem escrever o join)
    ana = session.scalars(select(Usuario).where(Usuario.email == "ana.martins@exemplo.com")).one()
    print("--- grupos da", ana.nome_usuario)
    for p in ana.participacoes:
        print(f"{p.grupo.nome_grupo} ({p.grupo.materia.nome}), desde {p.entrou_em}")

    # 3. Inserir e desfazer: o rollback deixa o banco como estava
    materia = session.scalars(select(Materia).where(Materia.nome == "Cálculo I")).one()
    novo = Grupo(nome_grupo="Cálculo II na prática", materia=materia, max_participantes=5)
    session.add(novo)
    session.flush()
    print("--- novo grupo recebeu o id", novo.grupo_id)
    session.rollback()
