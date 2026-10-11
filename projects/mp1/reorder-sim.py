# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Someone who could potentially use this, is a coffee shop owner to help determine when to reorder milk. By simulating daily deman and inventory levels, the tool compares different reorder points to identify which option best balances lost sales and excess inventory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My plan is to start with the 60 cartons of oat milk and the provided daily demand data. Then simulate each day, checking whether any previously ordered cartons arrive. Subract the number of cartons sold from the available inventory and record any lost sales. Check whether the remaining inventory plus pending orders at or below the reorder point. If so, place an order for 100 cartons to arrive three days later. THen repeat the process for all 30 days, carrying the remaining inventory and outstanding orders forward.

    I will then run the simulation separately for reorder points of 20, 30, 40, and 50. Then compare those results and see which reorder point provides the best balance between lost sales and inventory levels. The loop carries forward the remaining inventory and any pending orders from one day to the next. This allows the simulation to track how much stock is available and when new deliveries will arrive. I will check that the starting inventory pluys any deliveries, minus the cartons sold, equals the ending inventory. I will compare this independently calculated number with the ending inventory produced by the sim.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Your inputs.
    starting_stock = 60
    order_quantity = 100
    lead_time_days = 3
    reorder_points = [20, 30, 40, 50]
    daily_demand = [12, 15, 9, 14, 18, 11, 10, 16, 13, 17, 8, 12, 20, 14, 11,
                    9, 15, 13, 16, 12, 10, 14, 19, 11, 13, 15, 9, 12, 17, 14]
    return daily_demand, starting_stock


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    ## test cell
    #stock = starting_stock
    #demand = daily_demand[0]
    #sold = min(stock, demand)
    #stock = stock - sold
    #print(stock)
    return


@app.cell
def _(daily_demand, starting_stock):
    stock = starting_stock

    for demand in daily_demand:
        sold = min(stock, demand)
        stock = stock - sold
        print(stock)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
