import datetime
def SellProduct():
    menus = read_data("menus.txt")
    members = read_data("members.txt")

    order_id = str(int(datetime.datetime.now().timestamp()))
    table_name = input("Enter Table Name : ")
    mb_id = input("Enter Member ID (or 0 if guest): ")

    order_details = []
    subtotal = 0
    discount_rate = 0.0
    if mb_id != "0":
        discount_rate = 0.10 

    while True:
        hlm = "| No.|Id    |Type    |Name         |Stock    |Price    |"
        line = "="*len(hlm)
        mess = ""
        mess += f"\n{line}\n|{'List Menus':^54}|\n{line}\n{hlm}\n{line}\n"
        n = 1
        for data in menus:
            mess += f"|{n:3} |{data[0]:6}|{data[1]:8}|{data[2]:13}|{int(data[3]):9,.2f}|{int(data[4]):9,.2f}|\n"
            n += 1
        mess += f"{line}"
        print(mess)

        choice = input("Enter menu number (or 0 to finish): ")
        if choice == "0":
            break

        try:
            choice = int(choice)
            mn_id, mtype, name, stock, price = menus[choice-1]
            stock = int(stock)
            price = float(price)
        except:
            print("Invalid choice.")
            continue

        qty = int(input(f"Enter qty for {name}: "))
        if qty > stock:
            print("Not enough stock!")
            continue

        menus[choice-1][3] = str(stock - qty)

        line_total = qty * price
        order_details.append([order_id, mn_id, str(qty), str(line_total)])
        subtotal += line_total

    if not order_details:
        print("No orders made.")
        return

    discount_amount = subtotal * discount_rate
    total_price = subtotal - discount_amount

    with open("order_head.txt", "a", encoding="UTF_8") as fout:
        fout.write(order_id + "," + mb_id + "," + str(total_price) + "," +
                   table_name + "," + str(datetime.datetime.now()) + "\n")

    with open("order_detail.txt", "a", encoding="UTF_8") as fout:
        for od in order_details:
            fout.write(",".join(od) + "\n")

    with open("menus.txt", "w", encoding="UTF_8") as fout:
        for m in menus:
            fout.write(",".join(m) + "\n")

    print(f"\n{'='*40}\n|{'Receipt':^38}|\n{'='*40}")
    print(f"| Order ID     : {order_id:<21} |")
    print(f"| Table Name   : {table_name:<21} |")
    print(f"| Member ID    : {mb_id:<21} |")
    print("-"*40)
    for od in order_details:
        mn_id, qty, line_total = od[1], od[2], int(float(od[3]))
        name = ""
        for mn in menus:
            if mn[0] == mn_id:
                name = mn[2]
                break
        print(f"| {name:<12} x{qty:<5} = {line_total:<14,.2f} |")
    print("-"*40)
    print(f"| Subtotal     : {subtotal:<21,.2f} |")
    if mb_id != "0":
        print(f"| Discount(10%): {discount_amount:<21,.2f} |")
    print(f"| Total        : {total_price:<21,.2f} |")
    print("="*40)
    print("\nOrder saved successfully!\n")

def read_data(filename):
    datas = []
    with open(filename) as fin:
        for data in fin:
            data = data.rstrip('\n')
            datas.append(data.split(','))
        return(datas)

def Menus():
    filename = "menus.txt"
    while True:
        h = "Menus"
        print(f"\n{'='*20}\n|{h:^18}|\n{'='*20}\n|{'1. List Menus':<18}|\n|{'2. Add Menu':<18}|\n|{'3. Add Stock':<18}|\n|{'4. Back to Menus':<18}|\n{'='*20}\n")
        choice = input("Enter your choice : ")
        match choice:
            case "1":
                datas = read_data(filename)
                hlm = "| No.|  Id  |  Type  |  Name       |  Stock  |  Price  |"
                line = "="*len(hlm)
                mess = ""
                mess += f"\n{line}\n|{'List Menus':^54}|\n{line}\n{hlm}\n{line}\n"
                n = 1
                for data in datas:
                    mess += f"|{n:3} |{data[0]:6}|{data[1]:8}|{data[2]:13}|{int(data[3]):9,.2f}|{int(data[4]):9,.2f}|\n"
                    n += 1
                mess += f"{line}"
                print(mess)
            case "2":
                hdm = "Add Menu"
                line = "-"*20
                print(f"\n{line}\n|{hdm:^18}|\n{line}")
                mn_id = input("Enter Menu ID : ")
                type = input("Enter Menu Type : ")
                name = input("Enter Menu Name : ")
                stock = input("Enter Menu Stock : ")
                price = input("Enter Menu price : ")
                print("\nConfirm To Add This Menu?(Y/N)")
                confirm = input("Enter your confirm : ")
                confirm = confirm.upper()
                if confirm == "Y":
                    fout = open(filename,'a',encoding="UTF_8")
                    fout.write(mn_id+','+type+','+name+','+stock+','+price+'\n')
                    fout.close()
                    print("Save Data Menus allready.\n")
                else:
                    print("You cancle to add menu.")
            case "3":
                datas = read_data(filename)
                hlm = "| No.|  Id  |  Type  |  Name       |  Stock  |  Price  |"
                line = "="*len(hlm)
                mess = ""
                mess += f"\n{line}\n|{'Add Stock - Select Menu':^54}|\n{line}\n{hlm}\n{line}\n"
                n = 1
                for data in datas:
                    mess += f"|{n:3} |{data[0]:6}|{data[1]:8}|{data[2]:13}|{data[3]:9}|{data[4]:9}|\n"
                    n += 1
                mess += f"{line}"
                print(mess)

                try:
                    choice = int(input("Enter menu number to add stock: "))
                    if choice < 1 or choice > len(datas):
                        print("Invalid menu number.")
                        continue
                    add_qty = int(input("Enter quantity to add: "))
                    datas[choice-1][3] = str(int(datas[choice-1][3]) + add_qty)

                    with open(filename, "w", encoding="UTF_8") as fout:
                        for m in datas:
                            fout.write(",".join(m) + "\n")
                    print(f"Stock updated successfully! New stock for {datas[choice-1][2]} = {datas[choice-1][3]}")
                except:
                    print("Invalid input.")
            case "4":
                print("Back to Menus...\n")
                break

