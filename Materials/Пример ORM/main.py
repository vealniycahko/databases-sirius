from flask import Flask, request
from redis import Redis
import json
from sqlalchemy import Integer, Table, create_engine, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

redis_conn = Redis(port=26596, password="redis", decode_responses=True)

engine = create_engine(
    "postgresql+psycopg2://postgres:changeme@localhost:5432/postgres",
    client_encoding="utf8",
)

Base = declarative_base()

equipment_to_holder = Table(
    "equipmentToHolder",
    Base.metadata,
    Column("holderPhone", ForeignKey("holder.phone")),
    Column("equipmentTitle", ForeignKey("equipment.title")),
)


class Holder(Base, SerializerMixin):
    __tablename__ = "holder"

    phone: str = Column(String, primary_key=True)
    name: str = Column(String)
    equipment: list = relationship("Equipment", secondary=equipment_to_holder)
    storage_cells: list = relationship("StorageCell")


class Equipment(Base, SerializerMixin):
    __tablename__ = "equipment"

    title: str = Column(String, primary_key=True)
    color: str = Column(String)
    holders: list = relationship("Holder", secondary=equipment_to_holder)


class StorageCell(Base, SerializerMixin):
    __tablename__ = "storageCell"

    code: str = Column(String, primary_key=True)
    capacity: int = Column(Integer)
    holder_phone: str = Column("holderPhone", String, ForeignKey("holder.phone"))
    holder = relationship("Holder", back_populates="storage_cells")


@app.route("/holders")
def get_holders():
    try:
        offset = request.args.get("offset")
        limit = request.args.get("limit")
        redis_key = f"holders:offset={offset},limit={limit}"
        redis_holders = redis_conn.get(redis_key)

        if redis_holders is None:
            with Session(bind=engine) as session:
                holders = session.query(Holder).limit(limit).offset(offset).all()

                redis_holders = json.dumps(
                    [
                        holder.to_dict(
                            rules=("-equipment.holders", "-storage_cells.holder")
                        )
                        for holder in holders
                    ],
                    ensure_ascii=False,
                    indent=2,
                )

            redis_conn.set(redis_key, redis_holders, ex=1)

        return redis_holders, 200, {"content-type": "text/json"}
    except Exception as ex:
        return {"message": repr(ex)}, 400


@app.route("/holders/create", methods=["POST"])
def create_holder():
    try:
        body = request.json
        name = body["name"]
        phone = body["phone"]

        with Session(bind=engine, autocommit=True) as session:
            holder = Holder(phone=phone, name=name)
            session.add(holder)

        return {"message": f"Holder {name} with phone = {phone} created."}
    except Exception as ex:
        return {"message": repr(ex)}, 400


@app.route("/holders/update", methods=["POST"])
def update_holder():
    try:
        body = request.json
        name = body["name"]
        phone = body["phone"]

        with Session(bind=engine, autocommit=True) as session:
            holder: Holder = session.query(Holder).filter(Holder.phone == phone).one()
            holder.name = name
            session.flush()

        return {"message": f"Holder with phone = {phone} updated."}
    except Exception as ex:
        return {"message": repr(ex)}, 400


@app.route("/holders/delete", methods=["DELETE"])
def delete_holder():
    try:
        body = request.json
        phone = body["phone"]

        with Session(bind=engine, autocommit=True) as session:
            session.query(Holder).filter(Holder.phone == phone).delete()

        return {"message": f"Holder with phone = {phone} deleted."}
    except Exception as ex:
        return {"message": repr(ex)}, 400
