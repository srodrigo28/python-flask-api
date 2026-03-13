import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Conecta no MySQL raiz (sem selecionar db) para criar o banco de dados
connection = pymysql.connect(
    host=os.getenv('MYSQL_HOST', '127.0.0.1'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', ''),
    port=int(os.getenv('MYSQL_PORT', 3306))
)

try:
    with connection.cursor() as cursor:
        db_name = os.getenv('MYSQL_DB', 'loja_multi_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Banco de dados '{db_name}' verificado/criado com sucesso.")
finally:
    connection.close()
