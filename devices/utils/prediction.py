# devices/utils/prediction.py
from dataclasses import dataclass
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

@dataclass
class FailurePrediction:
    risk_percent: int
    risk_level: str
    predicted_failure_date: object  # date
    confidence: str
    drivers: list


def _clamp(v: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, v))


def compute_failure_prediction(device, maintenances_qs) -> FailurePrediction:
    """
    Heuristic prediction based on your real schema:
    - Maintenance types: preventive/corrective/emergency/calibration
    - completed (bool)
    - cost
    - device.status active/inactive/maintenance/retired
    - device.next_maintenance
    """

    today = timezone.localdate()
    last_30 = today - timedelta(days=30)
    last_90 = today - timedelta(days=90)

    total = maintenances_qs.count()

    m30 = maintenances_qs.filter(date__gte=last_30).count()
    m90 = maintenances_qs.filter(date__gte=last_90).count()

    # Failure-proxy: corrective + emergency are the strongest signals in your dataset
    corrective_90 = maintenances_qs.filter(date__gte=last_90, maintenance_type="corrective").count()
    emergency_90 = maintenances_qs.filter(date__gte=last_90, maintenance_type="emergency").count()

    # Incomplete maintenances indicate instability or backlog
    open_count = maintenances_qs.filter(completed=False).count()

    # Cost signals
    recent_cost = maintenances_qs.filter(date__gte=last_90).aggregate(s=Sum("cost"))["s"] or 0

    drivers = []
    score = 0

    # Frequency scoring
    if m30 >= 3:
        score += 18; drivers.append(f"High maintenance frequency in last 30 days ({m30}).")
    elif m30 == 2:
        score += 10; drivers.append("Two maintenances in last 30 days.")
    elif m30 == 1:
        score += 5; drivers.append("One maintenance in last 30 days.")

    if m90 >= 6:
        score += 14; drivers.append(f"High maintenance frequency in last 90 days ({m90}).")
    elif m90 >= 3:
        score += 8; drivers.append(f"Moderate maintenance frequency in last 90 days ({m90}).")

    # Corrective/Emergency are strong risk drivers
    if emergency_90 >= 2:
        score += 30; drivers.append(f"Multiple emergency maintenances in last 90 days ({emergency_90}).")
    elif emergency_90 == 1:
        score += 18; drivers.append("Emergency maintenance recorded recently.")

    if corrective_90 >= 2:
        score += 22; drivers.append(f"Multiple corrective maintenances in last 90 days ({corrective_90}).")
    elif corrective_90 == 1:
        score += 12; drivers.append("Corrective maintenance recorded recently.")

    # Open/incomplete work
    if open_count >= 2:
        score += 18; drivers.append(f"There are {open_count} incomplete maintenance records.")
    elif open_count == 1:
        score += 10; drivers.append("There is an incomplete maintenance record.")

    # Cost effect (tune thresholds as you like)
    if recent_cost >= 20000:
        score += 12; drivers.append(f"High maintenance cost in last 90 days ({int(recent_cost)} EGP).")
    elif recent_cost >= 8000:
        score += 7; drivers.append("Elevated maintenance cost in last 90 days.")

    # Device status impact
    if device.status == "maintenance":
        score += 15; drivers.append("Device is currently under maintenance.")
    elif device.status == "inactive":
        score += 20; drivers.append("Device is currently inactive.")
    elif device.status == "retired":
        score += 35; drivers.append("Device is retired (operational risk is effectively critical).")

    # Next maintenance proximity/overdue
    if device.next_maintenance:
        days_to_next = (device.next_maintenance - today).days
        if days_to_next < 0:
            score += 18; drivers.append("Next maintenance is overdue.")
        elif days_to_next <= 7:
            score += 10; drivers.append("Next maintenance due within 7 days.")
        elif days_to_next <= 21:
            score += 5; drivers.append("Next maintenance due within 21 days.")

    # Confidence from data volume
    if total >= 12:
        confidence = "High"
    elif total >= 5:
        confidence = "Medium"
    else:
        confidence = "Low"
        drivers.append("Limited historical maintenance data reduces confidence.")

    risk_percent = _clamp(int(score))

    if risk_percent >= 80:
        level = "Critical"
        eta_days = 7
    elif risk_percent >= 60:
        level = "High"
        eta_days = 21
    elif risk_percent >= 35:
        level = "Medium"
        eta_days = 45
    else:
        level = "Low"
        eta_days = 90

    predicted_failure_date = today + timedelta(days=eta_days)

    return FailurePrediction(
        risk_percent=risk_percent,
        risk_level=level,
        predicted_failure_date=predicted_failure_date,
        confidence=confidence,
        drivers=drivers[:6],
    )
