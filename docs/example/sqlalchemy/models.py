"""Modelo do Buscador de Grupos de Estudo em SQLAlchemy 2.0.

Espelha exatamente as tabelas de example/sql/01-schema.sql.
"""
from datetime import date, datetime, time

from sqlalchemy import (
    BigInteger, CheckConstraint, Date, DateTime, ForeignKey, Identity, Index,
    Integer, SmallInteger, Text, Time, func, text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome_usuario: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    participacoes: Mapped[list["Participacao"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True
    )


class Materia(Base):
    __tablename__ = "materias"

    materia_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, unique=True)
    codigo: Mapped[str] = mapped_column(Text, unique=True)

    grupos: Mapped[list["Grupo"]] = relationship(back_populates="materia")


class Grupo(Base):
    __tablename__ = "grupos"
    __table_args__ = (
        CheckConstraint("max_participantes > 0", name="grupos_max_participantes_check"),
        Index("idx_grupos_materia_id", "materia_id"),
    )

    grupo_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    nome_grupo: Mapped[str] = mapped_column(Text)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.materia_id"))
    max_participantes: Mapped[int] = mapped_column(Integer, server_default=text("10"))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    materia: Mapped["Materia"] = relationship(back_populates="grupos")
    participacoes: Mapped[list["Participacao"]] = relationship(
        back_populates="grupo", cascade="all, delete-orphan", passive_deletes=True
    )
    encontros: Mapped[list["Encontro"]] = relationship(
        back_populates="grupo", cascade="all, delete-orphan", passive_deletes=True
    )


class Participacao(Base):
    __tablename__ = "participacoes"
    __table_args__ = (Index("idx_participacoes_grupo_id", "grupo_id"),)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.usuario_id", ondelete="CASCADE"), primary_key=True
    )
    grupo_id: Mapped[int] = mapped_column(
        ForeignKey("grupos.grupo_id", ondelete="CASCADE"), primary_key=True
    )
    entrou_em: Mapped[date] = mapped_column(Date, server_default=func.current_date())

    usuario: Mapped["Usuario"] = relationship(back_populates="participacoes")
    grupo: Mapped["Grupo"] = relationship(back_populates="participacoes")


class Encontro(Base):
    __tablename__ = "encontros"
    __table_args__ = (
        CheckConstraint("dia_semana between 1 and 7", name="encontros_dia_semana_check"),
        Index("idx_encontros_grupo_id", "grupo_id"),
    )

    encontro_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.grupo_id", ondelete="CASCADE"))
    dia_semana: Mapped[int] = mapped_column(SmallInteger)
    hora_inicio: Mapped[time] = mapped_column(Time)
    local: Mapped[str] = mapped_column(Text)

    grupo: Mapped["Grupo"] = relationship(back_populates="encontros")
