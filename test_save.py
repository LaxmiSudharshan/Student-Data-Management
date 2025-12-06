import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "students.csv")

print(f"File path: {FILE_PATH}")
print(f"Directory: {BASE_DIR}")
print(f"File exists before: {os.path.exists(FILE_PATH)}")

# Test save
test_data = [["John", "10A", "A", "95"], ["Jane", "10B", "B", "85"]]

try:
    with open(FILE_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(test_data)
    print(f"✓ Successfully saved {len(test_data)} records")
    print(f"File exists after: {os.path.exists(FILE_PATH)}")
    
    # Read back
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"File content:\n{content}")
    
except Exception as e:
    print(f"✗ Error: {e}")
