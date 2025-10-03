import datetime
def SellProduct():
    menus = read_data("Storage/menus.txt")
    members = read_data("Storage/members.txt")
    # เจนจาก จำนวนวินาทีจากปี 1970
    order_id = str(int(datetime.datetime.now().timestamp()))
    table_name = input("Enter Table Name : ")
    mb_id = input("Enter Member ID (or 0 if guest): ")
    if table_name == '':
        table_name = 'Order Takeout'
    if mb_id == '':
        mb_id = '0'

    order_details = []
    subtotal = 0
    discount_rate = 0.0
    if mb_id != "0":
        discount_rate = 0.10 

    try:
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
    except:
        print("Invalid value.\nPlease try again.")

    if not order_details:
        print("No orders made.")
        return

    discount_amount = subtotal * discount_rate
    total_price = subtotal - discount_amount


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

    try:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        report_path = f"report_{date_str}.txt"
        
        with open(f"Reports/{report_path}", "a", encoding="UTF_8") as f:
            f.write(f"\n{'='*40}\n|{'Receipt':^38}|\n{'='*40}\n")
            f.write(f"\n| Order ID     : {order_id:<21} |\n")
            f.write(f"\n| Table Name   : {table_name:<21} |\n")
            f.write(f"\n| Member ID    : {mb_id:<21} |\n")
            f.write(f"\n{'-'*40}\n")
            for od in order_details:
                mn_id, qty, line_total = od[1], od[2], int(float(od[3]))
                name = ""
                for mn in menus:
                    if mn[0] == mn_id:
                        name = mn[2]
                        break
                f.write(f"\n| {name:<12} x{qty:<5} = {line_total:<14,.2f} |\n")
            f.write(f"\n{'-'*40}\n")
            f.write(f"\n| Subtotal     : {subtotal:<21,.2f} |\n")
            if mb_id != "0":
                f.write(f"\n| Discount(10%): {discount_amount:<21,.2f} |\n")
            f.write(f"\n| Total        : {total_price:<21,.2f} |\n")
            f.write(f"\n{'='*40}\n")

        with open("Storage/order_head.txt", "a", encoding="UTF_8") as fout:
            fout.write(order_id + "," + mb_id + "," + str(total_price) + "," +
                    table_name + "," + str(datetime.datetime.now()) + "\n")

        with open("Storage/order_detail.txt", "a", encoding="UTF_8") as fout:
            for od in order_details:
                fout.write(",".join(od) + "\n")

        with open("Storage/menus.txt", "w", encoding="UTF_8") as fout:
            for m in menus:
                fout.write(",".join(m) + "\n")
    except:
        print("An error occurred uploading.")

    print("\nOrder saved successfully!\n")

def read_data(filename):
    datas = []
    try:
        with open(filename) as fin:
            for data in fin:
                data = data.rstrip('\n')
                datas.append(data.split(','))
            return(datas)
    except:
        print("An error occurred while reading data.")


def Menus():
    filename = "Storage/menus.txt"
    try:
        while True:
            h = "Menus"
            print(f"\n{'='*20}\n|{h:^18}|\n{'='*20}\n|{'1. List Menus':<18}|\n|{'2. Add Menu':<18}|\n|{'3. Add Stock':<18}|\n|{'4. Back to Menus':<18}|\n{'='*20}\n")
            choice = input("Enter your choice : ")
            match choice:
                case "1":
                    ListMenus(filename)
                case "2":
                    AddMenu(filename)
                case "3":
                    AddStock(filename)
                case "4":
                    print("Back to Menus...\n")
                    break
                case _:
                    print("\nInvalid value.\nPlease try again.")
    except:
        print("An error occurred.")



def ListMenus(filename):
    try:
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
    except:
        print("An error occurred.")

def AddStock(filename):
    try:
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
    except:
        print("An error occurred.")

    try:
        choice = int(input("Enter menu number to add stock: "))
        if choice < 1 or choice > len(datas):
            print("Invalid menu number.")
        add_qty = int(input("Enter quantity to add: "))
        datas[choice-1][3] = str(int(datas[choice-1][3]) + add_qty)

        with open(filename, "w", encoding="UTF_8") as fout:
             for m in datas:
                fout.write(",".join(m) + "\n")
        print(f"Stock updated successfully! \nNew stock for {datas[choice-1][2]} = {datas[choice-1][3]}")
    except:
        print("An error occurred.")

def AddMenu(filename):
    hdm = "Add Menu"
    line = "-"*20
    print(f"\n{line}\n|{hdm:^18}|\n{line}")
    try:
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
    except:
        print("An error occurred.")


def Members():
    filename = "Storage/members.txt"
    while True:
        h = "Members"
        print(f"\n{'='*20}\n|{h:^18}|\n{'='*20}\n| {'1. List Members':<16} |\n| {'2. Add Member':<16} |\n| {'3. Back to Menus':<16} |\n{'='*20}\n")
        choice = input("Enter your choice : ")
        match choice:
            case "1":
                ListMembers(filename)
            case "2":
                AddMember(filename)
            case "3":
                print("Back to Menus...\n")
                break
            case _:
                print("\nInvalid value.\nPlease try again.")

def ListMembers(filename):
    try:
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
    except:
        print("An error occurred.")

def AddMember(filename):
    hdm = "Add Member"
    line = "-"*20
    print(f"\n{line}\n|{hdm:^18}|\n{line}")
    try:
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
    except:
        print("An error occurred.")
        
def Reports():
    h = "Reports Menu"
    try:
        while True:
            print(f"\n{'='*30}\n|{h:^28}|\n{'='*30}\n| {'1. Order Summary Report':<26} |\n| {'2. Daily Sales Report':<26} |\n| {'3. Member Sales Report':<26} |\n| {'4. Back To Menus':<26} |\n{'='*30}\n")
            choice = input("Enter your choice : ")
            match choice:
                case "1":
                    reportOrder()
                case "2":
                    reportDay()
                case "3":
                    reportMember()
                case "4":
                    print("Back to Menus...\n")
                    break
                case _:
                    print("\nInvalid value.\nPlease try again.")
    except:
        print("An error occurred.")

def reportOrder():
    try:
        members = read_data("Storage/members.txt")
        menus = read_data("Storage/menus.txt")
        orders = read_data("Storage/order_head.txt")
        details = read_data("Storage/order_detail.txt")

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
            print(f"|{n:<4}| {order_id:<15} | {fullname:<20} | {table_name:<10} | {int(float(total_price)):<10,.2f} | {create_date:<30}|")
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
        print(f"| Member     : {fullname:<22} ID : {mb_id}|")
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
        print(f"| Total{'|':>27} {int(float(total_price)):<9,.2f}|")
        print("="*len(hr),"\n")
    except:
        print("An error occurred.")

def reportDay():
    try:
        order_h = "Storage/order_head.txt"
        order_d = "Storage/order_detail.txt"
        menus = read_data("Storage/menus.txt")

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
        # .items() จะได้ key , value นำมา loop
        for menu_name, summary in sales_summary.items():
            print(f"| {n:<5} | {menu_name:<15} | {summary['qty']:<10,.2f} | {summary['total']:<10,.2f} |")
            n += 1

        print("-"*53)
        print(f"| {'Total Sales':<23} | {total_day:<23,.2f} |")
        print("="*53)
    except:
        print("An error occurred.")

def reportMember():
    try:
        order_h = "Storage/order_head.txt"
        order_d = "Storage/order_detail.txt"
        members = read_data("Storage/members.txt")
        menus = read_data("Storage/menus.txt")

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
        print("="*len(hr),"\n")
    except:
        print("An error occurred.")