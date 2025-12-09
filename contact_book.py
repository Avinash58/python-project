import json
import os


# ---------------------- CONTACT CLASS ----------------------
class Contact:
    """Represents a single contact"""

    def __init__(self, name, phone, email="", address=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    @staticmethod
    def from_dict(data):
        return Contact(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            address=data.get("address", "")
        )


# ---------------------- DECORATOR ----------------------
def autosave(method):
    """Automatically save to file after changing data"""
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self._save_to_file()
        return result
    return wrapper


# ---------------------- CONTACTBOOK CLASS ----------------------
class ContactBook:
    """Manages all contacts + handles file storage"""

    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self._load_from_file()

    def _load_from_file(self):
        if not os.path.exists(self.filename):
            self.contacts = []
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.contacts = [Contact.from_dict(c) for c in data]
        except (json.JSONDecodeError, OSError) as e:
            print(f"[ERROR] Could not load contacts: {e}")
            self.contacts = []

    def _save_to_file(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([c.to_dict() for c in self.contacts], f, indent=4)
        except OSError as e:
            print(f"[ERROR] Could not save contacts: {e}")

    # ---------- CRUD ----------
    @autosave
    def add_contact(self, contact: Contact):
        self.contacts.append(contact)
        print("[INFO] Contact added successfully!")

    @autosave
    def delete_contact(self, phone):
        original_count = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.phone != phone]
        if len(self.contacts) < original_count:
            print("[INFO] Contact deleted.")
        else:
            print("[WARN] No contact found.")

    @autosave
    def update_contact(self, phone, **updates):
        for c in self.contacts:
            if c.phone == phone:
                c.name = updates.get("name", c.name)
                c.phone = updates.get("phone", c.phone)
                c.email = updates.get("email", c.email)
                c.address = updates.get("address", c.address)
                print("[INFO] Contact updated!")
                return
        print("[WARN] No contact found.")

    # ---------- SEARCH & LIST ----------
    def search_contacts(self, query):
        query = query.lower()

        def matches(contact: Contact):   # Nested function
            return (query in contact.name.lower()
                    or query in contact.phone.lower()
                    or query in contact.email.lower())

        return [c for c in self.contacts if matches(c)]

    def list_contacts(self):
        return self.contacts


# ---------------------- HELPER ----------------------
def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.")


# ---------------------- MAIN MENU ----------------------
def run_contact_book():
    book = ContactBook()

    while True:
        print("\n========== CONTACT BOOK ==========")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("==================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = get_non_empty_input("Name: ")
            phone = get_non_empty_input("Phone: ")
            email = input("Email: ")
            address = input("Address: ")
            book.add_contact(Contact(name, phone, email, address))

        elif choice == "2":
            contacts = book.list_contacts()
            if not contacts:
                print("No contacts available.")
            else:
                print("\n--- Contact List ---")
                for i, c in enumerate(contacts, start=1):
                    print(f"{i}. {c.name} | {c.phone} | {c.email} | {c.address}")

        elif choice == "3":
            query = input("Search by name/phone/email: ")
            results = book.search_contacts(query)
            if not results:
                print("No contact found.")
            else:
                print("\n--- Search Results ---")
                for i, c in enumerate(results, start=1):
                    print(f"{i}. {c.name} | {c.phone} | {c.email} | {c.address}")

        elif choice == "4":
            phone = input("Enter contact phone to update: ")
            print("Leave blank to keep current value")
            new_name = input("New name: ")
            new_phone = input("New phone: ")
            new_email = input("New email: ")
            new_address = input("New address: ")

            updates = {}
            if new_name: updates["name"] = new_name
            if new_phone: updates["phone"] = new_phone
            if new_email: updates["email"] = new_email
            if new_address: updates["address"] = new_address

            book.update_contact(phone, **updates)

        elif choice == "5":
            phone = input("Enter phone to delete: ")
            book.delete_contact(phone)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option!")


# ---------------------- RUN PROGRAM ----------------------
if __name__ == "__main__":
    run_contact_book()
