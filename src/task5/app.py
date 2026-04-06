import os
import sqlite3
from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)

DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "clinical_trials.db"))


def get_trials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT trial_id, trial_name, med
        FROM trials
        ORDER BY trial_id
    """)
    rows = cursor.fetchall()

    conn.close()

    trials = []
    for row in rows:
        trials.append({
            "trial_id": row[0],
            "trial_name": row[1],
            "med": row[2]
        })

    return trials

def patient_exists(patient_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM patients WHERE patient_id = ?",
        (patient_id,)
    )
    row = cursor.fetchone()
    conn.close()

    return row is not None

from datetime import date

def save_measurement(patient_id, trial_id, med, condition_score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO measurements (
            patient_id,
            trial_id,
            measurement_date,
            drug,
            condition_score
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            trial_id,
            date.today().isoformat(),
            med,
            condition_score
        )
    )

    conn.commit()
    conn.close()

def get_average_score(trial_id, med):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(condition_score)
        FROM measurements
        WHERE trial_id = ? AND drug = ?
        """,
        (trial_id, med)
    )

    result = cursor.fetchone()
    conn.close()

    if result[0] is None:
        return None

    return result[0]

def get_normal_range(avg_score):
    lower_bound = avg_score * 0.9
    upper_bound = avg_score * 1.1
    return lower_bound, upper_bound

@app.route("/", methods=["GET", "POST"])
def index():
    trials = get_trials()
    errors = []
    success_message = ""

    if request.method == "POST":
        user_id = request.form.get("user_id", "").strip()
        trial_id = request.form.get("trial_id", "").strip()
        condition_score = request.form.get("condition_score", "").strip()
        med = request.form.get("med", "").strip()

        selected_trial = None

        if not user_id:
            errors.append("ID пользователя обязателен.")
        else:
            try:
                user_id = int(user_id)
                if user_id < 0:
                    errors.append("ID пользователя не может быть отрицательным.")
                elif not patient_exists(user_id):
                    errors.append("Пациент с таким ID не найден.")
            except ValueError:
                errors.append("ID пользователя должен быть целым числом.")

        if not trial_id:
            errors.append("Исследование обязательно.")
        else:
            try:
                trial_id = int(trial_id)
                selected_trial = next(
                    (trial for trial in trials if trial["trial_id"] == trial_id),
                    None
                )
                if selected_trial is None:
                    errors.append("Выбрано недопустимое исследование.")
            except ValueError:
                errors.append("Некорректный ID исследования.")

        if not condition_score:
            errors.append("Оценка самочувствия обязательна.")
        else:
            try:
                condition_score = int(condition_score)
                if condition_score < 0 or condition_score > 100:
                    errors.append("Оценка самочувствия должна быть от 0 до 100.")
            except ValueError:
                errors.append("Оценка самочувствия должна быть целым числом.")

        if not med:
            errors.append("Препарат обязателен.")
        elif selected_trial is not None:
            allowed_meds = ["Плацебо", selected_trial["med"]]
            if med not in allowed_meds:
                errors.append(
                    f"Для выбранного исследования допустимы только: "
                    f"{selected_trial['med']} или Плацебо."
                )

        if not errors:
            save_measurement(user_id, trial_id, med, condition_score)

            avg_score = get_average_score(trial_id, med)

            if avg_score is None:
               success_message = (
                    f"Данные сохранены, но не удалось рассчитать среднее значение "
                    f"для препарата {med}."
                )
            else:
                lower_bound, upper_bound = get_normal_range(avg_score)

                if lower_bound <= condition_score <= upper_bound:
                    result_message = "Ваше самочувствие находится в пределах нормы."
                else:
                    result_message = "Ваше самочувствие выходит за пределы нормы."

                success_message = (
                    f"Данные сохранены. "
                    f"Среднее значение для препарата {med} "
                    f"в исследовании {selected_trial['trial_name']}: {avg_score:.2f}. "
                    f"Диапазон нормы: от {lower_bound:.2f} до {upper_bound:.2f}. "
                    f"{result_message}"
                )

        return render_template(
            "index.html",
            trials=trials,
            errors=errors,
            success_message=success_message,
            form_data=request.form
        )

    return render_template(
        "index.html",
        trials=trials,
        errors=errors,
        success_message=success_message,
        form_data={}
    )


if __name__ == "__main__":
    app.run(debug=True)