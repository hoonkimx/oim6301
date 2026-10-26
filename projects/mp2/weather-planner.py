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
    # Mini Project 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Question

    A student club planning an outdoor event in Wellesley, Massachusetts could use this tool to determine which day has the best weather conditions. By comparing temperature, rain probability, and wind speed over the next seven days, the tool will help identify which days meet the club's requirements and recommend the best day for the event.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## My Plan Before AI

    My plan is to start by using the Open-Meteo geocoding API to find the coordinates for Wellesley, Massachusetts. I will then use those coordinates to request the daily weather forecast for the next seven days. The forecast will include the daily high and low temperatures, chance of rain, and maximum wind speed.

    I will organize the forecast data into a list where each day has its own record. Then I will compare each day's weather conditions against the club's limits to determine which days are suitable for an outdoor event. If multiple days meet all the requirements, I will choose the day with the lowest chance of rain, using wind speed as a tiebreaker. If no days qualify, I will select the day that breaks the fewest requirements.

    I will use two functions. The first will take a location name and state, request data from the geocoding API, and return the matching coordinates. The second will take those coordinates, request the weather forecast, and return a list of daily weather records.

    The API addresses will be https://geocoding-api.open-meteo.com/v1/search and https://api.open-meteo.com/v1/forecast.

    I will check that I have all the records by comparing the number of days in my results with the seven dates returned by the forecast API.

    To verify my results in Section 6, I will independently count the number of days that meet all four weather requirements and compare that number with the number of passing days reported by my tool.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inputs
    """)
    return


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"

    lowest_high_f = 55
    highest_high_f = 80
    max_rain_chance = 0
    max_wind_mph = 15
    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Work
    """)
    return


@app.cell
def _():
    import requests

    def get_coordinates(place, state):
        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": place,
            "count": 100,
            "countryCode": "US",
            "format": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        for location in data["results"]:
            if location["admin1"] == state:
                return location["latitude"], location["longitude"], location["name"]

        return None

    return get_coordinates, requests


@app.cell
def _(get_coordinates, place, state):
    latitude, longitude, location_name = get_coordinates(place, state)

    print(f"Location: {location_name}, {state}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    return latitude, location_name, longitude


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Seven Day Forecast
    """)
    return


@app.cell
def _(requests):
    def get_forecast(latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        daily = data["daily"]

        forecast = []

        for day, high, low, rain, wind in zip(
            daily["time"],
            daily["temperature_2m_max"],
            daily["temperature_2m_min"],
            daily["precipitation_probability_max"],
            daily["wind_speed_10m_max"]
        ):
            forecast.append({
                "date": day,
                "high": high,
                "low": low,
                "rain": rain,
                "wind": wind
            })

        return forecast

    return (get_forecast,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function Test
    """)
    return


@app.cell
def _(get_forecast, latitude, longitude):
    forecast = get_forecast(latitude, longitude)

    for _day in forecast:
        print(_day)
    return (forecast,)


@app.cell
def _(forecast):
    print(f"Forecast records retrieved: {len(forecast)}")

    if len(forecast) == 7:
        print("Record count verified.")
    else:
        print("Warning: Expected 7 forecast records.")
    return


@app.cell
def _(forecast):
    import json
    from pathlib import Path

    data_folder = Path("projects/mp2/data")
    data_folder.mkdir(parents=True, exist_ok=True)

    with open(data_folder / "wellesley_forecast.json", "w") as file:
        json.dump(
        [
            {key: value for key, value in day.items() if key != "passes"}
            for day in forecast
        ],
        file,
        indent=2
    )

    print("Forecast data saved successfully.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Weather Rules
    """)
    return


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    for _day in forecast:
        _day["passes"] = (
            _day["high"] >= lowest_high_f
            and _day["high"] <= highest_high_f
            and _day["rain"] <= max_rain_chance
            and _day["wind"] <= max_wind_mph
        )

        print(f"{_day['date']}: {_day['passes']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Best Day
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Original best-day selection before adding fallback logic*
    """)
    return


@app.cell
def _():
    ##best_day = None

    ##for _day in forecast:
    #    if _day["passes"]:
    #        if best_day is None:
    #            best_day = _day
    #        elif _day["rain"] < best_day["rain"]:
    #            best_day = _day
    #        elif _day["rain"] == best_day["rain"]:
    #            if _day["wind"] < best_day["wind"]:
    #                best_day = _day

    #print(f"Best day: {best_day['date']}")
    #print(f"Rain chance: {best_day['rain']}%")
    #print(f"Maximum wind: {best_day['wind']} mph")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *With fallback logic*
    """)
    return


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    selected_day = None

    for _day in forecast:
        if _day["passes"]:
            if selected_day is None:
                selected_day = _day
            elif _day["rain"] < selected_day["rain"]:
                selected_day = _day
            elif _day["rain"] == selected_day["rain"]:
                if _day["wind"] < selected_day["wind"]:
                    selected_day = _day

    if selected_day is None:
        fewest_broken_rules = None

        for _day in forecast:
            broken_rules = 0

            if _day["high"] < lowest_high_f:
                broken_rules += 1
            if _day["high"] > highest_high_f:
                broken_rules += 1
            if _day["rain"] > max_rain_chance:
                broken_rules += 1
            if _day["wind"] > max_wind_mph:
                broken_rules += 1

            if fewest_broken_rules is None or broken_rules < fewest_broken_rules:
                fewest_broken_rules = broken_rules
                selected_day = _day

    print(f"Best day: {selected_day['date']}")
    print(f"Rain chance: {selected_day['rain']}%")
    print(f"Maximum wind: {selected_day['wind']} mph")
    return (selected_day,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Answer
    """)
    return


