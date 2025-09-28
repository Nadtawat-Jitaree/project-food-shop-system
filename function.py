import datetime
def SellProduct():
    menus = read_data("menus.txt")
    members = read_data("members.txt")

    order_id = str(int(datetime.datetime.now().timestamp()))
    table_name = input("Enter Table Name : ")
    mb_id = input("Enter Member ID (or 0 if guest): ")
    order_details = []
    total_price = 0

    while True:
        hlm = "| No.|Id    |Type    |Name         |Stock    |Price    |"
        line = "="*len(hlm)
        mess = ""
        mess += f"\n{line}\n{'List Menus':^{len(hlm)}}\n{line}\n{hlm}\n{line}\n"
        n = 1
        for data in menus:
            mess += f"|{n:3} |{data[0]:6}|{data[1]:8}|{data[2]:13}|{data[3]:9}|{data[4]:9}|\n"
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
        total_price += line_total

    if not order_details:
        print("No orders made.")
        return

    with open("order_head.txt", "a", encoding="UTF_8") as fout:
        fout.write(order_id + "," + mb_id + "," + str(total_price) + "," +
                   table_name + "," + str(datetime.datetime.now()) + "\n")

    with open("order_detail.txt", "a", encoding="UTF_8") as fout:
        for od in order_details:
            fout.write(",".join(od) + "\n")

    with open("menus.txt", "w", encoding="UTF_8") as fout:
        for m in menus:
            fout.write(",".join(m) + "\n")

    print("Order saved successfully!")

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
        print(f"\n{'='*20}\n{h:^20}\n{'='*20}\n1. List Menus\n2. Add Menu\n3. Back to Menus\n{'='*20}\n")
        choice = input("Enter your choice : ")
        match choice:
            case "1":
                datas = read_data(filename)
                hlm = "| No.|  Id  |  Type  |  Name       |  Stock  |  Price  |"
                line = "="*len(hlm)
                mess = ""
                mess += f"\n{line}\n{'List Menus':^{len(hlm)}}\n{line}\n{hlm}\n{line}\n"
                n = 1
                for data in datas:
                    mess += f"|{n:3} |{data[0]:6}|{data[1]:8}|{data[2]:13}|{data[3]:9}|{data[4]:9}|\n"
                    n += 1
                mess += f"{line}"
                print(mess)
            case "2":
                hdm = "Enter Data Menu."
                line = "-"*len(hdm)
                print(f"\n{line}\n{hdm}\n{line}")
                mn_id = input("Enter ID : ")
                type = input("Enter Type : ")
                name = input("Enter Name : ")
                stock = input("Enter stock : ")
                price = input("Enter price : ")
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
                print("Back to Menus...\n")
                break
def Members():
    filename = "members.txt"
    while True:
        h = "Members"
        print(f"\n{'='*20}\n{h:^20}\n{'='*20}\n1. List Members\n2. Add Member\n3. Back to Menus\n{'='*20}\n")
        choice = input("Enter your choice : ")
        match choice:
            case "1":
                datas = read_data(filename)
                hlm = "| No.|  Id  |  FullName          |  tel      |"
                line = "="*len(hlm)
                mess = ""
                mess += f"\n{line}\n{'List Menus':^{len(hlm)}}\n{line}\n{hlm}\n{line}\n"
                n = 1
                for data in datas:
                    mess += f"|{n:3} |{data[0]:6}|{data[1]:20}|{data[2]:11}|\n"
                    n += 1
                mess += f"{line}"
                print(mess)
            case "2":
                hdm = "Enter Data Member."
                line = "-"*len(hdm)
                print(f"\n{line}\n{hdm}\n{line}")
                mb_id = input("Enter ID : ")
                fullname = input("Enter FullName : ")
                tel = input("Enter telephone number : ")
                print("\nConfirm To Add This Member?(Y/N)")
                confirm = input("Enter your confirm : ")
                confirm = confirm.upper()
                if confirm == "Y":
                    fout = open(filename,'a',encoding="UTF_8")
                    fout.write(mb_id+','+fullname+','+tel+'\n')
                    fout.close()
                    print("Save Data Member allready.\n")
                else:
                    print("You cancle to add menu.")
            case "3":
                print("Back to Menus...\n")
                break

def Reports():
    order_h = "order_head.txt"
    order_d = "order_detail.txt"
    members = read_data("members.txt")
    menus = read_data("menus.txt")

    h = "Reports"
    print(f"\n{'='*20}\n{h:^20}\n{'='*20}\n1. Report Orders\n{'='*20}\n")
    choice = input("Enter your choice : ")
    match choice:
        case "1":
            orders = read_data(order_h)
            details = read_data(order_d)

            print(f"\n{'='*20}\n{'Order List':^20}\n{'='*20}\n")
            hol = f"{'No.':<5}| {'OrderID':<15} | {'Member':<15} | {'Table':<10} | {'Total':<10} | {'Date':<30}|"
            print(f"{'='*len(hol)}\n{hol}\n{'='*len(hol)}")
            n = 1
            for order in orders:
                order_id, mb_id, total_price, table_name, create_date = order
                fullname = "Guest"
                for mb in members:
                    if mb[0] == mb_id:
                        fullname = mb[1]
                        break
                print(f"{n:<5}| {order_id:<15} | {fullname:<15} | {table_name:<10} | {total_price:<10} | {create_date:<30}|")
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

            print("\n" + "="*50)
            print(f"Order ID   : {order_id}")
            print(f"Member     : {fullname} (ID:{mb_id})")
            print(f"Table Name : {table_name}")
            print(f"Date       : {create_date}")
            print(f"Total Price: {total_price}")
            hr = f"|{'No.':<5}|{'Menu':<20}|{'Qty':<5}|{'Price':<10}|"
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
                    print(f"|{n:<5}|{menu_name:<20}|{qty:<5}|{price:<10}|")
                    n += 1
            print("-"*len(hr))
            print(f"{'|':>34}{total_price:<10}|")
            print("="*len(hr),"\n")