import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1. Load the dataset
data = pd.read_csv("student_performance.csv")

print("STUDENT PERFORMANCE DATA")
print("========================")
print(data)


# 2. Select input columns
features = [
    "StudyHours",
    "Attendance",
    "PreviousMarks",
    "AssignmentMarks",
    "InternalMarks"
]

target = "FinalMarks"


# 3. Calculate the importance of each feature
correlations = data[features + [target]].corr()[target]

print("\nFeature Correlation with Final Marks")
print("====================================")

for feature in features:
    print(feature, ":", round(correlations[feature], 2))


# 4. Create weights based on correlation
weights = np.array([
    abs(correlations["StudyHours"]),
    abs(correlations["Attendance"]),
    abs(correlations["PreviousMarks"]),
    abs(correlations["AssignmentMarks"]),
    abs(correlations["InternalMarks"])
])

# Convert weights so that their total is 1
weights = weights / weights.sum()


print("\nFeature Weights")
print("===============")

for feature, weight in zip(features, weights):
    print(feature, ":", round(weight, 3))


# 5. Get student details
print("\nENTER STUDENT DETAILS")
print("=====================")

study_hours = float(input("Enter study hours: "))
attendance = float(input("Enter attendance percentage: "))
previous_marks = float(input("Enter previous marks: "))
assignment_marks = float(input("Enter assignment marks: "))
internal_marks = float(input("Enter internal marks: "))


# 6. Store the student's values
student_values = np.array([
    study_hours,
    attendance,
    previous_marks,
    assignment_marks,
    internal_marks
])


# 7. Calculate predicted marks
predicted_marks = np.sum(student_values * weights)


# 8. Keep prediction within 0-100
predicted_marks = max(0, min(100, predicted_marks))


# 9. Display prediction
print("\nSTUDENT PERFORMANCE PREDICTION")
print("==============================")
print("Predicted Final Marks:", round(predicted_marks, 2))


# 10. Determine performance level
if predicted_marks >= 80:
    performance = "Excellent"
elif predicted_marks >= 60:
    performance = "Good"
elif predicted_marks >= 40:
    performance = "Average"
else:
    performance = "Needs Improvement"

print("Performance Level:", performance)


# 11. Display recommendation
print("\nRECOMMENDATION")
print("==============")

if study_hours < 4:
    print("Increase study hours.")

if attendance < 75:
    print("Try to improve attendance.")

if assignment_marks < 60:
    print("Focus more on assignments.")

if internal_marks < 60:
    print("Prepare better for internal examinations.")

if study_hours >= 4 and attendance >= 75 and assignment_marks >= 60 and internal_marks >= 60:
    print("Keep up the current performance.")


# 12. Create graph
plt.figure(figsize=(8, 5))

plt.scatter(
    data["StudyHours"],
    data["FinalMarks"],
    label="Existing Students"
)

plt.scatter(
    study_hours,
    predicted_marks,
    marker="*",
    s=200,
    label="Predicted Student"
)

plt.xlabel("Study Hours")
plt.ylabel("Final Marks")
plt.title("Student Performance Prediction")
plt.legend()
plt.grid(True)

plt.show()