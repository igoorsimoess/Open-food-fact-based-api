import requests
import psycopg2
from psycopg2 import extras
import pandas as pd
from io import BytesIO

csv_url = "https://cdn.coode.sh/food/data/csv/export.csv"


# Database creation parameters
db_creation_params = {
    # transform this into env variables
    "user": "postgres",
    "password": "postgres223",
    "host": "pgdb",
    "port": "5432",
}

try:
    # attempt to create the database (it's okay if it already exists)
    connection = psycopg2.connect(**db_creation_params)
    connection.autocommit = True
    create_db_query = "CREATE DATABASE fooddetails;"
    cursor = connection.cursor()
    cursor.execute(create_db_query)
    cursor.close()
    connection.close()
    print("db created")
except Exception as error:
    print(error)

db_params = {
    "database": "fooddetails",
    "user": "postgres",
    "password": "postgres223",
    "host": "pgdb",
    "port": "5432",
}

columns_to_extract = {
    "code": "code",
    "product_name_pt": "product_name",
    "quantity": "quantity",
    "brands": "brands",
    "categories": "categories",
    "labels": "labels",
    "countries": "cities",  
    "stores": "stores",
    "ingredients_text_pt": "ingredients_text",
    "traces": "traces",
    "serving_size": "serving_size",
    "off:nutriscore_grade": "nutriscore_grade",
    "off:nutriscore_score": "nutriscore_score",
}

try:
    response = requests.get(csv_url)
    response.raise_for_status()
    csv_data = response.content
    csv_data = BytesIO(csv_data)

    try:
        df = pd.read_csv(
            csv_data, delimiter="\t", usecols=columns_to_extract.keys(), na_values=[""]
        )  #
        df = df.drop(index=[497, 498])  # drop problematic rows
        df = df.where(pd.notna(df), None)  # cast all Nan values to None
        print("df read")
    except Exception as error:
        print(f"Erro na leitura do csv: {error}")

    try:
        connection = psycopg2.connect(**db_params)
        print("db connected")
    except Exception as error:
        print(f"Error connecting to the db: {error}\n")

    cursor = connection.cursor()

    create_table = """
    CREATE TABLE IF NOT EXISTS food_table (
        "code" NUMERIC PRIMARY KEY,
        "status" VARCHAR(10) DEFAULT 'published',
        "imported_t" TIMESTAMP NULL,
        "url" TEXT NULL,
        "creator" TEXT NULL,
        "created_t" INTEGER NULL,
        "last_modified_t" INTEGER NULL,
        "product_name" TEXT NULL,
        "quantity" TEXT NULL,
        "brands" TEXT NULL,
        "categories" TEXT NULL,
        "labels" TEXT NULL,
        "cities" TEXT NULL,
        "purchase_places" TEXT NULL,
        "stores" TEXT NULL,
        "ingredients_text" TEXT NULL,
        "traces" TEXT NULL,
        "serving_size" TEXT NULL,
        "serving_quantity" DOUBLE PRECISION NULL,
        "nutriscore_score" NUMERIC NULL,
        "nutriscore_grade" VARCHAR(3) NULL,
        "main_category" TEXT NULL,
        "image_url" TEXT NULL
    );
    """
    try:
        cursor.execute(create_table)
        print("table created")
    except Exception as error:
        print(f"Erro na execução da tabela: {error}\n")

    # Convert the pandas DataFrame to a list of tuples for bulk insertion
    data_to_insert = [tuple(row) for row in df.values]
    # print(data_to_insert[:5])

    insert_query = f"""
    INSERT INTO food_table ({', '.join(['"' + col + '"' for col in columns_to_extract.values()])}) VALUES %s;
    """
    try:
        extras.execute_values(cursor, insert_query, data_to_insert)
    except Exception as error:
        print(f"error when attempting to insert: {error}")
    try:
        connection.commit()
    except Exception as error:
        print(f"Error when copying data from CSV to the table: {error}")

    try:
        update_query = """
            UPDATE food_table 
            SET status = NULL
            WHERE nutriscore_score = 'NaN'
        """

        cursor.execute(update_query)
    except Exception as error:
        print(error)


except Exception as error:
    print(f"Error: {str(error)}")
finally:
    connection.commit()
    print("Finally")
    cursor.close()
    connection.close()
