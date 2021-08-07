from flask import sessions
import json
import os
#Admin Database
f = open("Databases/Admin_List.json")
admin = json.load(f)

def get_user(username):
    try:
       return admin[username]
    except KeyError:
       return None

#Sales Log Database
g = open("Databases/Sales_Log.json")
sales_log = json.load(g)
def get_sales_log():
    sales_log_list = []

    sales_log_dict={}
    for i,v in sales_log.items():
        for k in v:
            sales_log_dict[i]={"date":i,"product":k,"quantity":v[k]["Quantity"],"price":v[k]["Price"],"subtotal":v[k]["Subtotal"]}
            log = sales_log_dict[i]
            sales_log_list.append(log)

    return sales_log_list

#Purchase Log Database

def get_purchase_log():
    h = open("Databases/Purchase_Log.json")
    purchase_log = json.load(h)

    purchase_log_list = []

    purchase_log_dict={}
    for i,v in purchase_log.items():
        for k in v:
            purchase_log_dict[i]={"date":i,"product":k,"quantity":v[k]["Quantity"],"price":v[k]["Price"],"subtotal":v[k]["Subtotal"]}
            log = purchase_log_dict[i]
            purchase_log_list.append(log)

    return purchase_log_list

#Supplier Database
m = open("Databases/Supplier_Database.json")
supplier_info = json.load(m)

def get_supplier_pricing():
    supplier_pricing_list = []

    supplier_pricing_dict={}
    for i,v in supplier_info.items():
        for j,k in v["Products_CostsPHP"].items():
            supplier_pricing_dict={"product":j,"price":k}
            product = supplier_pricing_dict
            supplier_pricing_list.append(product)


    return supplier_pricing_list

#Product Database
n = open("Databases/Product_List.json")
product_list = json.load(n)
def get_sell_price(product_name):
    price = product_list[product_name]
    return price

f = open("Databases/Supplier_Database.json")
supplier_db=json.load(f)
def get_purchase_price(product_name):
    buy_price_dict={}
    for i in supplier_db.values():
        for k in i['Products_CostsPHP']:
            buy_price_dict[k]=i['Products_CostsPHP'][k]
    price = int(buy_price_dict[product_name])
    return price

def get_store_pricing():
    store_pricing_list = []
    store_pricing_dict={}
    for i,j in product_list.items():
        store_pricing_dict={"product":i,"price":j}
        product = store_pricing_dict
        store_pricing_list.append(product)
    return store_pricing_list

def input_sales(date,product_name,qty,price,subtotal):
    if date not in sales_log:
        sales_log[date]={product_name:{"Quantity": qty,"Price": price, "Subtotal": subtotal}}
    else:
        if product_name not in sales_log[date]:
            sales_log[date][product_name]={"Quantity": qty,"Price": price, "Subtotal": subtotal}
        elif product_name in sales_log[date]:
            qty = qty + sales_log[date][product_name]["Quantity"]
            subtotal = qty*price
            sales_log[date][product_name]={"Quantity": qty,"Price": price, "Subtotal": subtotal}
    with open("Databases/Sales_log.json","w") as log:
        json.dump(sales_log,log,indent=4)

def input_purchases(date,product_name,qty,price,subtotal):
    h = open("Databases/Purchase_Log.json")
    purchase_log = json.load(h)
    if date not in purchase_log:
        purchase_log[date]={product_name:{"Quantity": qty,"Price": price, "Subtotal": subtotal}}
    else:
        if product_name not in purchase_log[date]:
            purchase_log[date][product_name]={"Quantity": qty,"Price": price, "Subtotal": subtotal}
        elif product_name in purchase_log[date]:
            qty = qty + purchase_log[date][product_name]["Quantity"]
            subtotal = qty*price
            purchase_log[date][product_name]={"Quantity": qty,"Price": price, "Subtotal": subtotal}
    with open("Databases/Purchase_Log.json","w") as log:
        json.dump(purchase_log,log,indent=4)


def price_change(product,value):
    product_list[product] = value

    with open('Databases/Product_List.json',"w") as d:
        json.dump(product_list,d,indent=4)

#Current Inventory
o = open("Databases/Current_Inventory.json")
current_inventory = json.load(o)

def get_current_inventory():
    current_inventory_list = []

    current_inventory_dict = {}
    for i,v in current_inventory.items():
        current_inventory_dict = {"product":i,"quantity":v}
        product = current_inventory_dict
        current_inventory_list.append(product)
    return current_inventory_list


def get_product_inventory(product_name):
    quantity=current_inventory[product_name]
    return quantity

def subtract_current_inventory(product_name,qty):
    current_inventory[product_name]=current_inventory[product_name]-qty

    with open("Databases/Current_Inventory.json","w")as c_i:
        json.dump(current_inventory,c_i,indent=4)

def add_current_inventory(product_name,qty):
    current_inventory[product_name]=current_inventory[product_name]+qty

    with open("Databases/Current_Inventory.json","w")as c_i:
        json.dump(current_inventory,c_i,indent=4)

#Receipt Files
path = os.getcwd()+"/Receipts_Folder/Sales Receipts"
path2 = os.getcwd()+"/Receipts_Folder/Purchase Receipts"
sales_receipts = {}
purchase_receipts = {}

def get_sales_receipts():
    for filename in os.listdir(path):
        sales_receipts[filename] = "Receipts_Folder/Sales Receipts/"+filename
    return sales_receipts
def get_purchase_receipts():
    for filename in os.listdir(path2):
        purchase_receipts[filename] = "Receipts_Folder/Purchase Receipts/"+filename
    return purchase_receipts

#Read Receipt Files
def read_receipt(filepath):
    with open(filepath,"r") as f:
        lines = f.read()
    return lines

p = open("Databases/IdealProductList.json")
optimal_stock = json.load(p)
def get_optimal_quantity():
    optimal_stock_list=[]
    optimal_stock_dict={}
    for i in optimal_stock:
        optimal_stock_dict[i]={"product":i,"quantity":optimal_stock[i]}
        product=optimal_stock_dict[i]
        optimal_stock_list.append(product)

    return optimal_stock_list
