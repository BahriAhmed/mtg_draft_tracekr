import os
from sqlalchemy import create_engine, event, MetaData, Table, Column, Integer, Float, String, ForeignKey, insert, Text, JSON, text

def consolidate_all_to_db(
    rarity_table,
    color_table,
    card_table,
    card_stats_table,
    archetype_stats,
    card_info_table,
    deck_table,
    pack_table,
    pick_table,
    rating_table,
    keyword_table,
    card_keyword_table,
    pack_card_table,
    db_path: str
):
    # Ensure folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Create SQLite engine
    engine = create_engine(f"sqlite:///{db_path}")

    # Enable foreign keys
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    metadata = MetaData()

    
    with engine.begin() as conn:
        for t in [
            "pick_table",
            "pack_card_table",
            "pack_table",
            "deck_table",
            "card_keyword_table",
            "keyword_table",
            "card_info_table",
            "card_stats_table",
            "card_table",
            "archetype_stats",
            "rarity_table",
            "color_table",
            
        ]:
            conn.execute(text(f"DROP TABLE IF EXISTS {t}"))

    
    rarity_sql = Table(
        "rarity_table", metadata,
        Column("rarity_id", Integer, primary_key=True),
        Column("rarity", String, nullable=False)
    )

    color_sql = Table(
        "color_table", metadata,
        Column("color_id", Integer, primary_key=True),
        Column("color", String, nullable=True)
    )

    card_sql = Table(
        "card_table", metadata,
        Column("card_id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("rarity_id", Integer, ForeignKey("rarity_table.rarity_id")),
        Column("color_id", Integer, ForeignKey("color_table.color_id"))
    )

    card_stats_sql = Table(
        "card_stats_table", metadata,
        Column("card_id", Integer, ForeignKey("card_table.card_id")),
        *(Column(c, Float) for c in card_stats_table.columns if c != "card_id")
    )

    card_info_sql = Table(
        "card_info_table", metadata,
        Column("card_id", Integer, ForeignKey("card_table.card_id"), primary_key=True),
        *(Column(c, String) for c in card_info_table.columns if c != "card_id")
    )

    keyword_sql = Table(
        "keyword_table", metadata,
        Column("keyword_id", Integer, primary_key=True),
        Column("keyword_name", String, nullable=False)
    )

    card_keyword_sql = Table(
        "card_keyword_table", metadata,
        Column("card_id", Integer, ForeignKey("card_info_table.card_id")),
        Column("keyword_id", Integer, ForeignKey("keyword_table.keyword_id"))
    )

    archetype_stats_sql = Table(
        "archetype_stats", metadata,
        Column("stat_id", Integer, primary_key=True),
        Column("color_id", Integer, ForeignKey("color_table.color_id"), nullable=False),
        Column("popularity_percent", Float, nullable=False),
        Column("matches", Float, nullable=False),
    )

    deck_sql = Table(
        "deck_table", metadata,
        Column("deck_id", Integer, primary_key=True),
        *(Column(c, String) for c in deck_table.columns if c != "deck_id")
    )

    pack_sql = Table(
        "pack_table", metadata,
        Column("pack_id", Integer, primary_key=True),
        Column("pack_order", Integer, nullable=False),
        Column("deck_id", Integer, ForeignKey("deck_table.deck_id")), 
    )

    pick_sql = Table(
        "pick_table", metadata,
        Column("pick_id", Integer, primary_key=True),
        Column("pick_order", Integer, nullable=False),
        Column("pack_id", Integer, ForeignKey("pack_table.pack_id"), nullable=False),
        Column("picked_card_id", Integer, ForeignKey("card_table.card_id"), nullable=False)
    )

    pack_card_sql = Table(
        "pack_card_table", metadata,
        Column("pack_id", Integer, ForeignKey("pack_table.pack_id")),
        Column("card_id", Integer, ForeignKey("card_table.card_id"))
    )

    rating_sql = Table(
        "rating_table", metadata,
        Column("card_id", Integer, ForeignKey("card_table.card_id"), primary_key=True),
        Column("ai_rating", Float, nullable=True),
        Column("pro_rating", String, nullable=True),
        Column("description", String, nullable=True)
    )

    metadata.create_all(engine)

    with engine.begin() as conn:
        conn.execute(insert(rarity_sql), rarity_table.to_dict(orient="records"))
        conn.execute(insert(color_sql), color_table.to_dict(orient="records"))
        conn.execute(insert(card_sql), card_table.to_dict(orient="records"))
        conn.execute(insert(card_stats_sql), card_stats_table.to_dict(orient="records"))
        conn.execute(insert(card_info_sql), card_info_table.to_dict(orient="records"))
        conn.execute(insert(keyword_sql), keyword_table.to_dict(orient="records"))
        conn.execute(insert(card_keyword_sql), card_keyword_table.to_dict(orient="records"))
        conn.execute(insert(archetype_stats_sql), archetype_stats.to_dict(orient="records"))
        conn.execute(insert(deck_sql), deck_table.to_dict(orient="records"))
        conn.execute(insert(pack_sql), pack_table.to_dict(orient="records"))
        conn.execute(insert(pick_sql), pick_table.to_dict(orient="records"))
        conn.execute(insert(pack_card_sql), pack_card_table.to_dict(orient="records"))
        conn.execute(insert(rating_sql), rating_table.to_dict(orient="records"))
    print(f"All card, archetype, and deck/pack/pick tables saved to {db_path} with FKs enforced.")