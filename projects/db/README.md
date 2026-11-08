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
    PROJECTS ||--|{ PROJECT_ASSIGNMENTS : has
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

## Keys

Employees use person_id rather than work_email because an email can change
when someone's title changes. The ID stays the same, so their tasks and project
assignments still point to the right person. Each employee's current email must
still be unique. Each person-project pair appears only once in project_assignments.

## Optional relationships

A person can have no manager because the two founders report to nobody.
A project can have no client because some projects are internal. A task can
have no assignee because new tasks may be unassigned, and it has no completion
date until it is finished. A project can have no expenses, which is also one
of the business questions. A person can have no project assignments. Each
project needs assigned people; the generated data gives every project four.

## Rules that need a query

The tables check that a task's project and assignee each exist, but they do not
check that the assignee works on that particular project. A query will compare
the task's person-project pair with project_assignments. Tasks 299 and 300 are
the only intentional violations. Another query will compare task assignment
dates with employee start dates; the generated data has no violations of that
rule. A date comparison inside one task, such as completion not preceding
creation, is enforced with CHECK instead.

An ordinary foreign key also cannot require every project to have people
assigned to it. A query can find projects with fewer than two assignments;
the generated data gives each project four, matching the scenario's description
of several people. The ERD marks this relationship as required.

## Agent proposal revised

The agent's initial ERD allowed a project to have no employee assignments.
That was revised to a required relationship because the scenario says a project
has several people. The generated assignments also need checking: a diagram
alone does not enforce the minimum number of employees on a project.
