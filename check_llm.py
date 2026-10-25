from config import create_client
from analyzer import analyze_file

client = create_client()

results = analyze_file("test_code.py", client)

for r in results:
    if r["error"]:
        print(f"[{r['error']}]")
        continue

    print(f"=== {r['function']} ===")
    print(f"Vulnerable: {r['vulnerable']}")
    print(f"Type: {r['type']}")
    print(f"Confidence: {r['confidence']}")
    print(f"Reason: {r['reason']}")
    print()
