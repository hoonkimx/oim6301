"""Part A: build and check the BabsonAI Labs database."""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import csv
    import duckdb
    import marimo as mo
    import polars as pl
    import altair as alt
    return alt, csv, duckdb, mo, pl


@app.cell
def _(duckdb, mo):
    # notebook_dir keeps the database beside this notebook.
    database = mo.notebook_dir() / "database.duckdb"
    as_of = "2026-11-08"

    def ask(sql):
        # with closes the connection; .pl() returns a Polars table.
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return as_of, ask, database


@app.cell(hide_code=True)
def _(as_of, mo):
    mo.md(f"""
    # BabsonAI Labs — Part A

    Reporting date (`as_of`): **{as_of}**.
    Generated activity covers **2025-11-09 through 2026-11-08**.
    All names, clients, contact details, and transactions are fictional.

    Run `uv run python projects/db/make_data.py` first to create the CSV files.
    This notebook rebuilds the database from those CSV files every time it runs.
    Dates are read as DATE, IDs and hours as INTEGER, and money as DECIMAL(12,2).
    No CSV rows are skipped or removed.

    # 1. The Tables

    The CREATE TABLE statements below follow the README diagram.
    A primary key identifies a row; a foreign key points to a valid row in another
    table. NOT NULL requires a value, CHECK enforces a rule, UNIQUE prevents a
    duplicate, and DEFAULT supplies a value when an insert omits that column.
    """)
    return


