from decimal import Decimal


def get_simplified_who_median_weight(age_months: float, gender: str) -> Decimal:
    """
    A simplified lookup helper returning median (50th percentile) weight in kg
    based on simplified WHO Child Growth Standards.
    In production, this can parse a full CSV dataset or utilize an absolute formula.
    """
    # Sample curve approximation for the first 12 months
    base_weight = 3.3 if gender == 'M' else 3.2  # Birth average
    monthly_gain = 0.7 if age_months <= 6 else 0.4

    estimated_median = base_weight + (float(age_months) * monthly_gain)
    return Decimal(str(round(estimated_median, 3)))


def calculate_growth_analytics(visits):
    """
    Processes a queryset of clinical visits and transforms biometrics into
    structured temporal datasets for frontend plotting.
    """
    growth_data = {
        'labels': [],  # Timeline labels (e.g., "Age: 2.5 months")
        'weight_kg': [],  # Patient's weight plot points
        'height_cm': [],  # Patient's height plot points
        'who_median_weight': []  # Baseline global target comparison point
    }

    # Sort chronological alignment
    ordered_visits = sorted(visits, key=lambda v: v.visit_date)

    for visit in ordered_visits:
        age_months = visit.age_at_visit_months
        gender = visit.patient.gender

        growth_data['labels'].append(f"{age_months} mth")
        growth_data['weight_kg'].append(float(visit.weight_kg))
        growth_data['height_cm'].append(float(visit.height_cm))

        # Calculate comparison baselines
        median_w = get_simplified_who_median_weight(age_months, gender)
        growth_data['who_median_weight'].append(float(median_w))

    return growth_data