if __name__=="__main__":
    import mysql.connector
    from app.core.database import metadata,create_engine
    from app.env import (
        FOXLINK_DATABASE_HOST,
        FOXLINK_DATABASE_PORT,
        FOXLINK_DATABASE_USER,
        FOXLINK_DATABASE_PASSWORD,
        FOXLINK_DATABASE_NAME,
        API_DATABASE_HOST,
        API_DATABASE_PORT,
        API_DATABASE_USER,
        API_DATABASE_PASSWORD,
        API_DATABASE_NAME,
    )

    print(f"Working at Foxlink DB")
    connection = mysql.connector.connect(
        host=FOXLINK_DATABASE_HOST,
        user=FOXLINK_DATABASE_USER,
        password=FOXLINK_DATABASE_PASSWORD,
        port=FOXLINK_DATABASE_PORT
    )
    cursor = connection.cursor()
    ##### DROP  TABLE #####
    print("Dropping table...")
    try:
        cursor.execute(
            f"""DROP DATABASE {FOXLINK_DATABASE_NAME};"""
        )
        connection.commit()
    except Exception as e:
        print(e)
    ##### BUILD TABLE ######
    print("Createing table...")
    try:
        cursor.execute(
            f"""CREATE DATABASE {FOXLINK_DATABASE_NAME};"""
        )
        connection.commit()
    except Exception as e:
        print(e)
    ##### BUILD SCHEMA ######
    print("Creating Schema...")
    try:
        engine = create_engine(f"mysql://{FOXLINK_DATABASE_USER}:{FOXLINK_DATABASE_PASSWORD}@{FOXLINK_DATABASE_HOST}:{FOXLINK_DATABASE_PORT}/{FOXLINK_DATABASE_NAME}")
        metadata.create_all(engine)
    except Exception as e:
        print(e)
    

    print(f"Working at API DB.")
    connection = mysql.connector.connect(
        host=API_DATABASE_HOST,
        user=API_DATABASE_USER,
        password=API_DATABASE_PASSWORD,
        port=API_DATABASE_PORT
    )
    cursor = connection.cursor()
    ##### DROP  TABLE #####
    print("Dropping table...")
    try:
        cursor.execute(
            f"""DROP DATABASE {API_DATABASE_NAME};"""
        )
        connection.commit()
    except Exception as e:
        print(e)
    ##### BUILD TABLE ######
    print("Createing table...")
    try:
        cursor.execute(
            f"""CREATE DATABASE {API_DATABASE_NAME};"""
        )
        connection.commit()
    except Exception as e:
        print(e)
    ##### BUILD SCHEMA ######
    print("Schema Should be created by the API server...")


    ##### END #######
    print("All done!")