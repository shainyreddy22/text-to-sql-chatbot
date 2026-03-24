from langchain_community.utilities import SQLDatabase

def get_db():
    db = SQLDatabase.from_uri(
        "sqlite:///Chinook_Sqlite.sqlite",   # simplest — just the filename
        sample_rows_in_table_info=3,
        include_tables=None
    )
    print("Connected! Tables found:", db.get_usable_table_names())
    return db