# =====================================
# LOLA HOTEL RESERVATION MANAGEMENT SYSTEM
# =====================================

ROOMS_FILE = "rooms.txt"
GUESTS_FILE = "guests.txt"
BOOKINGS_FILE = "bookings.txt"
PAYMENTS_FILE = "payments.txt"
HOUSEKEEPING_FILE = "housekeeping.txt"


# ---------- FILE HELPERS ----------

def read_file(file):
    try:
        with open(file, "r") as f:
            return f.readlines()
    except:
        return []

def write_file(file, lines):
    with open(file, "w") as f:
        f.writelines(lines)


# ---------- COMMON CHECKS ----------

def id_exists(file, index, value):
    for l in read_file(file):
        if l.strip().split("|")[index] == value:
            return True
    return False


# ---------- MANAGER ----------

def add_room():
    room_id = input("Room ID (R001): ") 
    if id_exists(ROOMS_FILE, 0, room_id):
        print("Room ID already exists.")
        return

    rtype = input("Room Type (Single/Double/Deluxe): ")
    price = input("Price: ")

    write_file(ROOMS_FILE, read_file(ROOMS_FILE) +
               [f"{room_id}|{rtype}|{price}|available\n"])
    write_file(HOUSEKEEPING_FILE, read_file(HOUSEKEEPING_FILE) +
               [f"{room_id}|clean\n"])

    print("Room added.")

def view_rooms(filter_status=None):
    for l in read_file(ROOMS_FILE):
        d = l.strip().split("|")
        if filter_status is None or d[3] == filter_status:
            print(l.strip())

def manager_menu():
    while True:
        print("\n--- Manager ---")
        print("1. Add Room")
        print("2. View All Rooms")
        print("3. View Available Rooms")
        print("0. Back")

        c = input("Choose: ")
        if c == "1": add_room()
        elif c == "2": view_rooms()
        elif c == "3": view_rooms("available")
        elif c == "0": break


# ---------- RECEPTIONIST ----------

def add_guest():
    gid = input("Guest ID (G001): ")
    if id_exists(GUESTS_FILE, 0, gid):
        print("Guest ID exists.")
        return

    name = input("Name: ")
    phone = input("Phone: ")
    write_file(GUESTS_FILE, read_file(GUESTS_FILE) +
               [f"{gid}|{name}|{phone}\n"])
    print("Guest added.")

def walk_in_checkin():
    add_guest()
    book_room("booked")

def book_room(status):
    bid = input("Booking ID (B001): ")
    gid = input("Guest ID: ")

    view_rooms("available")
    rid = input("Choose Room ID: ")
    date = input("Date (YYYY-MM-DD): ")

    rooms = read_file(ROOMS_FILE)
    for i,l in enumerate(rooms):
        d = l.strip().split("|")
        if d[0] == rid and d[3] == "available":
            d[3] = status
            rooms[i] = "|".join(d) + "\n"
            write_file(ROOMS_FILE, rooms)

            write_file(BOOKINGS_FILE, read_file(BOOKINGS_FILE) +
                       [f"{bid}|{gid}|{rid}|{date}|{status}\n"])
            write_file(PAYMENTS_FILE, read_file(PAYMENTS_FILE) +
                       [f"{bid}|{d[2]}|unpaid\n"])
            print("Booking successful.")
            return
    print("Room not available.")

def checkin_reserved():
    for l in read_file(BOOKINGS_FILE):
        if "reserved" in l:
            print(l.strip())

    bid = input("Booking ID to check-in: ")
    bookings = read_file(BOOKINGS_FILE)
    for i,l in enumerate(bookings):
        d = l.strip().split("|")
        if d[0] == bid and d[4] == "reserved":
            d[4] = "booked"
            bookings[i] = "|".join(d) + "\n"
            write_file(BOOKINGS_FILE, bookings)

            rooms = read_file(ROOMS_FILE)
            for j,r in enumerate(rooms):
                rd = r.strip().split("|")
                if rd[0] == d[2]:
                    rd[3] = "booked"
                    rooms[j] = "|".join(rd) + "\n"
            write_file(ROOMS_FILE, rooms)
            print("Checked in.")
            return

