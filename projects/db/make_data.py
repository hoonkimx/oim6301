"""Write repeatable, fictional CSV data for Scenario A: BabsonAI Labs."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path


# A seed makes the random choices repeatable when this script runs again.
SEED = 6301
AS_OF = date(2026, 11, 8)
WINDOW_START = date(2025, 11, 9)
# __file__ locates this script, so the output does not depend on the terminal folder.
DATA_DIR = Path(__file__).resolve().parent / "data"


def random_date(rng, first, last):
    """Choose a date, including either endpoint."""
    days = (last - first).days
    return first + timedelta(days=rng.randint(0, days))


def write_csv(filename, columns, rows):
    """Write dictionaries as rows, with the column names on the first line."""
    with (DATA_DIR / filename).open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rng = random.Random(SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # All names, projects, clients, and contact details below are fictional.
    names = [
        ("Alex", "Morgan"), ("Jordan", "Reed"), ("Taylor", "Brooks"),
        ("Casey", "Rivera"), ("Riley", "Patel"), ("Avery", "Chen"),
        ("Sam", "Ellis"), ("Jamie", "Park"), ("Drew", "Bennett"),
        ("Quinn", "Hayes"), ("Cameron", "Lee"), ("Devon", "Shah"),
        ("Emerson", "Price"), ("Finley", "Cole"), ("Harper", "Diaz"),
        ("Jesse", "Wong"), ("Kai", "Ross"), ("Logan", "Singh"),
        ("Micah", "Stone"), ("Noel", "Clark"), ("Parker", "Kim"),
        ("Reese", "Grant"), ("Robin", "Bell"), ("Skyler", "Fox"),
        ("Rowan", "Lane"),
    ]
    people = []
    for person_id, name in enumerate(names, start=1):
        first_name, last_name = name
        if person_id <= 2:
            manager_id = None
            title = "Co-founder"
        elif person_id <= 6:
            manager_id = 1 if person_id % 2 else 2
            title = "Team lead"
        else:
            manager_id = 3 + (person_id % 4)
            title = rng.choice(["AI engineer", "Data analyst", "Product designer"])
        people.append({
            "person_id": person_id,
            "first_name": first_name,
            "last_name": last_name,
            "work_email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "title": title,
            "start_date": date(2024, 1, 1) + timedelta(days=person_id * 19),
            "manager_id": manager_id,
        })

    project_names = [
        "Customer Support Assistant", "Invoice Data Pipeline", "Internal Search",
        "Retail FAQ Assistant", "Sales Reporting Pipeline", "Team Planning Tool",
        "Restaurant Booking Assistant", "Inventory Data Pipeline", "Internal QA Tool",
        "Client Onboarding Assistant", "Delivery Data Pipeline", "Future Staff Portal",
    ]
    projects = []
    categories = ["LLM app", "data pipeline", "internal tool"]
    for project_id, project_name in enumerate(project_names, start=1):
        if project_id <= 7:
            status = "active"
        elif project_id == 8:
            status = "paused"
        elif project_id <= 11:
            status = "done"
        else:
            status = "planned"
        client_name = f"Example Client {project_id}"
        if project_id % 3 == 0:
            client_name = None
        project_start = WINDOW_START + timedelta(days=(project_id - 1) * 10)
        projects.append({
            "project_id": project_id,
            "project_name": project_name,
            "client_name": client_name,
            "category": categories[(project_id - 1) % 3],
            "budget": "3000.00" if project_id == 1 else f"{8000 + project_id * 750}.00",
            "start_date": project_start,
            "status": status,
        })

    assignments = []
    members_by_project = {}
    for project in projects:
        project_id = project["project_id"]
        # Person 1 commits 20 hours to each of projects 1-3: 60 active hours total.
        # Person 25 is kept off projects 1 and 2 for the two deliberate violations.
        if project_id <= 3:
            members = [1, 3 + project_id, 8 + project_id, 13 + project_id]
        else:
            members = rng.sample(range(2, 26), 4)
        members_by_project[project_id] = members
        for person_id in members:
            assignments.append({
                "person_id": person_id,
                "project_id": project_id,
                "project_role": "Project lead" if person_id == members[0] else "Contributor",
                "weekly_hours": 20 if person_id == 1 else rng.choice([4, 8, 12, 16]),
                "joined_date": project["start_date"],
            })

    tasks = []
    descriptions = ["Review requirements", "Build prototype", "Test output quality",
                    "Fix reported issue", "Update documentation", "Review client feedback"]
    for task_id in range(1, 301):
        project_id = (task_id - 1) % 12 + 1
        if task_id == 299:
            project_id = 1
        elif task_id == 300:
            project_id = 2
        project = projects[project_id - 1]
        created_date = random_date(rng, project["start_date"], AS_OF)
        assignee_id = rng.choice(members_by_project[project_id])
        if rng.random() < 0.12:
            assignee_id = None
        if task_id >= 299:
            assignee_id = 25
        assigned_date = created_date if assignee_id is not None else None
        due_date = created_date + timedelta(days=rng.randint(7, 28))
        completed_date = None
        if assignee_id is not None and rng.random() < 0.72:
            completed_date = random_date(rng, created_date, min(due_date, AS_OF))
        # Finished projects contain finished tasks; the planned project has only backlog.
        if project["status"] == "done":
            assignee_id = rng.choice(members_by_project[project_id])
            assigned_date = created_date
            completed_date = random_date(rng, created_date, min(due_date, AS_OF))
        elif project["status"] == "planned":
            assignee_id = None
            assigned_date = None
            completed_date = None
        tasks.append({
            "task_id": task_id,
            "project_id": project_id,
            "description": f"{rng.choice(descriptions)} #{task_id}",
            "created_date": created_date,
            "assignee_id": assignee_id,
            "assigned_date": assigned_date,
            "due_date": due_date,
            "completed_date": completed_date,
        })

    expenses = []
    expense_categories = ["GPU cloud", "data labeling", "software", "travel"]
    for expense_id in range(1, 181):
        project_id = (expense_id - 1) % 11 + 1
        project = projects[project_id - 1]
        category = rng.choices(expense_categories, weights=[5, 2, 4, 1], k=1)[0]
        # Most invoices are modest, with a few larger labeling or travel bills.
        if category == "GPU cloud":
            cents = rng.randint(8000, 80000)
        elif category == "data labeling":
            cents = rng.randint(40000, 180000)
        elif category == "software":
            cents = rng.choice([2900, 4900, 9900, 19900, 39900])
        else:
            cents = rng.randint(30000, 150000)
        expense_date = random_date(rng, project["start_date"], AS_OF)
        # Include the exact first and last days of the selected reporting window.
        if expense_id == 1:
            expense_date = WINDOW_START
        elif expense_id == 180:
            expense_date = AS_OF
        expenses.append({
            "expense_id": expense_id,
            "project_id": project_id,
            "expense_date": expense_date,
            "amount": f"{cents / 100:.2f}",
            "category": category,
            "note": f"Fictional {category.lower()} invoice {expense_id}",
        })

    # Dictionary key order supplies the CSV column order; no rows are skipped.
    for filename, rows in [
        ("people.csv", people), ("projects.csv", projects),
        ("project_assignments.csv", assignments), ("tasks.csv", tasks),
        ("expenses.csv", expenses),
    ]:
        write_csv(filename, list(rows[0].keys()), rows)
        print(f"{filename}: {len(rows)} rows")
    print(f"Window: {WINDOW_START} through {AS_OF}; seed: {SEED}")
    print("Deliberate membership violations: task 299 (person 25, project 1)")
    print("and task 300 (person 25, project 2). No other rules are deliberately broken.")
    print("Project 12 has no expenses. Person 1 has 60 hours across active projects.")


if __name__ == "__main__":
    main()
