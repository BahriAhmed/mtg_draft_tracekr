from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base



class Rarity(Base):
    __tablename__ = "rarity_table"

    rarity_id = Column(Integer, primary_key=True)
    rarity = Column(String, nullable=False)

class Color(Base):
    __tablename__ = "color_table"

    popularity_percent = Column(Float, nullable=False)
    matches = Column(Float, nullable=False)

    color_id = Column(Integer, primary_key=True)
    color = Column(String, nullable=True)

class Type(Base):
    __tablename__ = "type_table"

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String, nullable=False, unique=True)

class SubType(Base):
    __tablename__ = "sub_type_table"

    subtype_id = Column(Integer, primary_key=True, autoincrement=True)
    subtype_name = Column(String, nullable=False, unique=True)

class CardType(Base):
    __tablename__ = "card_type_table"

    card_id = Column(Integer, ForeignKey("card_table.card_id"), primary_key=True)
    type_id = Column(Integer, ForeignKey("type_table.type_id"), primary_key=True)
    is_legendary  = Column(Boolean, nullable=False)


class CardSubType(Base):
    __tablename__ = "card_sub_type_table"

    card_id = Column(Integer, ForeignKey("card_table.card_id"), primary_key=True)
    subtype_id = Column(Integer, ForeignKey("sub_type_table.subtype_id"), primary_key=True)

class Card(Base):
    __tablename__ = "card_table"

    card_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    rarity_id = Column(Integer, ForeignKey("rarity_table.rarity_id"))
    color_id = Column(Integer, ForeignKey("color_table.color_id"))

    scryfall_uri = Column(String, nullable=False)
    mana_cost = Column(String, nullable=True)
    oracle_text = Column(String, nullable=True)

    power = Column(String, nullable=True)
    toughness = Column(String, nullable=True)
    loyalty = Column(Integer, nullable=True)


    rarity = relationship("Rarity")
    color = relationship("Color")

    types = relationship("Type", secondary="card_type_table", backref="cards")
    sub_types = relationship("SubType", secondary="card_sub_type_table", backref="cards")

    stats = relationship("CardStats", back_populates="card", uselist=False)


class CardStats(Base):
    __tablename__ = "card_stats_table"

    card_id = Column(Integer, ForeignKey("card_table.card_id"), primary_key=True)

    seen = Column(Float, nullable=True)
    alsa = Column(Float, nullable=True)
    picked = Column(Float, nullable=True)

    ata = Column(Float, nullable=True)
    gp = Column(Float, nullable=True)
    gp_pct = Column(Float, nullable=True)
    gp_wr = Column(Float, nullable=True)

    oh = Column(Float, nullable=True)
    oh_wr = Column(Float, nullable=True)

    gd = Column(Float, nullable=True)
    gd_wr = Column(Float, nullable=True)

    gih = Column(Float, nullable=True)
    gih_wr = Column(Float, nullable=True)

    gns = Column(Float, nullable=True)
    gns_wr = Column(Float, nullable=True)

    iih = Column(Float, nullable=True)

    card = relationship("Card", back_populates="stats")


class Keyword(Base):
    __tablename__ = "keyword_table"

    keyword_id = Column(Integer, primary_key=True)
    keyword_name = Column(String, nullable=False)


class CardKeyword(Base):
    __tablename__ = "card_keyword_table"

    card_id = Column(Integer, ForeignKey("card_table.card_id"), primary_key=True)
    keyword_id = Column(Integer, ForeignKey("keyword_table.keyword_id"), primary_key=True)



class User(Base):
    __tablename__ = "user_table"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("role_table.role_id"), nullable=False)

    role = relationship("Role", backref="users")
    decks = relationship("Deck", back_populates="user")


class Deck(Base):
    __tablename__ = "deck_table"

    deck_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.user_id"))

    user = relationship("User", back_populates="decks")
    packs = relationship("Pack", back_populates="deck")


class Pack(Base):
    __tablename__ = "pack_table"

    pack_id = Column(Integer, primary_key=True)
    pack_order = Column(Integer, nullable=False)

    deck_id = Column(Integer, ForeignKey("deck_table.deck_id"))

    deck = relationship("Deck", back_populates="packs")

class PackCard(Base):
    __tablename__ = "pack_card_table"

    pack_card_id = Column(Integer, primary_key=True, autoincrement=True)

    pack_id = Column(Integer, ForeignKey("pack_table.pack_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("card_table.card_id"), nullable=False)

    pick_order = Column(Integer, nullable=False)

    is_picked = Column(Boolean, nullable=False)

    pack = relationship("Pack")
    card = relationship("Card")


class Rating(Base):
    __tablename__ = "rating_table"

    card_id = Column(Integer, ForeignKey("card_table.card_id"), primary_key=True)

    ai_rating = Column(Float, nullable=True)
    pro_rating = Column(String, nullable=True)
    description = Column(String, nullable=True)

    card = relationship("Card")

class Role(Base):
    __tablename__ = "role_table"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, nullable=False, unique=True)

