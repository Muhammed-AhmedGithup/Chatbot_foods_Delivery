import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mohamed",
    database="pandeyji_eatery"
)

# Create a cursor object
def order_track_satus(order_id):
    cursor=connection.cursor()
    cursor.execute(f'SELECT * FROM pandeyji_eatery.order_tracking where order_id={order_id};')
    result=cursor.fetchone()
    if result is not None:
        return result
    else: return None
    
    
def save_order(dic:dict):
    sum_of_price=0
    cursor=connection.cursor()
    status='delivered'
    cursor.execute('insert into order_tracking (status) values(%s)',(status,))
    order_id=cursor.lastrowid
    for k,v in dic.items():
        cursor.execute('select * from food_items where name=%s',(k,))
        item=cursor.fetchone()
        item_id=item[0]
        total_price=v*float(item[2])
        sum_of_price+=total_price
        quantity=v
        cursor.execute(f'insert into orders (order_id,item_id,quantity,total_price) values({order_id},{item_id},{quantity},{total_price})')
    connection.commit()
    return order_id , sum_of_price
        


