import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://nme2117:996785@34.73.36.248/project1"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass
  
@app.route('/')
def index():
  print(request.args)  
  return render_template("index2.html")

#ADD NEW PAGES HERE
@app.route('/customer2/')
def customer():
  #total custumers (online and in store)
  cursor = g.conn.execute("SELECT COUNT(receipt_id) FROM payment")
  total_count = []
  for result in cursor:
    total_count.append(result['count'])
  cursor.close()
  context1 = dict(data1 = total_count)
  
  #total online customers
  cursor = g.conn.execute("SELECT COUNT(cust_id) FROM customer")
  online_count = []
  for result in cursor:
    online_count.append(result['count'])
  cursor.close()
  context2 = dict(data2 = online_count)
  
  #total online customers
  cursor = g.conn.execute("SELECT COUNT(receipt_id) FROM sale")
  store_count = []
  for result in cursor:
    store_count.append(result['count'])
  cursor.close()
  context3 = dict(data3 = store_count)

  return render_template("customer2.html", **context1, **context2, **context3)

#location search
@app.route('/location-search', methods=['POST'])
def location_search():
  loc = request.form['location']
  cursor = g.conn.execute("SELECT * FROM shipping_info WHERE city LIKE %s OR country LIKE %s OR state LIKE %s OR zip LIKE %s", (loc,loc,loc,loc,))
  cust_results = []
  for result in cursor:
    cust_results.append(result[0:])
  cursor.close()
  context1 = dict(data1 = cust_results)
    
  return render_template("location-search-results.html", **context1, value=loc)

#inventory page
@app.route('/inventory', methods= ['POST','GET'])
def inventory():
  print(request.args)
  cursor = g.conn.execute("SELECT * FROM inventory")
  inventory_count = []
  for result in cursor:
    inventory_count.append(result[0:])
  cursor.close()
  context1 = dict(data1 = inventory_count)
  
  return render_template("inventory.html", **context1)

#customer orders
@app.route('/orders', methods=['POST'])
def orders():
  customer = request.form['cust_id']
  cursor = g.conn.execute("SELECT shopping_cart.cust_id, shopping_cart.order_number, orders.order_date, shopping_cart.SKU, products.name, products.price, shopping_cart.quantity FROM (shopping_cart NATURAL JOIN products) NATURAL JOIN orders WHERE shopping_cart.cust_id LIKE %s", (customer,))
  order_results = []
  for result in cursor:
    order_results.append(result[0:])
  cursor.close()
  context = dict(data = order_results)
    
  return render_template("orders.html", **context, value=customer)

#employee 
@app.route('/employee/')
def employee():
  cursor = g.conn.execute("SELECT COUNT(employee_id) FROM employee")
  employee_count = []
  for result in cursor:
    employee_count.append(result['count'])
  cursor.close()
  context1 = dict(data1 = employee_count)
    
  cursor = g.conn.execute("SELECT works_at.store_id, employee.* FROM employee NATURAL JOIN works_at GROUP BY works_at.store_id, employee.employee_id ORDER BY works_at.store_id")
  employee_count = []
  for result in cursor:
    employee_count.append(result[0:])
  cursor.close()
  context2 = dict(data2 = employee_count)
  
  return render_template("employee.html", **context1, **context2)

#tops page
@app.route('/tops')
def tops():
  cursor = g.conn.execute("SELECT DISTINCT(name), color, price, cost FROM products WHERE category = 'tops'")
  top_count = []
  for result in cursor:
    top_count.append(result[0:])
  cursor.close()
  context1 = dict(data1 = top_count)
  
  return render_template("tops.html", **context1)

#bottoms page
@app.route('/bottoms')
def bottoms():
  cursor = g.conn.execute("SELECT DISTINCT(name), color, price, cost FROM products WHERE category = 'bottoms'")
  bottom_count = []
  for result in cursor:
    bottom_count.append(result[0:])
  cursor.close()
  context1 = dict(data1 = bottom_count)
  
  return render_template("bottoms.html", **context1)

#dresses page
@app.route('/dresses')
def dresses():
  cursor = g.conn.execute("SELECT DISTINCT(name), color, price, cost FROM products WHERE category = 'dresses'")
  dresses_count = []
  for result in cursor:
    dresses_count.append(result[0:])
  cursor.close()
  context1 = dict(data1 = dresses_count)
  
  return render_template("dresses.html", **context1)

#accessories page
@app.route('/accessories')
def accessories():
  cursor = g.conn.execute("SELECT DISTINCT(name), color, price, cost FROM products WHERE category = 'accessories'")
  accessories_count = []
  for result in cursor:
    accessories_count.append(result[0:])
  cursor.close()
  context1 = dict(data1 = accessories_count)
  
  return render_template("accessories.html", **context1)

