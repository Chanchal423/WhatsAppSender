# ================================================================
#   AUTO WHATSAPP MESSAGE SENDER
#   Python | pywhatkit | pandas | tkinter
#   Send scheduled & bulk WhatsApp messages automatically
# ================================================================

import pywhatkit as kit
import pandas as pd
import time
from datetime import datetime

print("="*55)
print("   AUTO WHATSAPP MESSAGE SENDER")
print("="*55)
print()

# ─────────────────────────────────────────
# MENU
# ─────────────────────────────────────────
def show_menu():
    print("\n Choose an option:")
    print("  1. Send a single message now")
    print("  2. Schedule a message for later")
    print("  3. Send bulk messages (from CSV)")
    print("  4. Send a message to a group")
    print("  5. Exit")
    return input("\n Enter choice (1-5): ").strip()


# ─────────────────────────────────────────
# OPTION 1 — SEND SINGLE MESSAGE NOW
# ─────────────────────────────────────────
def send_now():
    print("\n── SEND MESSAGE NOW ──")
    phone   = input("Enter phone number with country code (e.g. +919876543210): ").strip()
    message = input("Enter your message: ").strip()

    if not phone or not message:
        print("❌ Phone and message cannot be empty.")
        return

    now     = datetime.now()
    hour    = now.hour
    minute  = now.minute + 2   # Send 2 minutes from now

    if minute >= 60:
        minute -= 60
        hour   += 1

    print(f"\n⏳ Sending to {phone} at {hour:02d}:{minute:02d}...")
    print("📱 WhatsApp Web will open in your browser.")
    print("   Make sure you are logged into WhatsApp Web!\n")

    try:
        kit.sendwhatmsg(phone, message, hour, minute,
                        wait_time=15, tab_close=True)
        print(f"\n✅ Message sent successfully to {phone}!")
    except Exception as e:
        print(f"❌ Error: {e}")


# ─────────────────────────────────────────
# OPTION 2 — SCHEDULE MESSAGE
# ─────────────────────────────────────────
def schedule_message():
    print("\n── SCHEDULE A MESSAGE ──")
    phone   = input("Enter phone number with country code: ").strip()
    message = input("Enter your message: ").strip()

    print("\nEnter time to send (24-hour format):")
    try:
        hour   = int(input("  Hour   (0-23): "))
        minute = int(input("  Minute (0-59): "))
    except ValueError:
        print("❌ Invalid time entered.")
        return

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        print("❌ Invalid time range.")
        return

    now = datetime.now()
    print(f"\n⏰ Scheduled: {phone} at {hour:02d}:{minute:02d}")
    print("📱 WhatsApp Web will open automatically at that time.")
    print("   Keep this program running!\n")

    try:
        kit.sendwhatmsg(phone, message, hour, minute,
                        wait_time=15, tab_close=True)
        print(f"\n✅ Scheduled message sent to {phone}!")
    except Exception as e:
        print(f"❌ Error: {e}")


