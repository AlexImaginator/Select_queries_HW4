import sqlalchemy


def query1(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name, release_year FROM album
            WHERE release_year = '2018'
            '''
    result = connection.execute(query).fetchall()
    print('---------------------------------')
    print('Альбомы, вышедшие в 2018 году:')
    for album in result:
        print(f'{album[0]} - {album[1]}')
    print('---------------------------------')
    connection.close()


def query2(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name, duration FROM track
            WHERE duration = (SELECT MAX(duration) FROM track)
            '''
    result = connection.execute(query).fetchone()
    longest_track = {'name': result[0], 'duration': result[1]}
    print('---------------------------------')
    print('Самый длинный трек:')
    print(f'{longest_track["name"]} - {longest_track["duration"].strftime("%M:%S")}')
    print('---------------------------------')
    connection.close()


def query3(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name, duration FROM track
            WHERE duration >= '00:03:30'
            '''
    result = connection.execute(query).fetchall()
    print('---------------------------------')
    print('Треки длиннее 3:30:')
    for track in result:
        print(f'{track[0]} - {track[1].strftime("%M:%S")}')
    print('---------------------------------')
    connection.close()


def query4(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name, release_year FROM collection
            WHERE release_year BETWEEN '2018' AND '2020'
            '''
    result = connection.execute(query).fetchall()
    print('---------------------------------')
    print('Сборники, вышедшие в 2018 - 2020:')
    for collection in result:
        print(f'{collection[0]} - {collection[1]} год')
    print('---------------------------------')
    connection.close()


def query5(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name FROM musician
            WHERE name NOT LIKE '%% %%'
            '''
    result = connection.execute(query).fetchall()
    print('---------------------------------')
    print('Исполнители с именем из одного слова:')
    for musician in result:
        print(musician[0])
    print('---------------------------------')
    connection.close()


def query6(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name FROM track
            WHERE name LIKE '%% мой %%'
            OR name LIKE '%% my %%'
            '''
    result = connection.execute(query).fetchall()
    print('---------------------------------')
    print('Треки, содержащие в названии мой / my:')
    for track in result:
        print(track[0])
    print('---------------------------------')
    connection.close()


def query7(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name, COUNT(musician_id) FROM genre
            JOIN genre_musician ON genre.id = genre_musician.genre_id
            GROUP BY genre.id
            '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Количество исполнителей по жанрам:')
    for item in result:
        print(f'{item[0]} - {item[1]}')
    print('-------------------------')
    connection.close()


def query8(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT COUNT(track.id) FROM album
            JOIN track ON album.id = track.album_id
            WHERE release_year BETWEEN '2019' AND '2020'
            '''
    result = connection.execute(query).fetchone()
    print('-------------------------')
    print('Количество треков, вошедших в альбомы 2019 - 2020 годов:')
    print(result[0])
    print('-------------------------')
    connection.close()


def query9(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT album.name, AVG(track.duration) FROM album
            JOIN track ON album.id = track.album_id
            GROUP BY album.id
            '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Средняя продолжительность треков по каждому альбому:')
    for item in result:
        print(f'{item[0]} - {str(item[1]).split(".")[0]}')
    print('-------------------------')
    connection.close()


def query10(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name FROM musician
            WHERE id !=
                (SELECT musician_id FROM album a
                JOIN album_musician am ON a.id = am.album_id
                WHERE release_year = '2020')
            '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Все исполнители, которые не выпустили альбомы в 2020 году:')
    for item in result:
        print(item[0])
    print('-------------------------')
    connection.close()


def query11(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT c.name FROM collection c
            JOIN collection_track ct ON c.id = ct.collection_id
            JOIN track t ON ct.track_id = t.id
            JOIN album a ON t.album_id = a.id
            JOIN album_musician am ON a.id = am.album_id
            JOIN musician m ON am.musician_id = m.id
            WHERE m.name = 'Пилот'
            '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Сборники, в которых присутствует исполнитель Пилот:')
    for item in result:
        print(item[0])
    print('-------------------------')
    connection.close()


def query12(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT a.name FROM album a
            JOIN album_musician am ON a.id = am.album_id
            JOIN musician m ON am.musician_id = m.id
            JOIN genre_musician gm ON m.id = gm.musician_id
            JOIN genre g ON gm.genre_id = g.id
            GROUP BY a.name
            HAVING COUNT(g.id) > '1'
            '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Альбомы, в которых присутствуют исполнители более 1 жанра:')
    for item in result:
        print(item[0])
    print('-------------------------')
    connection.close()


def query13(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT name FROM track
            LEFT JOIN collection_track ct ON track.id = ct.track_id
            WHERE ct.track_id IS NULL
            '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Треки, которые не входят в сборники:')
    for item in result:
        print(item[0])
    print('-------------------------')
    connection.close()


def query14(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query = f'''
            SELECT m.name FROM musician m
            JOIN album_musician am ON m.id = am.musician_id
            JOIN album a ON am.album_id = a.id
            JOIN track t ON a.id = t.album_id
            WHERE t.duration = (SELECT MIN(duration) FROM track)
            '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Исполнители, написавшие самый короткий по продолжительности трек:')
    for item in result:
        print(item[0])
    print('-------------------------')
    connection.close()


def query15(db):
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query_1 = f'''
            SELECT album_id, COUNT(id) FROM track
            GROUP BY album_id
            '''
    result = connection.execute(query_1).fetchall()
    min_count_tracks = min([item[1] for item in result])
    album_ids = [str(item[0]) for item in result if item[1] == min_count_tracks]
    query = f'''
          SELECT name FROM album
          WHERE id IN ({",".join(album_ids)})
          '''
    result = connection.execute(query).fetchall()
    print('-------------------------')
    print('Названия альбомов, содержащих наименьшее количество треков:')
    for item in result:
        print(item[0])
    print('-------------------------')
    connection.close()


def hw4_select_queries(db):
    query1(db)
    query2(db)
    query3(db)
    query4(db)
    query5(db)
    query6(db)


def hw5_select_queries(db):
    query7(db)
    query8(db)
    query9(db)
    query10(db)
    query11(db)
    query12(db)
    query13(db)
    query14(db)
    query15(db)
