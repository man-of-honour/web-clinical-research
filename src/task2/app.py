from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    trials = ["trial_1", "trial_2", "trial_3"]
    meds = ["Плацебо", "Препарат A"]

    errors = []
    success_message = ""

    if request.method == "POST":
        user_id = request.form.get("user_id", "").strip()
        trial = request.form.get("trial", "").strip()
        condition_score = request.form.get("condition_score", "").strip()
        med = request.form.get("med", "").strip()

        if not user_id:
            errors.append("ID пользователя обязателен.")
        else:
            try:
                user_id = int(user_id)
                if user_id < 0:
                    errors.append("ID пользователя не может быть отрицательным.")
            except ValueError:
                errors.append("ID пользователя должен быть целым числом.")

        if trial not in trials:
            errors.append("Выбрано недопустимое исследование.")

        if not condition_score:
            errors.append("Оценка самочувствия обязательна.")
        else:
            try:
                condition_score = int(condition_score)
                if condition_score < 0 or condition_score > 100:
                    errors.append("Оценка самочувствия должна быть от 0 до 100.")
            except ValueError:
                errors.append("Оценка самочувствия должна быть целым числом.")

        if med not in meds:
            errors.append("Выбран недопустимый препарат.")

        if not errors:
            success_message = (
                f"Данные валидны: "
                f"ID={user_id}, "
                f"Исследование={trial}, "
                f"Самочувствие={condition_score}, "
                f"Препарат={med}"
            )

        return render_template(
            "index.html",
            errors=errors,
            success_message=success_message,
            form_data=request.form
        )

    return render_template(
        "index.html",
        errors=errors,
        success_message=success_message,
        form_data={}
    )


if __name__ == "__main__":
    app.run(debug=True)