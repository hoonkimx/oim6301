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
    # Going further
    holding_cost = 0.50
    delivery_cost = 40
    lost_sale_cost = 8
    return (
        daily_demand,
        delivery_cost,
        holding_cost,
        lead_time_days,
        lost_sale_cost,
        order_quantity,
        reorder_points,
        starting_stock,
    )


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
def _(daily_demand, lead_time_days, order_quantity, starting_stock):
    reorder_point = 40
    deliveries = {}

    stock = starting_stock

    daily_results = []

    for day in range(1, len(daily_demand) + 1):
        starting_inventory = stock
        arrived = 0
    
        if day in deliveries:
            arrived = deliveries[day]
            stock = stock + arrived
    
        demand = daily_demand[day - 1]
        sold = min(stock, demand)
        lost = demand - sold
        stock = stock - sold

        pending_stock = 0

        units_ordered = 0
    
        for delivery_day in deliveries:
            if delivery_day > day:
                pending_stock = pending_stock + deliveries[delivery_day]

        if stock + pending_stock <= reorder_point:
            deliveries[day + lead_time_days] = order_quantity
            units_ordered = order_quantity
    
        daily_results.append({
            "day": day,
            "starting_stock": starting_inventory,
            "arrived": arrived,
            "demand": demand,
            "sold": sold,
            "lost": lost,
            "ending_stock": stock,
            "units_ordered": units_ordered
        })
    return (daily_results,)


@app.cell
def _(
    daily_demand,
    lead_time_days,
    order_quantity,
    reorder_points,
    starting_stock,
):
    def simulate(reorder_point):
        stock = starting_stock
        deliveries = {}
        results = []

        for day in range(1, len(daily_demand) + 1):
            starting_inventory = stock
            arrived = 0

            if day in deliveries:
                arrived = deliveries[day]
                stock = stock + arrived

            demand = daily_demand[day - 1]
            sold = min(stock, demand)
            lost = demand - sold
            stock = stock - sold

            pending_stock = 0

            for delivery_day in deliveries:
                if delivery_day > day:
                    pending_stock = pending_stock + deliveries[delivery_day]

            units_ordered = 0

            if stock + pending_stock <= reorder_point:
                deliveries[day + lead_time_days] = order_quantity
                units_ordered = order_quantity

            results.append({
                "day": day,
                "starting_stock": starting_inventory,
                "arrived": arrived,
                "demand": demand,
                "sold": sold,
                "lost": lost,
                "ending_stock": stock,
                "units_ordered": units_ordered
            })

        return results


    comparison = []

    for point in reorder_points:
        results = simulate(point)

        units_lost = 0
        days_lost = 0
        orders_placed = 0
        total_ending_stock = 0

        for result_row in results:
            units_lost = units_lost + result_row["lost"]
            total_ending_stock = total_ending_stock + result_row["ending_stock"]
    
            if result_row["lost"] > 0:
                days_lost = days_lost + 1
    
            if result_row["units_ordered"] > 0:
                orders_placed = orders_placed + 1

        average_stock = total_ending_stock / len(results)

        comparison.append({
            "reorder_point": point,
            "units_lost": units_lost,
            "days_lost": days_lost,
            "orders_placed": orders_placed,
            "average_stock": average_stock
        })

    
    print(f"{'Reorder Point':>15} {'Units Lost':>12} {'Days Lost':>12} {'Orders':>10} {'Avg Stock':>12}")
    print("-" * 65)

    for comparison_row in comparison:
        print(
            f"{comparison_row['reorder_point']:>15} "
            f"{comparison_row['units_lost']:>12} "
            f"{comparison_row['days_lost']:>12} "
            f"{comparison_row['orders_placed']:>10} "
            f"{comparison_row['average_stock']:>12.2f}"
        )
    return (simulate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(daily_results):
    print(f"{'Day':>5} {'Start':>8} {'Arrived':>8} {'Demand':>8} {'Sold':>8} {'Lost':>8} {'End':>8} {'Ordered':>8}")
    print("-" * 75)

    for row in daily_results:
        print(f"{row['day']:>5} {row['starting_stock']:>8} {row['arrived']:>8} {row['demand']:>8} {row['sold']:>8} {row['lost']:>8} {row['ending_stock']:>8} {row['units_ordered']:>8}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I recommend a reorder point of 40 cartons because it resulted in zero lost sales over the 30-day period with four orders placed and an average ending inventory of 48.43 cartons, compared to 58.43 cartons with a reorder point of 50.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(daily_results, starting_stock):
    total_sold = 0
    total_arrived = 0

    for verification_row in daily_results:
        total_sold = total_sold + verification_row["sold"]
        total_arrived = total_arrived + verification_row["arrived"]

    calculated_ending_stock = starting_stock + total_arrived - total_sold
    simulation_ending_stock = daily_results[-1]["ending_stock"]

    print(f"Independently calculated ending stock: {calculated_ending_stock}")
    print(f"Simulation ending stock: {simulation_ending_stock}")

    if calculated_ending_stock == simulation_ending_stock:
        print("Verification passed!")
    else:
        print("Verification failed!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To verify my results, I independently calculated the ending inventory by adding all deliveries received to the starting inventory and subtracting the total number of cartons sold. This calculation resulted in 61 cartons, which matched the simulation's ending inventory of 61 cartons. Since both calculations produced the same result, the verification passed.
    """)
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
    I used AI to help develop the inventory simulation and organize the results into tables. One issue I encountered was that my original code repeatedly printed the first day's results instead of displaying each day separately. I corrected the print statement and verified that the final table displayed all 30 days correctly. I also checked the inventory calculations independently in Section 6 to confirm that the results were accurate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(delivery_cost, holding_cost, lost_sale_cost, simulate):
    #the following was added to inputs
    #holding_cost = 0.50
    #delivery_cost = 40
    #lost_sale_cost = 8

    cost_results = []

    for test_point in range(10, 81):
        test_results = simulate(test_point)

        total_cost = 0

        for cost_row in test_results:
            total_cost = total_cost + cost_row["ending_stock"] * holding_cost
            total_cost = total_cost + cost_row["lost"] * lost_sale_cost

            if cost_row["units_ordered"] > 0:
                total_cost = total_cost + delivery_cost

        cost_results.append({
            "reorder_point": test_point,
            "total_cost": total_cost
        })

    best_point = cost_results[0]

    for cost_comparison in cost_results:
        if cost_comparison["total_cost"] < best_point["total_cost"]:
            best_point = cost_comparison

    print(f"Best reorder point: {best_point['reorder_point']}")
    print(f"Lowest total cost: ${best_point['total_cost']:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I added inventory holding costs, delivery costs, and lost sales costs to the simulation. I then tested reorder points from 10 to 80 to determine which resulted in the lowest total cost over the 30-day period. The optimal reorder point was 36 cartons, with a total cost of $886.50. This suggests that a reorder point of 36 provides the best balance between inventory costs, ordering costs, and lost sales under the given assumptions.
    """)
    return


if __name__ == "__main__":
    app.run()
