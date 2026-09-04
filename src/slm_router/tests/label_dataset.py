import json


INPUT_FILE = "data/capability_dataset.jsonl"
OUTPUT_FILE = "data/capability_labeled.jsonl"


def main():

    records = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    print(f"Loaded {len(records)} records.")

    labeled = []

    for i, item in enumerate(records, start=1):

        print("\n" + "=" * 80)
        print(f"TEST {i}/{len(records)}")
        print(f"ID: {item['id']}")
        print(f"Category: {item['category']}")
        print(f"Difficulty: {item['difficulty']}")
        print(f"\nPROMPT:\n{item['prompt']}")
        print(f"\nRESPONSE:\n{item['response']}")

        while True:
            label = input("\nLabel [P/F]: ").strip().upper()

            if label in ["P", "F"]:
                break

            print("Please enter P for PASS or F for FAIL.")

        item["label"] = "PASS" if label == "P" else "FAIL"

        labeled.append(item)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for record in labeled:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"Saved {len(labeled)} labeled records.")

    print("\n" + "=" * 80)
    print("LABELING COMPLETE")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()