@app.cell
def _():
    table_definitions = [
        """
        CREATE TABLE people (
            person_id INTEGER PRIMARY KEY,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            work_email VARCHAR NOT NULL UNIQUE,
            title VARCHAR NOT NULL,
            start_date DATE NOT NULL,
            manager_id INTEGER REFERENCES people(person_id),
            CHECK (manager_id IS NULL OR manager_id <> person_id)
        )
        """,
        """
        CREATE TABLE projects (
            project_id INTEGER PRIMARY KEY,
            project_name VARCHAR NOT NULL,
            client_name VARCHAR,
            category VARCHAR NOT NULL
                CHECK (category IN ('LLM app', 'data pipeline', 'internal tool')),
            budget DECIMAL(12,2) NOT NULL CHECK (budget > 0),
            start_date DATE NOT NULL,
            status VARCHAR NOT NULL DEFAULT 'planned'
                CHECK (status IN ('planned', 'active', 'paused', 'done'))
        )
        """,
        """
        CREATE TABLE project_assignments (
            person_id INTEGER NOT NULL REFERENCES people(person_id),
            project_id INTEGER NOT NULL REFERENCES projects(project_id),
            project_role VARCHAR NOT NULL,
            weekly_hours INTEGER NOT NULL CHECK (weekly_hours BETWEEN 1 AND 40),
            joined_date DATE NOT NULL,
            PRIMARY KEY (person_id, project_id)
        )
        """,
        """
        CREATE TABLE tasks (
            task_id INTEGER PRIMARY KEY,
            project_id INTEGER NOT NULL REFERENCES projects(project_id),
            description VARCHAR NOT NULL,
            created_date DATE NOT NULL,
            assignee_id INTEGER REFERENCES people(person_id),
            assigned_date DATE,
            due_date DATE NOT NULL,
            completed_date DATE,
            CHECK (due_date >= created_date),
            CHECK (completed_date IS NULL OR completed_date >= created_date),
            CHECK (
                (assignee_id IS NULL AND assigned_date IS NULL)
                OR (assignee_id IS NOT NULL AND assigned_date IS NOT NULL)
            ),
            CHECK (assigned_date IS NULL OR assigned_date >= created_date),
            CHECK (completed_date IS NULL OR assigned_date IS NULL
                   OR completed_date >= assigned_date)
        )
        """,
        """
        CREATE TABLE expenses (
            expense_id INTEGER PRIMARY KEY,
            project_id INTEGER NOT NULL REFERENCES projects(project_id),
            expense_date DATE NOT NULL,
            amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
            category VARCHAR NOT NULL
                CHECK (category IN ('GPU cloud', 'data labeling', 'software', 'travel')),
            note VARCHAR NOT NULL
        )
        """,
    ]
    return (table_definitions,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 2. The Data

    `make_data.py` uses fixed seed **6301** and writes five CSV files in `data/`.
    Expected counts: **25 people, 12 projects, 48 project assignments, 300 tasks,
    and 180 expenses**. Two founders have no manager. Projects 3, 6, 9, and 12
    are internal and have no client. Some tasks are unassigned or unfinished.
    Project 12 has no expenses and is still planned.

    Exactly two tasks intentionally break the rule that an assignee must work
    on the task's project:

    - **Task 299:** person 25 is assigned to a task on project 1, but is not on project 1.
    - **Task 300:** person 25 is assigned to a task on project 2, but is not on project 2.

    The foreign keys ensure both IDs exist individually. They do not check the
    person–project pairing; Part B will check that pairing with a query.
    Assignment dates still follow employee start dates in both deliberate errors.
    Every other scenario rule is followed.

    In the build cell, `_con` is a connection used only inside the `with` block.
    People load one row at a time, managers first, because their manager foreign
    key points back to the people table. The other files load into tables whose
    referenced rows already exist. Empty CSV fields become SQL NULL values.
    """)
    return


@app.cell
def _(csv, database, duckdb, table_definitions):
    # Check all inputs before deleting the database, so missing CSVs do not erase it.
    _data_dir = database.parent / "data"
    for _table in ["people", "projects", "project_assignments", "tasks", "expenses"]:
        if not (_data_dir / f"{_table}.csv").is_file():
            raise FileNotFoundError("Run make_data.py before running build.py.")

    # Delete the old file before opening a new database, as the assignment requires.
    database.unlink(missing_ok=True)
    with duckdb.connect(database) as _con:
        for _statement in table_definitions:
            _con.execute(_statement)

        with (_data_dir / "people.csv").open(newline="", encoding="utf-8") as _file:
            for _row in csv.DictReader(_file):
                _manager = None
                if _row["manager_id"]:
                    _manager = int(_row["manager_id"])
                # ? placeholders pass data separately from SQL text.
                _con.execute(
                    "INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [int(_row["person_id"]), _row["first_name"], _row["last_name"],
                     _row["work_email"], _row["title"], _row["start_date"], _manager],
                )

        for _table in ["projects", "project_assignments", "tasks", "expenses"]:
            # All CSV fields start as text; insertion converts them to the declared types.
            _con.execute(
                f"INSERT INTO {_table} SELECT * FROM read_csv(?, header=true, all_varchar=true)",
                [str(_data_dir / f"{_table}.csv")],
            )

        # Aggregate expenses first, so joining them never duplicates a project's budget.
        _con.execute("""
            CREATE VIEW weekly_project_spending AS
            SELECT p.project_id, p.project_name, p.status, p.budget,
                   COALESCE(e.total_spent, 0) AS total_spent,
                   p.budget - COALESCE(e.total_spent, 0) AS remaining_budget,
                   ROUND(100.0 * COALESCE(e.total_spent, 0) / p.budget, 2) AS percent_spent
            FROM projects AS p
            LEFT JOIN (
                SELECT project_id, SUM(amount) AS total_spent
                FROM expenses
                GROUP BY project_id
            ) AS e ON p.project_id = e.project_id
        """)

    # This returned value makes the later cells wait until the build finishes.
    build_complete = True
    print("Built database.duckdb from all 5 CSV files; build connection closed.")
    print("Converted IDs/hours/dates/money for 565 rows; skipped 0 rows.")
    return (build_complete,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 3. A Look at the Data

    This reads `expenses.csv` directly with Polars and charts invoice amounts.
    `cast(pl.Float64)` converts all 180 monetary values to numbers for plotting;
    it does not change the database's exact DECIMAL money values.
    `bin=True` groups nearby amounts into histogram bars, and `count()` counts invoices.
    """)
    return