def Members():
    filename = "members.txt"
    while True:
        h = "Members"
        print(f"\n{'='*20}\n|{h:^18}|\n{'='*20}\n| {'1. List Members':<16} |\n| {'2. Add Member':<16} |\n| {'3. Back to Menus':<16} |\n{'='*20}\n")
        choice = input("Enter your choice : ")
        match choice:
            case "1":
                datas = read_data(filename)
                hlm = "| No.|  Id  |  FullName          |  tel      |"
                line = "="*len(hlm)
                mess = ""
                mess += f"\n{line}\n|{'List Menus':^44}|\n{line}\n{hlm}\n{line}\n"
                n = 1
                for data in datas:
                    mess += f"|{n:3} |{data[0]:6}|{data[1]:20}|{data[2]:11}|\n"
                    n += 1
                mess += f"{line}"
                print(mess)
            case "2":
                hdm = "Add Member"
                line = "-"*20
                print(f"\n{line}\n|{hdm:^18}|\n{line}")
                mb_id = input("Enter Member ID : ")
                fullname = input("Enter Member FullName : ")
                tel = input("Enter Member Telephone Number : ")
                print("\nConfirm To Add This Member?(Y/N)")
                confirm = input("Enter your confirm : ")
                confirm = confirm.upper()
                if confirm == "Y":
                    fout = open(filename,'a',encoding="UTF_8")
                    fout.write(mb_id+','+fullname+','+tel+'\n')
                    fout.close()
                    print("Save Data Member allready.\n")
                else:
                    print("You cancle to add member.")
            case "3":
                print("Back to Menus...\n")
                break

def Reports():
    h = "Reports Menu"
    print(f"\n{'='*20}\n|{h:^18}|\n{'='*20}\n|{'1. Report Orders':^18}|\n|{'2. Report Daily':^18}|\n|{'3. Report Member':^18}|\n{'='*20}\n")
    choice = input("Enter your choice : ")
    match choice:
        case "1":
            reportOrder()
        case "2":
            reportDay()
        case "3":
            reportMember()

def reportOrder():
    order_h = "order_head.txt"
    order_d = "order_detail.txt"
    members = read_data("members.txt")
    menus = read_data("menus.txt")
    orders = read_data(order_h)
    details = read_data(order_d)

    hol = f"|{'No.':<4}| {'OrderID':<15} | {'Member':<20} | {'Table':<10} | {'Total':<10} | {'Date':<30}|"
    print(f"\n{'='*len(hol)}\n|{'Order List':^103}|")
    print(f"{'='*len(hol)}\n{hol}\n{'='*len(hol)}")
    n = 1
    for order in orders:
        order_id, mb_id, total_price, table_name, create_date = order
        fullname = "Guest"
        for mb in members:
            if mb[0] == mb_id:
                fullname = mb[1]
                break
        print(f"|{n:<4}| {order_id:<15} | {fullname:<20} | {table_name:<10} | {total_price:<10} | {create_date:<30}|")
        n += 1
    print(f"{'='*len(hol)}")

    ord = input("\nEnter order number to view details (0=cancel): ")
    if ord == "0":
        print("Cancel report.")
        return
    
    try:
        ord = int(ord)
        order = orders[ord-1]
    except:
        print("Invalid choice.")
        return

    order_id, mb_id, total_price, table_name, create_date = order
    fullname = "Guest"
    for mb in members:
        if mb[0] == mb_id:
            fullname = mb[1]
            break

    hr = f"|{'No.':<5}|{'Menu':<15}|{'Qty':<10}|{'Price':<10}|"
    print("\n" + "="*len(hr))
    print(f"|{'Order Detail':^43}|")
    print("" + "="*len(hr))
    print(f"| Order ID   : {order_id:<29}|")
    print(f"| Member     : {fullname} ID : {mb_id:<18}|")
    print(f"| Table Name : {table_name:<29}|")
    print(f"| Date       : {create_date:<29}|")
    print(f"| Total Price: {int(float(total_price)):<29,.2f}|")
    print("-"*len(hr))
    print(hr)
    print("-"*len(hr))

    n = 1
    for d in details:
        if d[0] == order_id:
            mn_id, qty, price = d[1], d[2], d[3]
            menu_name = ""
            for mn in menus:
                if mn[0] == mn_id:
                    menu_name = mn[2]
                    break
            print(f"| {n:<4}| { menu_name:<14}| {int(float(qty)):<9,.2f}| {int(float(price)):<9,.2f}|")
            n += 1
    print("-"*len(hr))
    print(f"|{'|':>33} {int(float(total_price)):<9,.2f}|")
    print("="*len(hr),"\n")

