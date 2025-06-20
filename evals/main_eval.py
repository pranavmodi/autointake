from scenario_1_new_intake import simulate_new_intake
from scenario_2_all_docs_complete import simulate_intake_all_docs_complete
from scenario_3_non_pi import simulate_intake_non_pi
from scenario_4_escalation import simulate_intake_escalation

def main():
    """
    Presents a menu to the user to select and run an intake simulation scenario.
    """
    scenarios = {
        "1": ("New Intake (Standard)", simulate_new_intake),
        "2": ("Intake - All Documents Complete", simulate_intake_all_docs_complete),
        "3": ("Intake - Non-PI Case", simulate_intake_non_pi),
        "4": ("Intake - Escalation", simulate_intake_escalation),
    }

    print("Select an intake scenario to simulate:")
    for key, (description, _) in scenarios.items():
        print(f"  {key}. {description}")

    choice = input("Enter the number of the scenario you want to run: ")

    if choice in scenarios:
        description, func = scenarios[choice]
        print(f"\nRunning scenario: '{description}'...")
        func()
    else:
        print("Invalid choice. Please run the script again and select a valid number.")

if __name__ == "__main__":
    main() 