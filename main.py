import csv
import sys
from pathlib import Path

def sql_escape(value: str) -> str:
    """Escape single quotes for SQL"""
    return value.replace("'", "''")

def format_value(value: str):
    """Convert CSV value to SQL-safe value"""
    if value is None:
        return "NULL"

    value = value.strip()

    if value == "":
        return "NULL"

    upper = value.upper()

    if upper in {"TRUE", "FALSE"}:
        return upper

    # numeric check
    try:
        float(value)
        return value
    except ValueError:
        pass

    # timestamp heuristic
    if ":" in value and "-" in value:
        return f"'{sql_escape(value)}'"

    return f"'{sql_escape(value)}'"

def csv_to_sql(csv_file, table_name, output_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)

        columns = ", ".join(headers)

        values_sql = []
        for row in reader:
            formatted = [format_value(v) for v in row]
            values_sql.append(f"({', '.join(formatted)})")

    insert_sql = f"""INSERT INTO {table_name} ({columns})
VALUES
""" + ",\n".join(values_sql) + ";\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(insert_sql)

    print(f"✅ SQL file generated: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python csv_to_sql.py <input.csv> <schema.table> <output.sql>")
        sys.exit(1)

    csv_file = Path(sys.argv[1])
    table_name = sys.argv[2]
    output_file = Path(sys.argv[3])

    csv_to_sql(csv_file, table_name, output_file)
