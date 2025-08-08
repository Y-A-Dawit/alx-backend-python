import re

with open("sqlite_dump.sql", "r", encoding="utf-8") as f:
    dump = f.read()

dump = re.sub(r"PRAGMA.*;\n", "", dump)
dump = dump.replace("BEGIN TRANSACTION;", "")
dump = dump.replace("COMMIT;", "")

dump = dump.replace("AUTOINCREMENT", "AUTO_INCREMENT")
dump = re.sub(r"INTEGER PRIMARY KEY", "INTEGER PRIMARY KEY AUTO_INCREMENT", dump)
dump = re.sub(r'"([^"]+)"', r'`\1`', dump)

dump = dump.replace("1;", "1;").replace("0;", "0;")

with open("mysql_ready_dump.sql", "w", encoding="utf-8") as f:
    f.write(dump)

print("✅ Converted to MySQL format: mysql_ready_dump.sql")
# convert_sqlite_to_mysql.py
import re

with open("sqlite_dump.sql", "r", encoding="utf-8") as f:
    dump = f.read()

# Remove SQLite-specific commands
dump = re.sub(r"PRAGMA.*;\n", "", dump)
dump = dump.replace("BEGIN TRANSACTION;", "")
dump = dump.replace("COMMIT;", "")

# Convert AUTOINCREMENT syntax
dump = dump.replace("AUTOINCREMENT", "AUTO_INCREMENT")

# Convert INTEGER PRIMARY KEY to MySQL style
dump = re.sub(r"INTEGER PRIMARY KEY", "INTEGER PRIMARY KEY AUTO_INCREMENT", dump)

# Replace double quotes with backticks for table/column names
dump = re.sub(r'"([^"]+)"', r'`\1`', dump)

# Optional: adjust boolean values
dump = dump.replace("1;", "1;").replace("0;", "0;")

# Save to new file
with open("mysql_ready_dump.sql", "w", encoding="utf-8") as f:
    f.write(dump)

print("✅ Converted to MySQL format: mysql_ready_dump.sql")