#financial statements 
@app.route('/finance')
def finance():
  cursor = g.conn.execute("SELECT COUNT(card_number) FROM card")
  card_count = []
  for result in cursor:
    card_count.append(result['count'])
  cursor.close()
  context1 = dict(data1 = card_count)
  
  cursor = g.conn.execute("SELECT * FROM card")
  card = []
  for result in cursor:
    card.append(result[0:])
  cursor.close()
  context2 = dict(data2 = card)
  
  cursor = g.conn.execute("SELECT COUNT(receipt_id) FROM cash")
  cash_count = []
  for result in cursor:
    cash_count.append(result['count'])
  cursor.close()
  context3 = dict(data3 = card_count)
  
  cursor = g.conn.execute("SELECT * FROM cash")
  cash = []
  for result in cursor:
    cash.append(result[0:])
  cursor.close()
  context4 = dict(data4 = cash)
  
  cursor = g.conn.execute("SELECT COUNT(gift_card_number) FROM gift_card")
  gift_card_count = []
  for result in cursor:
    gift_card_count.append(result['count'])
  cursor.close()
  context5 = dict(data5 = gift_card_count)
  
  cursor = g.conn.execute("SELECT * FROM gift_card")
  gift_card = []
  for result in cursor:
    gift_card.append(result[0:])
  cursor.close()
  context6 = dict(data6 = gift_card)
  
  return render_template("finance.html", **context1, **context2, **context3, **context4, **context5, **context6)

#referrals
@app.route('/referrals')
def referrals():
  cursor = g.conn.execute("SELECT shipping_info.cust_id, shipping_info.first_name, shipping_info.last_name FROM customer NATURAL JOIN shipping_info WHERE customer.is_referral_member = 1")
  ref_members = []
  for result in cursor:
    ref_members.append(result[0:])
  cursor.close()
  context1 = dict(data1 = ref_members)
  
  cursor = g.conn.execute("SELECT DISTINCT (member_id), member_code, member_points FROM referral")
  members = []
  for result in cursor:
    members.append(result[0:])
  cursor.close()
  context2 = dict(data2 = members)
  
  return render_template("referrals.html", **context1, **context2)

@app.route('/new_employee', methods=['POST'])
def new_hire():
  store_id = request.form.get('store_id', False)
  employee_id = request.form.get('employee_id', False)
  first_name = request.form.get('first_name', False)
  middle_name = request.form.get('middle_name', False)
  last_name = request.form.get('last_name', False)
  sex = request.form.get('sex', False)
  age = request.form.get('age', False)
  position = request.form.get('position', False)
  salary = request.form.get('salary', False)
  start_date = request.form.get('start_date', False)
  
  g.conn.execute("INSERT INTO employee(employee_id, first_name, middle_name, last_name, sex, age, position, salary, start_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (employee_id, first_name, middle_name, last_name, sex, age, position, salary, start_date,))
  g.conn.execute("INSERT INTO works_at(employee_id, store_id) VALUES (%s, %s)", (employee_id, store_id,))
  return redirect('/employee/')

@app.route('/store', methods=['POST'])
def store_search():
  store_id = request.form['store_id']
  cursor = g.conn.execute("SELECT * FROM inventory WHERE store_id = %s", (store_id,))
  store_results = []
  for result in cursor:
    store_results.append(result[0:])
  cursor.close()
  context1 = dict(data1 = store_results)
  
  cursor = g.conn.execute("SELECT COUNT(SKU) FROM inventory NATURAL JOIN products WHERE inventory.store_id = %s AND products.category = 'tops'", (store_id,))
  top_results = []
  for result in cursor:
    top_results.append(result[0])
  cursor.close()
  context2 = dict(data2 = top_results)
  
  cursor = g.conn.execute("SELECT COUNT(SKU) FROM inventory NATURAL JOIN products WHERE inventory.store_id = %s AND products.category = 'bottoms'", (store_id,))
  bottom_results = []
  for result in cursor:
    bottom_results.append(result[0])
  cursor.close()
  context3 = dict(data3 = top_results)
  
  cursor = g.conn.execute("SELECT COUNT(SKU) FROM inventory NATURAL JOIN products WHERE inventory.store_id = %s AND products.category = 'dresses'", (store_id,))
  dress_results = []
  for result in cursor:
    dress_results.append(result[0])
  cursor.close()
  context4 = dict(data4 = dress_results)
  
  cursor = g.conn.execute("SELECT COUNT(SKU) FROM inventory NATURAL JOIN products WHERE inventory.store_id = %s AND products.category = 'accessories'", (store_id,))
  access_results = []
  for result in cursor:
    access_results.append(result[0])
  cursor.close()
  context5 = dict(data5 = access_results)
    
  return render_template("store-results.html", **context1,  **context2, **context3, **context4, **context5, value=store_id)

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  
  run()