@app.cell
def _(alt, database, pl):
    expense_csv = pl.read_csv(database.parent / "data" / "expenses.csv", infer_schema=False)
    expense_csv = expense_csv.with_columns(pl.col("amount").cast(pl.Float64))
    expense_chart = alt.Chart(expense_csv).mark_bar().encode(
        x=alt.X("amount:Q", bin=alt.Bin(maxbins=20), title="Expense amount ($)"),
        y=alt.Y("count():Q", title="Number of expenses"),
        tooltip=[alt.Tooltip("count():Q", title="Expenses")],
    ).properties(title="Distribution of fictional project expenses")
    expense_chart
    return expense_chart, expense_csv


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    The many smaller invoices and fewer large bills are plausible for a small AI
    startup because recurring software charges are usually smaller than labeling
    and travel bills; the generator uses different amount ranges by category
    rather than giving every expense the same uniform price distribution.

    # 4. Row Counts
    """)
    return


@app.cell
def _(ask, build_complete):
    row_counts = ask("""
        SELECT 'people' AS table_name, COUNT(*) AS rows FROM people
        UNION ALL SELECT 'projects', COUNT(*) FROM projects
        UNION ALL SELECT 'project_assignments', COUNT(*) FROM project_assignments
        UNION ALL SELECT 'tasks', COUNT(*) FROM tasks
        UNION ALL SELECT 'expenses', COUNT(*) FROM expenses
    """)
    print(row_counts)
    row_counts
    return (row_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 5. A Row It Refuses

    Expected: an expense of **-1.00** is rejected by the `amount > 0` constraint.
    This uses a short write connection because `ask()` opens read-only connections.
    `try` / `except` displays the expected rejection without stopping the notebook.
    """)
    return


@app.cell
def _(build_complete, database, duckdb, mo):
    refusal_message = ""
    with duckdb.connect(database) as _con:
        try:
            _con.execute("""
                INSERT INTO expenses VALUES
                (999999, 1, DATE '2026-11-08', -1.00, 'software', 'Invalid test row')
            """)
        except duckdb.ConstraintException as _error:
            refusal_message = str(_error)
        else:
            # If the constraint is accidentally removed, do not leave the test row behind.
            _con.execute("DELETE FROM expenses WHERE expense_id = 999999")
            raise AssertionError("The database accepted a negative expense.")
    print(refusal_message)
    mo.md(f"Expected rejection received:\n\n```text\n{refusal_message}\n```")
    return (refusal_message,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 6. Answers You Already Knew

    These expectations come from the generator and are written before the queries:

    1. **25 employees**, because the script defines 25 fictional names.
    2. **2 employees without managers**, because only people 1 and 2 are founders.
    3. **0 expenses for project 12**, because expense project IDs cycle only through 1–11.

    Each query runs below. `assert` stops with an error if an actual value differs
    from the expected value. `.item()` extracts a single value from a one-cell table.
    """)
    return


@app.cell
def _(ask, build_complete, pl):
    known_checks = [
        ("Employees", "SELECT COUNT(*) FROM people", 25),
        ("Employees without managers", "SELECT COUNT(*) FROM people WHERE manager_id IS NULL", 2),
        ("Project 12 expenses", "SELECT COUNT(*) FROM expenses WHERE project_id = 12", 0),
    ]
    _comparisons = []
    for _label, _query, _expected in known_checks:
        _actual = ask(_query).item()
        assert _actual == _expected, f"{_label}: expected {_expected}, got {_actual}"
        _comparisons.append({"check": _label, "query": _query,
                             "expected": _expected, "actual": _actual,
                             "agrees": _actual == _expected})
    known_answers = pl.DataFrame(_comparisons)
    print(known_answers)
    known_answers
    return known_answers, known_checks


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # 7. A View

    Weekly question: **How much has each project spent, and how much budget remains?**
    `weekly_project_spending` is created in the build cell and can be queried by name.
    A view saves a query, rather than a separate copy of its results, so it reads the
    current underlying records. Part B's budget question will use this view.

    `LEFT JOIN` keeps projects without expenses, and `COALESCE(..., 0)` shows their
    spending as zero instead of NULL. The percent is spending divided by budget,
    multiplied by 100.
    """)
    return


@app.cell
def _(ask, build_complete):
    spending_view = ask("SELECT * FROM weekly_project_spending ORDER BY project_id")
    spending_view
    return (spending_view,)


if __name__ == "__main__":
    app.run()
