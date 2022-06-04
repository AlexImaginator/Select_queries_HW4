import sqlalchemy
import json


def create_tables(db, sql_query_file):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    with open(sql_query_file, 'r') as tables:
        tables_list = tables.read().split(';')
        tables_list.pop()
        for table in tables_list:
            connection.execute(table)
    connection.close()


def genre_insert(db, data):
    genre_list = []
    for musician in data:
        genre_list.extend(musician['genre'])
    genre_list_uniq = list(set(genre_list))
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for genre in genre_list_uniq:
        query_check = f'''
                SELECT name FROM genre
                WHERE name = '{genre}'
                '''
        if not connection.execute(query_check).fetchall():
            query_insert = f'''
                    INSERT INTO genre (name)
                    VALUES ('{genre}')
                    '''
            connection.execute(query_insert)
    connection.close()


def musician_insert(db, data):
    musician_list_uniq = []
    for musician in data:
        if musician['musician'] not in musician_list_uniq:
            musician_list_uniq.append(musician['musician'])
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for musician in musician_list_uniq:
        query_check = f'''
                SELECT name FROM musician
                WHERE name = '{musician}'
                '''
        if not connection.execute(query_check).fetchall():
            query_insert = f'''
                    INSERT INTO musician (name)
                    VALUES ('{musician}')
                    '''
            connection.execute(query_insert)
    connection.close()


def genre_musician_insert(db, data):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for musician in data:
        for genre in musician['genre']:
            query_check = f'''
                SELECT musician_id, genre_id FROM genre_musician
                WHERE musician_id = (SELECT id FROM musician
                                    WHERE name = '{musician["musician"]}'
                                    )
                AND genre_id = (SELECT id FROM genre
                               WHERE name = '{genre}'
                               )
                '''
            if not connection.execute(query_check).fetchall():
                query_insert = f'''
                    INSERT INTO genre_musician (musician_id, genre_id)
                    VALUES (    (SELECT id FROM musician
                                WHERE name = '{musician["musician"]}'
                                ),
                                (SELECT id FROM genre
                                WHERE name = '{genre}'
                                )
                            )
                    '''
                connection.execute(query_insert)
    connection.close()


def album_insert(db, data):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for musician in data:
        for album in musician['album']:
            query_check = f'''
                SELECT * FROM musician
                WHERE name = '{musician["musician"]}'
                AND id = (
                    SELECT musician_id FROM album_musician
                    WHERE album_id = (
                        SELECT id FROM album
                        WHERE name = '{album["name"]}' AND release_year = '{album["year"]}'
                        )
                    )
                '''
            if not connection.execute(query_check).fetchall():
                query_insert = f'''
                    INSERT INTO album (name, release_year)
                    VALUES ('{album["name"]}', '{album["year"]}')
                    '''
                connection.execute(query_insert)
    connection.close()


def album_musician_insert(db, data):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for musician in data:
        for album in musician['album']:
            query_check = f'''
                SELECT musician_id, album_id FROM album_musician
                WHERE musician_id = (
                    SELECT id FROM musician
                    WHERE name = '{musician["musician"]}'
                    )
                AND album_id = (
                    SELECT id FROM album
                    WHERE name = '{album["name"]}'
                    )
                '''
            if not connection.execute(query_check).fetchall():
                query_insert = f'''
                    INSERT INTO album_musician (musician_id, album_id)
                    VALUES (
                        (SELECT id FROM musician
                        WHERE name = '{musician["musician"]}'
                        ),
                        (SELECT id FROM album
                        WHERE name = '{album["name"]}'
                        )
                    )
                    '''
                connection.execute(query_insert)
    connection.close()


def track_insert(db, data):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for musician in data:
        for album in musician['album']:
            for track in album['track']:
                query_check = f'''
                SELECT id FROM track
                WHERE name = '{track["title"]}'
                AND duration = '{track["duration"]}'
                AND album_id = (
                    SELECT id FROM album
                    WHERE name = '{album["name"]}'
                    AND id IN (
                        SELECT album_id FROM album_musician
                        WHERE musician_id = (
                            SELECT id FROM musician
                            WHERE name = '{musician["musician"]}'
                            )
                        )
                    )
                '''
                if not connection.execute(query_check).fetchall():
                    query_insert = f'''
                        INSERT INTO track (name, duration, album_id)
                        VALUES (
                            '{track["title"]}',
                            '{track["duration"]}',
                            (SELECT id FROM album
                            WHERE name = '{album["name"]}'
                            AND id IN (
                                SELECT album_id FROM album_musician
                                WHERE musician_id = (
                                    SELECT id FROM musician
                                    WHERE name = '{musician["musician"]}'
                                    )
                                )
                            )
                        )
                        '''
                    connection.execute(query_insert)
    connection.close()


def insert_from_file(db, src_file):
    with open(src_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    genre_insert(db, data)
    musician_insert(db, data)
    genre_musician_insert(db, data)
    album_insert(db, data)
    album_musician_insert(db, data)
    track_insert(db, data)


def collection_insert(db, src_file):
    with open(src_file, 'r', encoding='utf-8') as collections_file:
        data = json.load(collections_file)
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for collection in data:
        query_check = f'''
                SELECT * FROM collection
                WHERE name = '{collection["name"]}'
                AND release_year = '{collection["release_year"]}'
                '''
        if not connection.execute(query_check).fetchall():
            query_insert = f'''
                    INSERT INTO collection (name, release_year)
                    VALUES ('{collection["name"]}', '{collection["release_year"]}')
                    '''
            connection.execute(query_insert)
    connection.close()


def collection_track_insert(db, src_file):
    with open(src_file, 'r', encoding='utf-8') as collections_file:
        data = json.load(collections_file)
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    for collection in data:
        for track in collection['tracks']:
            query_check = f'''
                SELECT collection_id, track_id FROM collection_track
                WHERE collection_id = (SELECT id FROM collection
                                    WHERE name = '{collection["name"]}'
                                    )
                AND track_id = (SELECT id FROM track
                               WHERE id = '{track}'
                               )
                '''
            if not connection.execute(query_check).fetchall():
                query_insert = f'''
                    INSERT INTO collection_track (collection_id, track_id)
                    VALUES (    (SELECT id FROM collection
                                WHERE name = '{collection["name"]}'
                                ),
                                (SELECT id FROM track
                                WHERE id = '{track}'
                                )
                            )
                    '''
                connection.execute(query_insert)
    connection.close()
