#Guide to Receipt Content:
# Receipt Content - a temp dict to hold the content of the receipts
# Purchase Receipt Content Format:
#{
#    "kind":"Purchase",
#    "Supplier":"{NAME_OF_SUPPLIER}",
#    "Order":{
#        "{PRODUCT_NAME}":{PRODUCT_QTY}
#    }
#}
#Sales Receipt Content Format:
#{
#    "kind":"Sales",
#    "Order":{
#        "{PRODUCT_NAME}":{PRODUCT_QTY}
#    }
#}

import json
from datetime import date

#Receipt Maker Def
def Receipt_Maker(kind,day):

    #Supplier Database
    g = open("Databases/Supplier_Database.json")
    sdb = json.load(g)

    #Product List
    n = open('Databases/Product_List.json')
    pdb = json.load(n)

    #Supplier Database
    g = open("Databases/Supplier_Database.json")
    sdb = json.load(g)

    #Product List
    n = open('Databases/Product_List.json')
    pdb = json.load(n)

    #Sales Log
    z = open("Databases/Sales_Log.json")
    sl = json.load(z)
    #Purchase Receipt Content
    m = open('Databases/Purchase_Receipt_Content.json')
    prdb = json.load(m)
    #Sales Receipt Content
    p = open('Databases/Sales_Receipt_Content.json')
    srdb = json.load(p)

    #General Functions
    Total = 0
    today = date.today()
    today = today.strftime("%m-%d-%Y")
    if kind == "Purchase":
    #Purchase Receipt
        supplier =""
        for i in  prdb[today].keys(): 
            if i  in sdb["Jared's Carriage Retail"]['Products_CostsPHP'].keys():
                supplier = "Jared's Carriage Retail"
            elif i in sdb["Shan's Shampoo"]['Products_CostsPHP'].keys():
                supplier = "Shan's Shampoo"
            elif i in sdb["Shan's Shampoo"]['Products_CostsPHP'].keys():
                supplier = "Shan's Shampoo"
            elif i in sdb["Colyn's Cola"]['Products_CostsPHP'].keys():
                supplier = "Colyn's Cola"
            elif i in sdb["Os' Sauce and salts"]['Products_CostsPHP'].keys():
                supplier = "Os' Sauce and salts"
            elif i in sdb["Reese's Milk and Cheese retail"]['Products_CostsPHP'].keys():
                supplier = "Reese's Milk and Cheese retail"

        #Header
        f = open(f"Receipts_Folder/Purchase Receipts/{today}_{supplier}_Purchase_Receipt.txt","w")
        f.write("---------------------------------------------\n") #40 Spaces
        f.write(f"Supplier :     {supplier}\n")
        f.write(f"Email    :     {sdb[supplier]['Email']}\n")
        f.write(f"Date     :     {today}\n")
        f.write("---------------------------------------------")
        f.write("\n")
        f.close

        #Body
        with open(f"Receipts_Folder/Purchase Receipts/{today}_{supplier}_Purchase_Receipt.txt","a") as f:
            for i in prdb[today].keys():
                Product = i
                Qty = str(prdb[today][i])
                Subtotal = str(int(Qty) * int(sdb[supplier]['Products_CostsPHP'][Product]))
                Total += int(Subtotal)
                while len(Product) < (31-len(Qty)):
                    Product += " "
                if len(Qty) == 1:
                    Qty = "0" + Qty
                while len(str(Qty)) < (10-len(Subtotal)):
                    Qty += " "
                f.write(f"{Product}\t{Qty}\t{Subtotal}\n")

        #Footer
        f = open(f"Receipts_Folder/Purchase Receipts/{today}_{supplier}_Purchase_Receipt.txt","a")
        f.write("---------------------------------------------\n")
        Last_Line = "Total    :"
        while len(Last_Line)< (45-len(str(Total))):
            Last_Line += " "
        f.write(f"{Last_Line}{Total}")
        f.close()
    elif kind == "Sales":
#Sales Receipt
        Total=0
        today = day
        today = today.replace("/","-")
        #Header
        g = open(f"Receipts_Folder/Sales Receipts/{today}_Sales_Receipt.txt","w")
        g.write("---------------------------------------------\n") #40 Spaces
        g.write(f"Date     :     {today}\n")
        g.write("---------------------------------------------")
        g.write("\n")
        g.close

        #Body
        with open(f"Receipts_Folder/Sales Receipts/{today}_Sales_Receipt.txt","a") as g:
            for i in srdb[today].keys():
                Product = str(i)
                Qty = str(srdb[today][i]["Quantity"])
                Subtotal = str(srdb[today][i]["Subtotal"])
                Total += int(Subtotal)
                while len(Product) < (31-len(Qty)):
                    Product += " "
                if len(Qty) == 1:
                    Qty = "0" + Qty
                while len(str(Qty)) < (10-len(Subtotal)):
                    Qty += " "
                g.write(f"{Product}\t{Qty}\t{Subtotal}\n")

        #Footer
        g = open(f"Receipts_Folder/Sales Receipts/{today}_Sales_Receipt.txt","a")
        g.write("---------------------------------------------\n")
        Last_Line = "Total    :"
        while len(Last_Line)< (45-len(str(Total))):
            Last_Line += " "
        g.write(f"{Last_Line}{Total}")
        g.close()

def sales_content_writer(date):
    z = open("Databases/Sales_Log.json")
    sl = json.load(z)
    day = date
    temp = sl[day]
    Date = date.replace("/","-")
    srdb = {}
    srdb[Date] = temp
    with open('Databases/Sales_Receipt_Content.json','w') as b:
        json.dump(srdb,b,indent=4)

def add_temp_orders(i):
    to= []
    to.append(i)
    with open('Databases/temp_purchase_content.json','w') as f:
        json.dump(to,f,indent=4)

def order_sorter():
    j = open('Databases/temp_purchase_content.json')
    to = json.load(j)
    to = to[0]
    e = open('Databases/Supplier_Database.json')
    e = json.load(e)
    a ={}
    b= {}
    c ={}
    g = {}
    h = {}
    for i in range(0,len(to)): #checks which product in the to list
            j = to[i]['product']
            if j in e["Jared's Carriage Retail"]["Products_CostsPHP"].keys():
                    a[j] = to[i]['quantity']
            elif j in e["Shan's Shampoo"]["Products_CostsPHP"].keys():
                    b[j] = to[i]['quantity']
            elif j in e["Colyn's Cola"]["Products_CostsPHP"].keys():
                        c[j] = to[i]['quantity']
            elif j in e["Reese's Milk and Cheese retail"]["Products_CostsPHP"].keys():
                    g[j] = to[i]['quantity']
            elif j in e["Os' Sauce and salts"]["Products_CostsPHP"].keys():
                    h[j] = to[i]['quantity']
    return a,b,c,g,h


def purchase_content_writer(list):
    day = date.today().strftime("%m-%d-%Y")
    srdb = {}
    srdb[day] = list
    with open('Databases/Purchase_Receipt_Content.json','w') as b:
        json.dump(srdb,b,indent=4)