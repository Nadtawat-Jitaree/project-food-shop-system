from function import SellProduct ,Menus , Members , Reports

def Main():
    while True:
        h = "Food Shop System"
        line = "="*len(h)
        print(f"{line}\n{h}\n{line}\n1. Sell Product \n2. Menus\n3. Member\n4. Reports\n5. Exit\n{line}")
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