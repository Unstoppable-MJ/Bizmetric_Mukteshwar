import pyodbc
from datetime import datetime

class Hotel:

    def __init__(self):

        server = r"GANESH\SQLEXPRESS"
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
        print("\n" + "="*40)
        print(" " * 12 + "MENU")
        print("="*40)
        for item, price in self.menu.items():
            print(f"{item:<25}{price:>10}")
        print("="*40)

    def take_order(self):
        while True:
            item = input("Enter item name: ").lower()
            if item in self.menu:
                qty = int(input("Enter quantity: "))
                self.order[item] = self.order.get(item, 0) + qty
            else:
                print("Item not available")

            ch = input("Do you want to order more? ").lower()
            if ch != "yes":
                break

    def generate_bill(self):

        width = 50
        total = 0
        lines = []

        def center(text):
            return text.center(width)

        def row(col1, col2, col3):
            return f"| {col1:<20} | {col2:^5} | {col3:>10} |"

        border = "+" + "-"*(width-2) + "+"

        print("\n" + border)
        print("|" + center("HOTEL BILL") + "|")
        print("|" + center(datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "|")
        print(border)

        header = row("Item", "Qty", "Amount")
        print(header)
        print(border)

        lines.append(border)
        lines.append("|" + center("HOTEL BILL") + "|")
        lines.append("|" + center(datetime.now().strftime("%d-%m-%Y %H:%M:%S")) + "|")
        lines.append(border)
        lines.append(header)
        lines.append(border)

        for item, qty in self.order.items():
            amount = self.menu[item] * qty
            total += amount

            bill_row = row(item, qty, amount)
            print(bill_row)
            lines.append(bill_row)

            self.cursor.execute(
                "insert into Bills(item,quantity,amount) values(?,?,?)",
                item, qty, amount
            )

        print(border)
        total_line = f"| {'TOTAL':<20} | {'':^5} | {total:>10} |"
        print(total_line)
        print(border)

        lines.append(border)
        lines.append(total_line)
        lines.append(border)

        self.conn.commit()

        filename = datetime.now().strftime("bill_%Y%m%d_%H%M%S.txt")

        with open(filename, "w") as f:
            for line in lines:
                f.write(line + "\n")

    def close(self):
        self.conn.close()


h = Hotel()
h.show_menu()
h.take_order()
h.generate_bill()
h.close()
