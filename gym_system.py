"""Fitness club class booking ledger.

Books members into classes up to a capacity limit, handles cancellations
and exports the rosters to a JSON file.
"""
import glob
import json
from pathlib import Path

# Global state
class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class.

    Returns True when the booking succeeds, and False when the class is
    unknown, the class is full, or the member is already booked.
    """
    if attendance_log is None:
        attendance_log = []
    member_id = str(member_id)
    if class_name not in class_capacity:
        print("Unknown class:", class_name)
        return False
    roster = rosters.setdefault(class_name, [])
    if member_id in roster:
        print(f"{member_id} is already booked into {class_name}")
        return False
    if len(roster) >= class_capacity[class_name]:
        print("Class full:", class_name)
        return False
    roster.append(member_id)
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Remove a member from a class roster, if they are on it."""
    roster = rosters.get(class_name, [])
    member_id = str(member_id)
    if member_id in roster:
        roster.remove(member_id)
    else:
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set the seat limit for a class. Seats must be zero or more."""
    if seats < 0:
        raise ValueError(f"seats must be 0 or more, got {seats}")
    class_capacity[class_name] = seats


def add_members(class_name, count):
    """Book up to `count` walk-in guests (GUEST-0, GUEST-1, ...).

    Guest numbers that are already on the roster are skipped. Stops at
    the first failed booking (class full or unknown) and returns how many
    guests were booked.
    """
    taken = set(rosters.get(class_name, []))
    guest_number = 0
    booked = 0
    for _ in range(count):
        while f"GUEST-{guest_number}" in taken:
            guest_number += 1
        if not book_class(f"GUEST-{guest_number}", class_name):
            break
        guest_number += 1
        booked += 1
    return booked


def export_roster(file="gym_schedule.json"):
    """Write all rosters to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(rosters, handle)


def clear_old_exports(prefix="old_"):
    """Delete JSON files in the current folder starting with prefix."""
    for old_file in Path.cwd().glob(glob.escape(prefix) + "*.json"):
        old_file.unlink()


def show_rosters():
    """Print each class with the members booked into it."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(members))


def ask_walk_in_count():
    """Ask how many walk-in guests to add. Invalid input means none."""
    raw = input("How many walk-in guests for HIIT? (Enter for 1): ") or "1"
    try:
        count = int(raw)
    except ValueError:
        print("Not a whole number, adding no guests.")
        return 0
    if count < 0:
        print("Guest count cannot be negative, adding no guests.")
        return 0
    return count


def main():
    """Run a small demo of the booking ledger."""
    for member in ("M1", "M2", "M3", "M4"):
        book_class(member, "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")
    try:
        set_capacity("Spin", -2)
    except ValueError as error:
        print("Could not set capacity:", error)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    add_members("HIIT", ask_walk_in_count())
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
