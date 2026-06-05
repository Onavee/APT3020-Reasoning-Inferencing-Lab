import json
# student information
class Student:
    def __init__(self, gpa, attendance, disciplinary,
                 prerequisites, fees):

        self.gpa = gpa
        self.attendance = attendance
        self.disciplinary = disciplinary
        self.prerequisites = prerequisites
        self.fees = fees

# loading the rules from a json file
def load_rules(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    return data["rules"]
# Applying the rules to the student information
def check_condition(student_value, condition):

    if isinstance(student_value, (int, float)):

        if condition.startswith(">="):
            return student_value >= float(condition[2:])

        elif condition.startswith("<="):
            return student_value <= float(condition[2:])

        elif condition.startswith(">"):
            return student_value > float(condition[1:])

        elif condition.startswith("<"):
            return student_value < float(condition[1:])

    return str(student_value) == condition
# Forward Chaining
class ReasoningEngine:

    def __init__(self, rules):
        self.rules = rules

    def infer(self, student):

        results = []

        for rule in self.rules:

            if self.evaluate_rule(student, rule["if"]):

                results.append({
                    "rule": rule["name"],
                    "conclusion": rule["then"]
                })

        return results

    def evaluate_rule(self, student, conditions):

        for key, condition in conditions.items():

            student_value = getattr(student, key)

            if not check_condition(student_value, condition):
                return False

        return True
# Backward Chaining
class BackwardChainingEngine:

    def __init__(self, rules):
        self.rules = rules

    def check_goal(self, student, goal):

        for rule in self.rules:

            if rule["then"] == goal:

                if self.evaluate_rule(student, rule["if"]):

                    return {
                        "goal": goal,
                        "result": True,
                        "rule": rule["name"],
                        "message": "Goal is satisfied"
                    }

                return {
                    "goal": goal,
                    "result": False,
                    "rule": rule["name"],
                    "message": "Goal NOT satisfied"
                }

        return {
            "goal": goal,
            "result": False,
            "rule": None,
            "message": "Goal not found"
        }


    def evaluate_rule(self, student, conditions):

        for key, condition in conditions.items():

            student_value = getattr(student, key)

            if not check_condition(student_value, condition):
                return False

        return True

# Running the reasoning engine
def run_case(engine, student, label):

    
    print(f"\nSTUDENT PROFILE: {label}")
    

    print("\nFACTS:")
    print(f"GPA: {student.gpa}")
    print(f"Attendance: {student.attendance}")
    print(f"Disciplinary: {student.disciplinary}")
    print(f"Prerequisites: {student.prerequisites}")
    print(f"Fees: {student.fees}")

    results = engine.infer(student)

    print("\nRULES TRIGGERED:")

    if results:
        for r in results:
            print(f" {r['rule']}")
    else:
        print("None")

    print("\nCONCLUSIONS:")

    if results:
        for r in results:
            print( r["conclusion"])
    else:
        print("None")  


if __name__ == "__main__":

    rules = load_rules("knowledgebase.json")

    forward_engine = ReasoningEngine(rules)
    backward_engine = BackwardChainingEngine(rules)

    student1 = Student(3.8, 90, "No", "Completed", "No")
    student2 = Student(3.2, 75, "No", "Completed", "No")
    student3 = Student(2.4, 60, "Yes", "Not Completed", "Yes")

    # Forward chaining demo
    run_case(forward_engine, student1, "High Performer")
    run_case(forward_engine, student2, "Average Student")
    run_case(forward_engine, student3, "At Risk Student")

    # Backward chaining demo
print("\nBACKWARD CHAINING DEMO")
goal = "Eligible for Scholarship"
goal_results = backward_engine.check_goal(student1, goal)
print("\nGOAL:", goal_results["goal"])
print("RULE:", goal_results["rule"])
print("RESULT:", goal_results["result"])
print("MESSAGE:", goal_results["message"])