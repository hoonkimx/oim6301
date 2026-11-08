def compute_bmi(weight, height):
    """Compute the Body Mass Index (BMI) given weight and height."""
    bmi = weight / (height ** 2)
    return bmi


def classify_bmi(bmi):
    """Classify the BMI into categories."""
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"

    return category


def main():
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in meters: "))

    bmi_value = compute_bmi(weight, height)
    result = classify_bmi(bmi_value)

    print(f"Your BMI is {bmi_value:.2f}, and your category is {result}.")


main()