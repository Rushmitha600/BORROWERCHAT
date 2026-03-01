import json
import os
import csv

class FAQData:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_folder = os.path.join(BASE_DIR, "data")

        self.faqs = []

        # ==============================
        # 🔹 Load JSON FAQs
        # ==============================
        json_path = os.path.join(data_folder, "faq_data.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    if isinstance(json_data, list):
                        self.faqs.extend(json_data)
                print("✅ JSON FAQs Loaded")
            except Exception as e:
                print("❌ JSON Load Error:", e)

        # ==============================
        # 🔹 Load CSV FAQs
        # ==============================
        csv_path = os.path.join(data_folder, "faq_data.csv")
        if os.path.exists(csv_path):
            try:
                with open(csv_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 2 and row[0] and row[1]:
                            self.faqs.append({
                                "question": row[0].strip(),
                                "answer": row[1].strip(),
                                "emoji": "💬",
                                "category": "loan",
                                "tags": []
                            })
                print("✅ CSV FAQs Loaded")
            except Exception as e:
                print("❌ CSV Load Error:", e)

        print(f"📚 Total FAQs Loaded: {len(self.faqs)}")

    def get_all_faqs(self):
        return self.faqs
