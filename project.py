from function import SellProduct ,Menus , Members , Reports

def Main():
    while True:
        h = "| Food Shop System |"
        line = "="*len(h)
        print(f"{line}\n{h}\n{line}\n| {'1. Order / Sell':<16} |\n| {'2. Manage Menus':<16} |\n| {'3. Manage Member':<16} |\n| {'4. Reports':<16} |\n| {'5. Exit':<16} |\n{line}")
        choice = input("Enter your choice : ")
        match choice:
            case "1":
                SellProduct()
            case "2":
                Menus()
            case "3":
                Members()
            case "4":
                Reports()
            case "5":
                print("Exit Program.")
                break
    
    
if __name__ == "__main__":
    Main()