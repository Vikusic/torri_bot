import psycopg2

try:
    #conn = psycopg2.connect(dbname='candles', user='postgres', password='root', host='localhost')
    conn = psycopg2.connect('postgresql://postgres:root@localhost:5433/candles')
except:
    print('Ошибка подключения!!!')

#cursor = conn.cursor(parameters)

# def product_reseach(parameters):
#
#     with conn.cursor() as curs:
#         curs.execute('SELECT name_product FROM products WHERE id_type_products = (%s)', str(parameters))
#         a = curs.fetchall()
#         a = str(a)
#         print(a)

# def product_reseach(parameters):
#     stroka = ''
#     with conn.cursor() as curs:
#         curs.execute('SELECT name_product FROM products WHERE id_type_products = (%s)', str(parameters))
#         b = curs.execute('SELECT COUNT(name_product) FROM products WHERE id_type_products = (%s)', str(parameters))
#         for i in range(2):
#             a = curs.fetchone()
#             stroka += str(a)
#     b = str(b)
#     print('1', type(b))
#     print('2', stroka)
#     print('--')
#     print('3', b)
#     return stroka
#
# product_reseach(1)


print('------')
parameters = 1
with conn.cursor() as curs:
    #curs.execute('SELECT name_product FROM products WHERE id_type_products = (%s)', str(parameters))
    curs.execute('SELECT COUNT(name_product) FROM products WHERE id_type_products = (%s)', str(parameters))
    #print(type(number))
    # извлекаем одну строку
    a = curs.fetchone()
    print(a)
    a = str(a)
    print(type(a))
    print(a)
    a = int(a[1])
    print(type(a))