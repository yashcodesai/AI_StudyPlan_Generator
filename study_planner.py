from utils.optimizer import assign_weighted_hours
import pandas as pd
import math

def generate_plan(selected_subjects, daily_hours, total_days):
    # Load the topic data
    df = pd.read_csv("data/topics_difficulty.csv")
    df.columns = df.columns.str.strip() #Remove extra spaces from column names
    print("CSV Columns:", df.columns)

    # Filter topics by selected subjects
    df = df[df["Subject"].isin(selected_subjects)]

    # Sort by Difficulty (Easy < Medium < Hard)
    difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}
    df["Difficulty_Level"] = df["Difficulty"].map(difficulty_order)
    df = df.sort_values(by="Difficulty_Level")
    df["Weighted_Hours"] = df.apply(
    lambda row: assign_weighted_hours(row["Difficulty"], row["Estimated_Hours"]), axis=1
)

    # Calculate total study time required
    total_hours_needed = df["Estimated_Hours"].sum()

    # Calculate total available hours
    total_available_hours = daily_hours * total_days

    if total_hours_needed > total_available_hours:
        return pd.DataFrame([{
            "Day": "⚠️",
            "Subject": "Not enough time to cover all topics.",
            "Topic": "Reduce subject choices or increase hours/days.",
            "Hours": "-"
        }])

    # Build the plan
    plan = []
    current_day = 1
    remaining_hours_today = daily_hours

    for _, row in df.iterrows():
        hours_needed = row["Weighted_Hours"]
        while hours_needed > 0:
            hours_today = min(hours_needed, remaining_hours_today)
            plan.append({
                "Day": f"Day {current_day}",
                "Subject": row["Subject"],
                "Topic": row["Topic"],
                "Hours": hours_today
            })
            hours_needed -= hours_today
            remaining_hours_today -= hours_today

            if remaining_hours_today == 0:
                current_day += 1
                remaining_hours_today = daily_hours

    return pd.DataFrame(plan)