import psycopg2
from datetime import datetime

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

def print_all(id_param, param, name, count):   #выдаёт позиции выбранной категории print_all("id_product", "products", "name_product", "date_of_creation")
    stroka = ''
    with conn.cursor() as curs:
        curs.execute("SELECT MAX("+id_param+") FROM "+param+"") #, ((id_param),(param)))  #узнаём максимальный id
        max_id = int(str(curs.fetchone())[1:-2])   #(int(str(tuple)))

        curs.execute("SELECT " + name +"," + count + " FROM "+ param + "") #выбираем все под категорию
        for i in range(max_id):
            st = curs.fetchone()
            stroka += '\n' + str(st)[1:-1]
            stroka = stroka.replace("datetime.date", '')
            stroka = stroka.replace("'", '')
    print(stroka)
    return stroka


user_dict = {}
user_dict1 = {1360095076: {'name': 'Венера', 'age': '189', 'type': 'свеча формовая', 'aroma': 'Ваниль', 'color_name': 'violet', 'wish_news': False}}

#print(type(user.get(1360095076).get('name')))

def add_product():
    with conn.cursor() as curs:
        print("1")
        #namber = ((
        curs.execute("SELECT MAX(products.id_product) FROM products") #max.item
        namber = curs.fetchall()
        print("2")
        print(namber, type(namber))
        namber = int((str(namber[0])[1:-2]))
        print(namber, type(namber))
        curs.execute("INSERT INTO products(id_product, name_product,id_type_products,date_of_creation) "
                     "VALUES(" + str(namber+1) + ", ' " + user_dict.get(1360095076).get('name') +"', 1,'"+ str(datetime.now().date()) + "')")
        print("3")
        curs.execute('SELECT * FROM products')
        #a= curs.execute('SELECT * FROM products')
        print("4")
        #curs.fetchall()
        a = curs.fetchall()
        print(a)
        print("5")
        #conn.commit()

def delete_product(id):  #функция на удаление записи из бд по id
    with conn.cursor() as curs:
        curs.execute("DELETE FROM products WHERE id_product = '" + str(id) +"'")
        #curs.fetchall()
        print("ok")
        #conn.commit()


