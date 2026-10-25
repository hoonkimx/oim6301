import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***The Question***

    A student club planning an outdoor event in Wellesley, Massachusetts could use this tool to determine which day has the best weather conditions. By comparing temperature, rain probability, and wind speed over the next seven days, the tool will help identify which days meet the club's requirements and recommend the best day for the event.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***My Plan Before AI***

    My plan is to start by using the Open-Meteo geocoding API to find the coordinates for Wellesley, Massachusetts. I will then use those coordinates to request the daily weather forecast for the next seven days. The forecast will include the daily high and low temperatures, chance of rain, and maximum wind speed.

    I will organize the forecast data into a list where each day has its own record. Then I will compare each day's weather conditions against the club's limits to determine which days are suitable for an outdoor event. If multiple days meet all the requirements, I will choose the day with the lowest chance of rain, using wind speed as a tiebreaker. If no days qualify, I will select the day that breaks the fewest requirements.

    I will use two functions. The first will take a location name and state, request data from the geocoding API, and return the matching coordinates. The second will take those coordinates, request the weather forecast, and return a list of daily weather records.

    The API addresses will be https://geocoding-api.open-meteo.com/v1/search and https://api.open-meteo.com/v1/forecast.

    I will check that I have all the records by comparing the number of days in my results with the seven dates returned by the forecast API.

    To verify my results in Section 6, I will independently count the number of days that meet all four weather requirements and compare that number with the number of passing days reported by my tool.
    """)
    return


if __name__ == "__main__":
    app.run()
