
from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from datetime import date
import lp_model as lp
import ws_database as db
import receipt_writer as rw
import authentication
import logging
import os
import receipt_writer
import datetime
import lp_model
import json
app = Flask(__name__)

app.secret_key = b'secretkey'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

navbar = """
         <a href='/login'>Login</a> | <a href='/user_interface_page'>User interface</a> | <a href='/saleslog'>Sales Log</a> |
         <a href='/order_input'>Order input</a> | <a href='/receipt'>Receipt</a> | <a href='/deliveryconfirmation'>Delivery confirmation</a>
         <p/>
         """

@app.route('/')
def welcome():
    return render_template("home.html", page="Login")

@app.route('/login',methods=["GET","POST"])
def login():
    return render_template("login.html", page="Login")

@app.route('/auth',methods=["GET","POST"])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    is_successful, admin = authentication.login(username,password)
    app.logger.info("%s", is_successful)
    if(is_successful):
        session["admin"] = admin
        return redirect('/user_interface_page')
    else:
        return redirect('/login')

@app.route('/order_input', methods=["GET","POST"])
def orderinput():
    store_pricing_list=db.get_store_pricing()
    if request.method == "POST":
        req = request.form
        d = date.today().strftime("%m/%d/%Y")
        product_name = req.get("product")
        qty = int(req.get("quantity"))
        price = db.get_sell_price(product_name)
        subtotal = qty*price
        qty<= db.get_product_inventory(product_name)
        db.input_sales(d,product_name,qty,price,subtotal)
        db.subtract_current_inventory(product_name,qty)
        kind = "Sales"
        rw.sales_content_writer(d)
        rw.Receipt_Maker(kind,d)
    return render_template("orderinput.html", page="Customer Order Input",store_pricing_list=store_pricing_list)

@app.route('/orderstocks', methods=["GET","POST"])
def orderstocks():
    lp.LP_Model()
    optimal_stock_list=db.get_optimal_quantity()
    purchase_list=lp.To_Purchase_func()
    if request.method == "POST":
        d = date.today().strftime("%m/%d/%Y")
        for i in purchase_list:
            product_name=i["product"]
            qty=int(i["quantity"])
            price = db.get_purchase_price(product_name)
            subtotal = qty*price
            db.input_purchases(d,product_name,qty,price,subtotal)
            db.add_current_inventory(product_name,qty)
        rw.add_temp_orders(purchase_list)
        Jared,Shan,Colyn,Reese,Os= rw.order_sorter()
        if Jared != {}:
            rw.purchase_content_writer(Jared)
            rw.Receipt_Maker("Purchase",d)
        if Shan != {}:
            rw.purchase_content_writer(Shan)
            rw.Receipt_Maker("Purchase",d)
        if Colyn != {}:
            rw.purchase_content_writer(Colyn)
            rw.Receipt_Maker("Purchase",d)
        if Reese != {}:
            rw.purchase_content_writer(Reese)
            rw.Receipt_Maker("Purchase",d)
        if Os != {}:
            rw.purchase_content_writer(Os)
            rw.Receipt_Maker("Purchase",d)
        return redirect('/purchaselog')
    return render_template("orderstocks.html", page="Order Stocks",optimal_stock_list=optimal_stock_list,purchase_list=purchase_list)

@app.route('/logout')
def logout():
    return redirect("/")

@app.route('/user_interface_page')
def userinterfacepage():
    return render_template("userinterface.html", page="User interface")

@app.route('/saleslog',methods=["GET","POST"])
def saleslog():
    sales_log_list = db.get_sales_log()
    return render_template("saleslog.html", page="Sales Log",sales_log_list=sales_log_list)

@app.route('/purchaselog')
def purchaselog():
    purchase_log_list = db.get_purchase_log()
    return render_template("purchaselog.html", page="Purchase Log",purchase_log_list=purchase_log_list)

@app.route('/salesreceipts',methods=["GET","POST"])
def salesreceipt():
    sales_receipts = db.get_sales_receipts()
    return render_template("salesreceipts.html", page="Sales Receipt",sales_receipts=sales_receipts)

@app.route('/purchasereceipts',methods=["GET","POST"])
def purchasereceipt():
    purchase_receipts = db.get_purchase_receipts()
    return render_template("purchasereceipts.html", page="Purchase Receipt",purchase_receipts=purchase_receipts)

@app.route("/receipt_reader",methods=["GET","POST"])
def receipt_reader():
    receipt = request.form.get('receipt')
    text = db.read_receipt(receipt)
    return render_template("receipt_reader.html",page="Receipt_Reader",receipt=receipt,text=text)

@app.route('/currentinventory')
def currentinventory():
    current_inventory_list = db.get_current_inventory()
    return render_template("currentinventory.html", page="Current Inventory",current_inventory_list=current_inventory_list)


@app.route('/salesreceiptsmaker')
def salesreceiptsmaker():
    return render_template("salesreceiptsmaker.html",page="SalesrReceiptsMaker")

g = open("Databases/Sales_Log.json")
sales_log = json.load(g)
@app.route('/salesrecprg',methods=["GET","POST"])
def salesrecprg():
    if request.method=="POST":
        day = request.form.get('day')
        if day in sales_log:
            kind = request.form.get('kind')
            receipt_writer.sales_content_writer(day)
            receipt_writer.Receipt_Maker(kind,day)
            sales_receipts = db.get_sales_receipts()
            return render_template("salesreceipts.html", page="Sales Receipt",sales_receipts=sales_receipts)
        else:
            return redirect ('/dateinvalid')
@app.route('/dateinvalid')
def dateinvalid():
    return render_template("dateinvalid.html", page="Date Invalid")



@app.route('/reports', methods=["GET","POST"])
def reports():
    lp_model.Report_Generator()
    product_list=db.product_list
    return render_template("reports_page.html",page="reports_page",product_list=product_list)

if __name__ == '__main__':
    app.run(debug=True)