@app.cell
def _(forecast, location_name, selected_day, state):
    print(f"Weather forecast for {location_name}, {state}")
    print(f"{'Date':<14} {'High':>8} {'Low':>8} {'Rain %':>10} {'Wind mph':>10} {'Passes':>10}")
    print("-" * 65)

    for _day in forecast:
        print(
            f"{_day['date']:<14} "
            f"{_day['high']:>8.1f} "
            f"{_day['low']:>8.1f} "
            f"{_day['rain']:>10} "
            f"{_day['wind']:>10.1f} "
            f"{str(_day['passes']):>10}"
        )

    print()

    if selected_day["passes"]:
        print(
            f"I recommend {selected_day['date']} for the outdoor event in "
            f"{location_name}, {state}, because it meets all the weather "
            f"requirements with {selected_day['rain']}% rain probability "
            f"and maximum wind of {selected_day['wind']} mph."
        )
    else:
        print(
            f"No days meet all the weather requirements. "
            f"The closest option is {selected_day['date']}, "
            f"with {selected_day['rain']}% rain probability "
            f"and maximum wind of {selected_day['wind']} mph."
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Verification
    """)
    return


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    verified_pass_count = 0

    for _day in forecast:
        if (
            lowest_high_f <= _day["high"] <= highest_high_f
            and _day["rain"] <= max_rain_chance
            and _day["wind"] <= max_wind_mph
        ):
            verified_pass_count += 1

    reported_pass_count = 0

    for _day in forecast:
        if _day["passes"]:
            reported_pass_count += 1

    print(f"Independently calculated passing days: {verified_pass_count}")
    print(f"Passing days reported by the tool: {reported_pass_count}")

    if verified_pass_count == reported_pass_count:
        print("Verification passed!")
    else:
        print("Verification failed!")
    return


@app.cell
def _(
    forecast,
    highest_high_f,
    lowest_high_f,
    max_rain_chance,
    max_wind_mph,
    selected_day,
):
    passing_days_check = []

    for _day in forecast:
        if (
            lowest_high_f <= _day["high"] <= highest_high_f
            and _day["rain"] <= max_rain_chance
            and _day["wind"] <= max_wind_mph
        ):
            passing_days_check.append(_day)

    if passing_days_check:
        expected_day = min(
            passing_days_check,
            key=lambda d: (d["rain"], d["wind"])
        )

        print(f"Expected best day: {expected_day['date']}")
        print(f"Tool selected: {selected_day['date']}")
        print(f"Best-day verification passed: {expected_day['date'] == selected_day['date']}")
    else:
        print("No qualifying days to verify with this check.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To verify my results, I independently checked the weather conditions for each day against the four requirements. I then compared the number of days that passed this calculation with the number of passing days reported by my tool.

    With the original rain limit of 30%, both calculations identified 7 suitable days. After changing the rain limit to 0% in Section 8, both calculations identified 3 suitable days. The verification passed in both cases.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Working with the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I used AI to help write the functions for retrieving weather data and selecting the best day for an outdoor event. One issue I encountered was that Marimo would not allow me to define the same variable, best_day, in two separate cells. I corrected this by changing the variable name to selected_day in the updated selection code in Section 4. After making the change, the code ran successfully and selected October 28 as the best day. I also independently checked the weather requirements in Section 6, where both calculations identified 7 suitable days.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading it Back

    **Function 1:** get_coordinates()

    The get_coordinates function takes a place and state as inputs and uses the Open-Meteo geocoding API to find the location. It returns the latitude, longitude, and location name. One line I needed clarification on was response.raise_for_status(), which checks if the API request was successful and raises an error if it wasn't.

    **Function 2:** get_forecast()

    The get_forecast function takes the latitude and longitude as inputs and uses them to request seven days of weather data. It returns a list of dictionaries containing the date, high and low temperatures, rain probability, and maximum wind speed for each day. One line I needed clarification on was zip(), which allows the code to loop through multiple lists at the same time and combine the corresponding values.

    **Prediction**

    I predict that changing max_rain_chance from 30 to 0 will reduce the number of passing days from 7 to 3. I also predict that October 28 will remain the recommended day because it has a 0% chance of rain and the lowest wind speed among the days with no expected rain.

    **Actual Results**

    After changing max_rain_chance from 30 to 0, the number of passing days decreased from 7 to 3, which matched my prediction. October 25, 28, and 29 were the only days that met all four requirements. October 28 also remained the recommended day because it had a 0% chance of rain and the lowest maximum wind speed at 4.8 mph. Although some of the forecast values changed slightly when I reran the API request, the overall results matched my prediction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further
    """)
    return


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    print("Weather Suitability Scores")
    print(f"{'Date':<14} {'Score':>8}")
    print("-" * 24)

    for _day in forecast:
        score = 10

        if _day["high"] < lowest_high_f or _day["high"] > highest_high_f:
            score -= 2

        if _day["rain"] > max_rain_chance:
            score -= 2

        if _day["wind"] > max_wind_mph:
            score -= 2

        score -= _day["rain"] / 20
        score -= _day["wind"] / 20

        score = max(0, round(score, 1))

        print(f"{_day['date']:<14} {score:>8.1f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For my extension, I added a weather suitability score out of 10 for each day. The score considers whether the day meets the club's requirements, while also accounting for differences in rain probability and wind speed. This gives the club another way to compare the forecast beyond simply identifying which days pass or fail. I kept the original recommendation logic unchanged.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3.75 Hours
    """)
    return


if __name__ == "__main__":
    app.run()
