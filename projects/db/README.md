# 1. The Scenario

Scenario A: BabsonAI Labs.

BabsonAI Labs is a startup with about 25 employees that currently tracks
people, projects, staffing, tasks, and expenses in spreadsheets and chat
threads. Its founders want to understand project spending, unfinished
work, and employee workloads.

This database will support the eight business questions listed under
Scenario A in the assignment.

# 2. The ERD

```mermaid
erDiagram
    PEOPLE {
        int person_id PK
        string first_name
        string last_name
        string work_email UK
        string title
        date start_date
        int manager_id FK
    }

    PROJECTS {
        int project_id PK
        string project_name
        string client_name
        string category
        decimal budget
        date start_date
        string status
    }

    PROJECT_ASSIGNMENTS {
        int person_id PK, FK
        int project_id PK, FK
        string project_role
        int weekly_hours
        date joined_date
    }

    TASKS {
        int task_id PK
        int project_id FK
        string description
        date created_date
        int assignee_id FK
        date assigned_date
        date due_date
        date completed_date
    }

    EXPENSES {
        int expense_id PK
        int project_id FK
        date expense_date
        decimal amount
        string category
        string note
    }

    PEOPLE o|--o{ PEOPLE : manages
    PEOPLE ||--o{ PROJECT_ASSIGNMENTS : has
    PROJECTS ||--o{ PROJECT_ASSIGNMENTS : has
    PROJECTS ||--o{ TASKS : contains
    PEOPLE o|--o{ TASKS : receives
    PROJECTS ||--o{ EXPENSES : incurs
```

# 3. What One Row Means

people: One row is one employee, with their contact information, job title, start date, and who they report to.

projects: One row is one project, with its client if it has one, category, budget, start date, and current status.

project_assignments: One row is one employee working on one project, including their role, weekly hours, and when they joined it.

tasks: One row is one task for one project, including who it is assigned to, if anyone, and when it was created, assigned, due, and completed.

expenses: One row is one expense for one project, including its date, amount, category, and a short note.

# 4. Design Choices