def reportDay():
    order_h = "order_head.txt"
    order_d = "order_detail.txt"
    menus = read_data("menus.txt")

    day = input("Enter date (YYYY-MM-DD): ")

    orders = read_data(order_h)
    details = read_data(order_d)
    order_ids = []
    for order in orders:
        order_id, mb_id, total_price, table_name, create_date = order
        # startswith ใช้ตรวจสอบว่าค่า day ที่รับมาตรงกับ create_date ไหนบ้าง
        if create_date.startswith(day):
            order_ids.append(order_id)

    if not order_ids:
        print(f"\nNo orders found for {day}")
        return

    sales_summary = {}
    total_day = 0

    for d in details:
        if d[0] in order_ids: 
            mn_id, qty, price = d[1], int(d[2]), float(d[3])

            menu_name = ""
            for mn in menus:
                if mn[0] == mn_id:
                    menu_name = mn[2]
                    break

            if menu_name not in sales_summary:
                sales_summary[menu_name] = {"qty": 0, "total": 0.0}
            sales_summary[menu_name]["qty"] += qty
            sales_summary[menu_name]["total"] += price
            total_day += price

    print("\n" + "="*53)
    print(f"| {'Daily Sales Report for':>30} {day:<18} |")
    print("="*53)
    print(f"| {'No.':<5} | {'Menu':<15} | {'Qty':<10} | {'Total':<10} |")
    print("-"*53)

    n = 1
    for menu_name, summary in sales_summary.items():
        print(f"| {n:<5} | {menu_name:<15} | {summary['qty']:<10,.2f} | {summary['total']:<10,.2f} |")
        n += 1

    print("-"*53)
    print(f"| {'Total Sales':<23} | {total_day:<23,.2f} |")
    print("="*53)

def reportMember():
    order_h = "order_head.txt"
    order_d = "order_detail.txt"
    members = read_data("members.txt")
    menus = read_data("menus.txt")

    print(f"\n{'='*52}\n|{'Members List':^50}|\n{'='*52}")
    n = 1
    print(f"| No. | {'FullName':<20} | {'ID':<6} | {'Telephone':<10} |\n{'='*52}")
    for mb in members:
        print(f"| {n:<3} | {mb[1]:<20} | {mb[0]:<6} | {mb[2]:<10} |")
        n += 1
    print("="*52)

    sel = input("\nEnter member number to view report (0=cancel): ")
    if sel == "0":
        print("Cancel report.")
        return

    try:
        sel = int(sel)
        mb_id = members[sel-1][0]
        fullname = members[sel-1][1]
    except:
        print("Invalid choice.")
        return

    orders = read_data(order_h)
    details = read_data(order_d)

    order_ids = []
    for order in orders:
        order_id, ob_mb_id, total_price, table_name, create_date = order
        if ob_mb_id == mb_id:
            order_ids.append(order_id)

    if not order_ids:
        print(f"\nNo orders found for member: {fullname}")
        return

    sales_summary = {}
    total_member = 0

    for d in details:
        if d[0] in order_ids:
            mn_id, qty, price = d[1], int(d[2]), float(d[3])

            menu_name = ""
            for mn in menus:
                if mn[0] == mn_id:
                    menu_name = mn[2]
                    break

            if menu_name not in sales_summary:
                sales_summary[menu_name] = {"qty": 0, "total": 0.0}
            sales_summary[menu_name]["qty"] += qty
            sales_summary[menu_name]["total"] += price
            total_member += price

    hr = f"|{'No.':<5}|{'Menu':<17}|{'Qty':<11}|{'Total':<12}|"
    print("\n" + "="*len(hr))
    print(f"|{'Sales Report by Member':^{len(hr)-2}}|")
    print("="*len(hr))
    print(f"| Member : {fullname:<26} ID: {mb_id:<6} |")
    print("-"*len(hr))
    print(hr)
    print("-"*len(hr))

    n = 1
    for menu_name, summary in sales_summary.items():
        print(f"| {n:<4}| {menu_name:<16}| {summary['qty']:<10,.2f}| {summary['total']:<11,.2f}|")
        n += 1

    print("-"*len(hr))
    print(f"|{'Total Sales':<35}| {total_member:<11,.2f}|")
    print("="*len(hr))
