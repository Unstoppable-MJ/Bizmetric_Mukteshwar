L1 = ["HR", "Finance", "Marketing", "DS"]

class College:

    def __init__(self):
        self.course_fee = 200000
        self.hostel_fee = 200000
        self.food_per_month = 2000
        self.transport_per_sem = 13000

    def calculate_fees(self, subject, analytics, hostel, months, transport):

        total = 0

        fee = self.course_fee

        if subject != "DS" and analytics == "Y":
            fee = fee + (self.course_fee * 0.10)

        total = total + fee

        if hostel == "Y":
            total = total + self.hostel_fee

        total = total + (months * self.food_per_month)

        if transport == "semester" or transport == "annual":
            total = total + (self.transport_per_sem * 2)

        return total


print("Available Courses:", L1)

while True:
    subject = input("Enter subject: ").upper()
    if subject in L1:
        break
    else:
        print("Invalid subject! Please choose from", L1)

while True:
    analytics = input("Do you want analytics? (Y/N): ").upper()
    if analytics in ["Y", "N"]:
        break
    else:
        print("Enter Y or N")

while True:
    hostel = input("Do you want hostel? (Y/N): ").upper()
    if hostel in ["Y", "N"]:
        break
    else:
        print("Enter Y or N")
   

while True:
    transport = input("Transport type (semester/annual): ")
    if transport in ["semester", "annual"]:
        break
    else:
        print("Enter semester or annual")

months = int(input("Food for how many months?: "))

obj = College()

total_amount = obj.calculate_fees(subject, analytics, hostel, months, transport)

print("\n--------Your Entered Details Are:-----------")
print(f"Your Subject:{subject}")
print(f"For Analyatics you entered:{analytics}")
print(f"For Hostel you entered:{hostel}")
print(f"You have entered Food for:{months} Months")
print(f"You have entered Transport type:{transport}")
print("---------------------------------------")
print("Total Annual Fees =", total_amount)
print("---------------------------------------")











