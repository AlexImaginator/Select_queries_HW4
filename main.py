from db_manager import create_tables, insert_from_file, collection_insert, collection_track_insert
from select_queries import hw_select_queries


def main():
    db = ''
    sql_query_file = 'tables_creating.sql'
    src_tracks = 'tracks_src_db.json'
    create_tables(db, sql_query_file)
    insert_from_file(db, src_tracks)
    collection_insert(db, 'collections_src_db.json')
    collection_track_insert(db, 'collections_src_db.json')
    hw_select_queries(db)


if __name__ == '__main__':
    main()
