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
    query = 'SELECT name, duration FROM track'
    result = connection.execute(query).fetchall()
    longest_track = {'name': result[0][0], 'duration': result[0][1]}
    for track in result:
        if track[1] > longest_track['duration']:
            longest_track['name'] = track[0]
            longest_track['duration'] = track[1]
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
            WHERE release_year >= '2018'
            AND release_year <= '2020'
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


def hw_select_queries(db):
    query1(db)
    query2(db)
    query3(db)
    query4(db)
    query5(db)
    query6(db)
