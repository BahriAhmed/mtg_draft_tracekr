from draft_tracker_system.db.base import Base
from draft_tracker_system.db.models import *
from draft_tracker_system.db.session import get_engine, get_session
from draft_tracker_system.db.repository import bulk_insert
from kedro.framework.session import KedroSession

def build_db_url():
    session = KedroSession.create()
    context = session.load_context()
    creds = context.config_loader["credentials"]["postgres_db"]
    return f"postgresql+psycopg2://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['db']}"

def consolidate_all_to_db(
    rarity_table,
    color_table,
    card_table,
    card_stats_table,
    archetype_stats,
    card_info_table,
    deck_table,
    pack_table,
    rating_table,
    keyword_table,
    card_keyword_table,
    pack_card_table,
    type_table, 
    subtype_table, 
    card_type_table,
    card_subtype_table
):  

    # create engine + session
    db_url = build_db_url()
    engine = get_engine(db_url)
    session = get_session(engine)

    # reset database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Insert data 
    card = card_table.merge(card_info_table, on="card_id", how="left")
    color = color_table.merge(archetype_stats, on="color_id", how='left').drop(columns = "stat_id")
    

    bulk_insert(session, Rarity, rarity_table)
    bulk_insert(session, Color, color)
    bulk_insert(session, Card, card)
    bulk_insert(session, CardStats, card_stats_table)
    bulk_insert(session, Keyword, keyword_table)
    bulk_insert(session, CardKeyword, card_keyword_table)
    bulk_insert(session, Deck, deck_table)
    bulk_insert(session, Pack, pack_table)
    bulk_insert(session, PackCard, pack_card_table)
    bulk_insert(session, Rating, rating_table)

    bulk_insert(session, Type, type_table)
    bulk_insert(session, SubType, subtype_table)
    bulk_insert(session, CardType, card_type_table)
    bulk_insert(session, CardSubType, card_subtype_table)

    session.commit()
    session.close()