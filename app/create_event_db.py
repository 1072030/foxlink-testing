if __name__=="__main__":
    import mysql.connector
    from app.services.database import metadata,create_engine
    from app.env import (
        FOXLINK_DATABASE_HOST,
        FOXLINK_DATABASE_PORT,
        FOXLINK_DATABASE_USER,
        FOXLINK_DATABASE_PASSWORD,
        FOXLINK_DATABASE_NAME
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


    ##### END #######
    print("All done!")