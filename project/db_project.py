#HotelManagement Bill Generation COde using Class Object and DB Connectivity.
import pyodbc

class Hotel:

    def __init__(self):
        
        
        server = r"MUKU\SQLEXPRESS"
        database = "HotelManagementSystem"

        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )

        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()
        self.menu = self.get_menu()
        self.order = {}

    def get_menu(self):
        self.cursor.execute("select item,price from Menu")
        return dict(self.cursor.fetchall())

    def show_menu(self):
        print("---- MENU ----")
        for item, price in self.menu.items():
            print(item, ":", price)

    def take_order(self):
        while True:
            item = input("Enter item name: ").lower()
            if item in self.menu:
                qty = int(input("Enter quantity: "))
                if item in self.order:
                    self.order[item] += qty
                else:
                    self.order[item] = qty
            else:
                print("Item not available")

            ch = input("Do you want to order more? ").lower()
            if ch != "yes":
                break

    def generate_bill(self):
        print("\n----- BILL -----")
        total = 0
        for item, qty in self.order.items():
            amount = self.menu[item] * qty
            total += amount
            print(item, qty, amount)
            self.cursor.execute(
                "insert into Bills(item,quantity,amount) values(?,?,?)",
                item, qty, amount
            )
        self.conn.commit()
        print("Total Amount =", total)

    def close(self):
        self.conn.close()


h = Hotel()
h.show_menu()
h.take_order()
h.generate_bill()
h.close()
