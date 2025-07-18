def assign_weighted_hours(difficulty, estimated_hours):
    if difficulty == 1:  # Easy
        return estimated_hours * 0.8
    elif difficulty == 2:  # Medium
        return estimated_hours * 1.0
    elif difficulty == 3:  # Hard
        return estimated_hours * 1.2
    else:
        return estimated_hours  # default fallback