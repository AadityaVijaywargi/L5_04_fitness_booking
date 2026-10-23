# Issues found in `gym_system.py`

Line numbers refer to the **original** file (commit `a2af42b`). Ordered by severity, highest first. "Tool" shows what reported the issue; "none" means it only showed up when running the program and reading the output.

Baseline: Pylint **6.60/10** (16 messages), Bandit **1 High**, Flake8 **10** findings.
After fixes: Pylint **10.00/10**, Bandit **0 issues**, Flake8 **0 issues**.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from input (Bandit B605, CWE-78, **High**) | Security | 36 | `os.system("rm -f " + prefix + "*.json")` passes a caller-controlled string to a shell, so a prefix like `x; rm -rf ~` would run arbitrary commands. | Removed `os.system`. Delete files with `Path.cwd().glob(glob.escape(prefix) + "*.json")` and `unlink()`. No shell is involved. Dropped the unused `os` import. |
| Off-by-one capacity check (tool: none) | Bug | 11 | `len(roster) > capacity` lets one extra person in. Running the program booked **4 members into Yoga (capacity 3)** and 2 into HIIT (capacity 2) before the guest was even added. | Changed the check to `len(roster) >= class_capacity[class_name]`. Yoga now stops at 3. |
| Unknown classes accepted (tool: none) | Bug | 9-11 | `class_capacity.get(class_name, 0)` gives capacity 0, but with the off-by-one above the first person still got in, so "Pilates" was booked and a roster was created for it. | `book_class` now rejects any class not in `class_capacity` ("Unknown class") and only creates a roster for known classes. |
| Mutable default argument (Pylint W0102) | Bug | 8 | `attendance_log=[]` is created once and shared by every call that omits it, so entries pile up across unrelated bookings. | Default is `None`; a fresh list is created inside the function when none is passed. |
| Negative capacity accepted (tool: none) | Bug | 24-25, 49 | `set_capacity("Spin", -2)` silently stored -2, which made Spin permanently "full". | `set_capacity` raises `ValueError` when seats < 0; `main` catches it and prints a message. |
| Unvalidated `int(input())` (tool: none) | Bug (crash) | 52-53 | Typing `abc` or `-1` for walk-in guests crashed with a traceback or behaved oddly. | New `ask_walk_in_count()` catches `ValueError`, rejects negatives, and returns 0 with a message. |
| Bare `except` (Pylint W0702, Flake8 E722) | Bug | 21-22 | `except:` hides every error, including typos and `KeyboardInterrupt`, and prints "Nothing to cancel" for all of them. | Replaced the try/except with an explicit membership check using `rosters.get(class_name, [])`. (An intermediate commit narrowed it to `(KeyError, ValueError)`.) |
| Unclosed file, no encoding (Pylint R1732, W1514) | Resource | 32-33 | `open(...)` is never closed, so data may not be flushed, and the encoding depends on the platform. | `with open(file, "w", encoding="utf-8") as handle:` |
| Duplicate guest IDs / double booking (tool: none) | Bug | 28-29 | `addMembers` always starts at `GUEST-0`, so a second call reuses IDs, and nothing stops the same member joining a class twice. | `book_class` rejects a member already on the roster. `add_members` skips guest numbers already taken and stops at the first failed booking. |
| Mixed ID types (tool: none) | Data consistency | 47 | `book_class(55, "HIIT")` stores an `int` among string IDs, so the JSON export mixes types and `.remove("55")` would not match `55`. | IDs are normalised with `str(member_id)` on booking and cancellation. |
| `main()` runs on import (tool: none) | Design | 58 | Importing the module (for tests, say) immediately runs the demo, asks for input and writes files. | Wrapped in `if __name__ == "__main__":`. |
| Function name not snake_case (Pylint C0103) | Style | 27 | `addMembers` breaks PEP 8 naming. | Renamed to `add_members` (only `main` called it). |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 8, 18, 24, 27, 31, 35, 38, 42 | No module docstring and no function docstrings (9 messages). | Added a module docstring and a one-line or short docstring to every function. |
| `%` string formatting (Pylint C0209) | Style | 15 | `"%s -> %s" % (...)` where an f-string is clearer. | `f"{member_id} -> {class_name}"` |
| Iterating dict by key then indexing (Pylint C0206) | Style | 39 | `for c in rosters:` then `rosters[c]`. | `for class_name, members in rosters.items():` (also gave `c` a readable name). |
| Missing blank lines (Flake8 E302 x8, E305 x1) | Style | 8, 18, 24, 27, 31, 35, 38, 42, 58 | PEP 8 wants two blank lines around top-level definitions. | Added the blank lines. |
