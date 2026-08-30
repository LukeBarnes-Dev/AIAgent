from functions.get_file_content import get_file_content
from config import MAX_CHARS

calculator_test_cases: list[str] = ["lorem.txt", "main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
for item in calculator_test_cases:
    result = get_file_content("calculator", item)
    print(f"{item} length: {len(result)}")
    print(f"{item} truncated: {'truncated' in result}")
    if len(result) < MAX_CHARS:
        print(result)
