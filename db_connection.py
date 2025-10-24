import psycopg2
import pandas as pd

conn = psycopg2.connect("""
    host=hitopemadtar.beget.app
    port=5432
    sslmode=disable
    dbname=univer
    user=ERK
    password=Erk_123
    target_session_attrs=read-write
""")

query = "SELECT * FROM passes LIMIT 100;"

df = pd.read_sql_query(sql=query, con=conn)

print("Тип объекта:", type(df))
print("Размер:", df.shape)
print("Инфо:")
df.info()
print("Данные:")
print(df)
print('============')
