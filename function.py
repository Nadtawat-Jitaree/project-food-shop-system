def SellProduct():
    print()

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
        print(f"\n{'='*20}\n{h:^20}\n{'='*20}\n1. List Menus\n2. Add Menu\n3. Exit\n{'='*20}\n")
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
                print("Exit Menus...\n")
                break
def Members():
    print()

def Reports():
    print()