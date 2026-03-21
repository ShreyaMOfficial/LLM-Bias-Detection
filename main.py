import csv
from modules.bias_detector import detect_bias

def run_system():

    user_prompt = input("Enter prompt: ").strip().lower()
    found = False

    with open("data/generated_text.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            csv_prompt = row["prompt"].strip().lower()

            if csv_prompt == user_prompt:
                found = True
                text = row["generated_text"]

                result = detect_bias(text)

                print("\n========== RESULT ==========")
                print("Prompt:", row["prompt"])
                print("Generated Text:", text)
                print("Bias Type:", ", ".join(result["bias_types"]))
                print("Severity:", result["severity"])
                print("Bias Score:", result["bias_score"])
                print("Evidence:", result["evidence"])
                print("Reasons:")
                for reason in result["reasons"]:
                    print("-", reason)
                print("============================\n")

                break

    if not found:
        print("Prompt not found in generated_text.csv")


if __name__ == "__main__":
    run_system()