# ─────────────────────────────────────────
# OPTION 3 — BULK MESSAGES FROM CSV
# ─────────────────────────────────────────
def send_bulk():
    print("\n── BULK MESSAGE SENDER ──")
    print("📄 CSV file format required:")
    print("   Column 1: phone  (e.g. +919876543210)")
    print("   Column 2: name   (e.g. Rahul)")
    print("   Column 3: message (optional — uses default if empty)\n")

    csv_file = input("Enter CSV filename (e.g. contacts.csv): ").strip()

    try:
        df = pd.read_csv(csv_file)
        print(f"✅ Loaded {len(df)} contacts from {csv_file}")
    except FileNotFoundError:
        print(f"❌ File '{csv_file}' not found!")
        print("   Creating a sample contacts.csv for you...")
        create_sample_csv()
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    default_msg = input("\nEnter default message (leave blank to use CSV column): ").strip()

    now    = datetime.now()
    hour   = now.hour
    minute = now.minute + 2

    print(f"\n⏳ Sending to {len(df)} contacts...")
    print("   WhatsApp Web will open for each message.\n")

    success = 0
    failed  = 0

    for i, row in df.iterrows():
        phone = str(row.get("phone", "")).strip()
        name  = str(row.get("name", "Friend")).strip()
        msg   = default_msg if default_msg else str(row.get("message", "Hello!")).strip()

        # Personalize message
        msg = msg.replace("{name}", name)

        if not phone.startswith("+"):
            print(f"  ⚠️  Skipping {name} — invalid phone: {phone}")
            failed += 1
            continue

        # Adjust time for each message (2 min gap)
        minute += 3
        if minute >= 60:
            minute -= 60
            hour   += 1
        if hour >= 24:
            hour = 0

        print(f"  📤 Sending to {name} ({phone}) at {hour:02d}:{minute:02d}...")
        try:
            kit.sendwhatmsg(phone, msg, hour, minute,
                            wait_time=15, tab_close=True)
            print(f"  ✅ Sent to {name}")
            success += 1
            time.sleep(5)  # Small delay between messages
        except Exception as e:
            print(f"  ❌ Failed for {name}: {e}")
            failed += 1

    print(f"\n── BULK SEND COMPLETE ──")
    print(f"  ✅ Sent:   {success}")
    print(f"  ❌ Failed: {failed}")


# ─────────────────────────────────────────
# OPTION 4 — SEND TO GROUP
# ─────────────────────────────────────────
def send_to_group():
    print("\n── SEND TO WHATSAPP GROUP ──")
    print("📌 How to find Group ID:")
    print("   1. Open WhatsApp Web")
    print("   2. Open the group chat")
    print("   3. Copy the group ID from the URL")
    print("   Example URL: https://web.whatsapp.com/accept?code=ABC123")
    print("   Group ID = 'ABC123XYZ-GROUPID@g.us'\n")

    group_id = input("Enter Group ID: ").strip()
    message  = input("Enter message: ").strip()

    if not group_id or not message:
        print("❌ Group ID and message are required.")
        return

    now    = datetime.now()
    hour   = now.hour
    minute = now.minute + 2
    if minute >= 60:
        minute -= 60
        hour   += 1

    print(f"\n⏳ Sending to group at {hour:02d}:{minute:02d}...")
    try:
        kit.sendwhatmsg_to_group(group_id, message, hour, minute,
                                  wait_time=15, tab_close=True)
        print("✅ Group message sent!")
    except Exception as e:
        print(f"❌ Error: {e}")


# ─────────────────────────────────────────
# CREATE SAMPLE CSV
# ─────────────────────────────────────────
def create_sample_csv():
    sample = pd.DataFrame([
        {"phone": "+919876543210", "name": "Rahul",  "message": "Hello {name}! This is an automated message."},
        {"phone": "+919123456789", "name": "Priya",  "message": "Hi {name}! Hope you are doing well."},
        {"phone": "+919000000001", "name": "Arjun",  "message": "Hey {name}! Just checking in."},
    ])
    sample.to_csv("contacts.csv", index=False)
    print("\n✅ Sample 'contacts.csv' created in your project folder!")
    print("   Edit it with your real phone numbers and messages.")
    print("   Then run option 3 again.\n")
    print(sample.to_string(index=False))


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    print("📱 Make sure WhatsApp Web is open & logged in at:")
    print("   https://web.whatsapp.com\n")

    while True:
        choice = show_menu()

        if   choice == "1": send_now()
        elif choice == "2": schedule_message()
        elif choice == "3": send_bulk()
        elif choice == "4": send_to_group()
        elif choice == "5":
            print("\n👋 Goodbye! Happy Messaging!")
            break
        else:
            print("❌ Invalid choice. Enter 1-5.")


if __name__ == "__main__":
    main()
