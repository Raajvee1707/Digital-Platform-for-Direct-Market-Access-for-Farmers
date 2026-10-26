
import oracledb

try:
    connection = oracledb.connect(
        user="FARM_PROJECT",
        password="FarmerDB_2026!",
        dsn="localhost:1521/FREEPDB1"
    )

    print("Oracle connection successful!")

    cursor = connection.cursor()
    cursor.execute("SELECT PRODUCT_ID, NAME, PRICE FROM PRODUCT")

    for row in cursor:
        print(row)

    cursor.close()
    connection.close()

except oracledb.Error as error:
    print("Connection failed:")
    print(error)
