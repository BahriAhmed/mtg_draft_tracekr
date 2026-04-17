def bulk_insert(session, model, df):
    if df.empty:
        return

    objects = [model(**row) for row in df.to_dict(orient="records")]
    session.bulk_save_objects(objects)