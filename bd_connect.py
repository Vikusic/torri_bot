import psycopg2

try:
    #conn = psycopg2.connect(dbname='candles', user='postgres', password='root', host='localhost')
    conn = psycopg2.connect('postgresql://postgres:root@localhost:5433/candles')
except:
    print('Ошибка подключения!!!')

cursor = conn.cursor()
# a = cursor.execute('SELECT name_product FROM products WHERE id_product = 2')
# print(a)
# all_users = cursor.fetchall()
# cursor.close()
# conn.close()

def stroka():
    with conn.cursor() as curs:
        curs.execute('SELECT name_product FROM products WHERE id_type_products = 1 ')
        a = curs.fetchall()
        a = str(a)
    return a

def product_reseach(parameters):   #выдаёт позиции выбранной категории
    stroka = ''
    with conn.cursor() as curs:
        curs.execute('SELECT COUNT(name_product) FROM products WHERE id_type_products = (%s)', str(parameters))  #узнаём сколько всего позиций в категории
        count = int(str(curs.fetchone())[1])   #(int(str(tuple)))

        curs.execute('SELECT name_product FROM products WHERE id_type_products = (%s)', str(parameters)) #выбираем все под категорию
        for i in range(count):
            st = curs.fetchone()
            stroka += '\n' + str(st)[2:-3]
    return stroka