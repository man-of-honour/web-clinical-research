# Clinical Research Web Application

A lightweight **Flask** web application for entering, validating, storing, and analyzing clinical trial data.

This project was built as part of a Python and database practice assignment, then refined into a portfolio-ready project for GitHub.

---

## Overview

The application allows a user to:

- enter a **patient ID**
- select a **clinical trial** from the database
- enter a **condition score** on a scale from `0` to `100`
- specify a **drug**
- validate the submitted data
- save the record into the database
- calculate the average `condition_score` for the selected drug within the selected trial
- determine whether the submitted condition score falls within the normal range

The final version of the application is implemented in **Flask** and works with an existing **SQLite** database from the previous project.

---

## Features

- Simple web interface built with **Flask** and **HTML**
- Server-side validation of all user input
- Dynamic loading of trials from the database
- Validation of drug choice for the selected trial
- Storage of new measurements in the database
- Automatic insertion of the current date for each measurement
- Calculation of the average condition score for the selected drug in the selected trial
- Calculation of a normal range defined as **±10%** of the average score
- Feedback to the user indicating whether the patient's condition is within the normal range

---

## Tech Stack

- **Python**
- **Flask**
- **SQLite**

---

## Project Structure

```text
.
├── add_med.sql
├── clinical_trials.db
├── src
│   ├── task1
│   │   ├── app.py
│   │   └── templates
│   │       └── index.html
│   ├── task2
│   │   ├── app.py
│   │   └── templates
│   │       └── index.html
│   ├── task3
│   │   ├── app.py
│   │   └── templates
│   │       └── index.html
│   ├── task4
│   │   ├── app.py
│   │   └── templates
│   │       └── index.html
│   └── task5
│       ├── app.py
│       └── templates
│           └── index.html
└── README.md
```

---

## File Description

- `add_med.sql` — SQL script for updating the database schema and filling the `med` field
- `clinical_trials.db` — SQLite database used by the application
- `src/task1` — basic interface and validation
- `src/task2` — database modification step
- `src/task3` — dynamic loading of trial data from the database
- `src/task4` — saving validated user input
- `src/task5` — final working version with analysis and user feedback

The final application is launched from `src/task5/app.py`.

---

## Development Stages

### Task 1 — Interface and Basic Validation

At the first stage, the application provides a basic HTML form that allows the user to:

- enter `user_id`
- choose a clinical trial
- enter `condition_score`
- specify a drug

Validation rules:

- patient ID must be a non-negative integer
- condition score must be between 0 and 100
- drug field must not be empty
- a trial must be selected

### Task 2 — Database Update

At this stage, the database schema is extended.

A new column is added to the `trials` table:

```sql
ALTER TABLE trials ADD COLUMN med VARCHAR(100);
```

After that, the field is populated with actual drug names for the existing trials.

The SQL script is stored in:

- `add_med.sql`

### Task 3 — Loading Data from the Database

The list of available trials is no longer hardcoded.

Instead, the application retrieves the following fields directly from the `trials` table:

- `trial_id`
- `trial_name`
- `med`

Additional validation is implemented:

- for a selected trial, the drug must be either:
  - `Placebo`
  - or the `med` assigned to that trial

### Task 4 — Saving Data

After successful validation, the application:

- checks whether the patient exists in the `patients` table
- saves a new record into the `measurements` table

Saved fields:

- `patient_id`
- `trial_id`
- `measurement_date`
- `drug`
- `condition_score`

The measurement date is inserted automatically as the current date.

### Task 5 — Analysis and User Feedback

After saving the record, the application:

- calculates the average `condition_score` for the selected drug within the selected trial
- calculates the normal range as ±10% of the average
- compares the submitted score with this range
- informs the user whether the condition score is within the normal range

---

## Database Schema

The project uses the SQLite database `clinical_trials.db`.

### `patients`

| Column | Description |
|---|---|
| `patient_id` | Unique patient identifier |
| `name` | Patient name |
| `age` | Patient age |
| `gender` | Patient gender |
| `condition` | Patient condition |

### `trials`

| Column | Description |
|---|---|
| `trial_id` | Unique trial identifier |
| `trial_name` | Trial name |
| `start_date` | Trial start date |
| `end_date` | Trial end date |
| `med` | Drug used in the trial |

### `measurements`

| Column | Description |
|---|---|
| `measurement_id` | Unique measurement identifier |
| `patient_id` | ID of the patient |
| `trial_id` | ID of the trial |
| `measurement_date` | Date of the measurement |
| `drug` | Drug specified by the user |
| `condition_score` | Self-reported condition score |

---

## How to Run

1. Install Flask:

```bash
python -m pip install flask
```

2. Make sure the database file is located in the project root.

Required file:

- `clinical_trials.db`

3. Run the final version of the application:

```bash
python src/task5/app.py
```

4. Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

## Example Workflow

- The user enters a patient ID.
- The user selects a clinical trial.
- The user enters a condition score.
- The user specifies a drug.
- The application validates the submitted data.

If the data is valid:

- the record is saved to the database
- the average score for the selected drug is calculated
- the normal range is calculated
- the result of the analysis is displayed to the user

---

## Implemented Functionality

- web interface built with Flask
- HTML form for user input
- validation of patient ID, trial selection, condition score, and drug
- dynamic loading of trials from the database
- validation of drug-trial consistency
- patient existence check before saving
- saving new records into the `measurements` table
- automatic insertion of the current date
- calculation of average `condition_score`
- calculation of a normal range based on ±10%
- user feedback indicating whether the submitted score is within the normal range

---

## Notes

This project was originally created as an educational assignment focused on:

- Python web development
- working with relational databases
- SQL queries
- validation and processing of user input
- simple analytics based on stored clinical trial data

For portfolio purposes, the project demonstrates:

- backend logic in Flask
- interaction with SQLite
- form handling and validation
- database read/write operations
- basic analytical processing in a medical-data context

---

## Author

Created by Filipp Ananishnev as part of a Python and database practice project.

The project is presented in this repository as a portfolio piece focused on the intersection of medicine and IT.