def checkout():
    bid = input("Booking ID: ")
    bookings = read_file(BOOKINGS_FILE)
    for i,l in enumerate(bookings):
        d = l.strip().split("|")
        if d[0] == bid and d[4] == "booked":
            d[4] = "checkedout"
            bookings[i] = "|".join(d) + "\n"
            write_file(BOOKINGS_FILE, bookings)

            rooms = read_file(ROOMS_FILE)
            for j,r in enumerate(rooms):
                rd = r.strip().split("|")
                if rd[0] == d[2]:
                    rd[3] = "available"
                    rooms[j] = "|".join(rd) + "\n"
            write_file(ROOMS_FILE, rooms)

            write_file(HOUSEKEEPING_FILE, read_file(HOUSEKEEPING_FILE) +
                       [f"{d[2]}|dirty\n"])
            print("Checked out.")
            return

def cancel_booking():
    bid = input("Booking ID to cancel: ")
    bookings = read_file(BOOKINGS_FILE)
    for i,l in enumerate(bookings):
        if l.startswith(bid):
            bookings[i] = l.replace("reserved", "cancelled")
            write_file(BOOKINGS_FILE, bookings)
            print("Booking cancelled.")
            return

def receptionist_menu():
    while True:
        print("\n--- Receptionist ---")
        print("1. Walk-in Check-in")
        print("2. Book Room (Reserved)")
        print("3. Check-in Reserved Guest")
        print("4. Checkout")
        print("5. Cancel Booking")
        print("6. View Guests")
        print("7. View Rooms")
        print("0. Back")

        c = input("Choose: ")
        if c == "1": walk_in_checkin()
        elif c == "2": book_room("reserved")
        elif c == "3": checkin_reserved()
        elif c == "4": checkout()
        elif c == "5": cancel_booking()
        elif c == "6": print("".join(read_file(GUESTS_FILE)))
        elif c == "7": view_rooms()
        elif c == "0": break


# ---------- ACCOUNTANT ----------

def view_payments():
    for l in read_file(PAYMENTS_FILE):
        print(l.strip())

def mark_paid():
    view_payments()
    bid = input("Booking ID to mark paid: ")
    lines = read_file(PAYMENTS_FILE)
    for i,l in enumerate(lines):
        d = l.strip().split("|")
        if d[0] == bid and d[2] == "unpaid":
            d[2] = "paid"
            lines[i] = "|".join(d) + "\n"
            write_file(PAYMENTS_FILE, lines)
            print("Payment updated.")
            return

def accountant_menu():
    while True:
        print("\n--- Accountant ---")
        print("1. View Payments")
        print("2. Record Payment")
        print("0. Back")

        c = input("Choose: ")
        if c == "1": view_payments()
        elif c == "2": mark_paid()
        elif c == "0": break


# ---------- CLEANER ----------

def cleaner_menu():
    while True:
        print("\n--- Cleaner ---")
        print("Dirty Rooms:")
        dirty = [l for l in read_file(HOUSEKEEPING_FILE) if "dirty" in l]
        for d in dirty: print(d.strip())

        rid = input("Room ID to clean (or 0): ")
        if rid == "0": break

        lines = read_file(HOUSEKEEPING_FILE)
        for i,l in enumerate(lines):
            if l.startswith(rid):
                lines[i] = f"{rid}|clean\n"
                write_file(HOUSEKEEPING_FILE, lines)
                print("Room cleaned.")
                break


# ---------- GUEST ----------

def guest_menu():
    while True:
        print("\n--- Guest ---")
        print("1. View Available Rooms")
        print("2. Book Room")
        print("3. View Booking History")
        print("0. Back")

        c = input("Choose: ")
        if c == "1": view_rooms("available")
        elif c == "2": book_room("reserved")
        elif c == "3":
            gid = input("Enter Guest ID: ")
            for l in read_file(BOOKINGS_FILE):
                if gid in l:
                    print(l.strip())
        elif c == "0": break


# ---------- MAIN ----------

def main_menu():
    while True:
        print("\n=== LOLA HOTEL SYSTEM ===")
        print("1. Manager")
        print("2. Receptionist")
        print("3. Accountant")
        print("4. Cleaner")
        print("5. Guest")
        print("0. Exit")

        c = input("Select role: ")
        if c == "1": manager_menu()
        elif c == "2": receptionist_menu()
        elif c == "3": accountant_menu()
        elif c == "4": cleaner_menu()
        elif c == "5": guest_menu()
        elif c == "0": break

if __name__ == "__main__":
    main_menu()
