from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from .models import Device, MaintenanceTask, PMTemplate


def _template_match_q(device):
    return (
        Q(device_type=device.device_type)
        & (Q(manufacturer='') | Q(manufacturer__iexact=device.manufacturer))
        & (Q(model='') | Q(model__iexact=device.model))
        & Q(is_active=True)
    )


def get_best_template_for_device(device):
    templates = PMTemplate.objects.filter(_template_match_q(device))
    return templates.order_by('-manufacturer', '-model', 'interval_days').first()


def schedule_device_tasks(device, horizon_days=180, reference_date=None):
    """Ensure future tasks exist for a device based on best matching PM template."""
    reference_date = reference_date or timezone.now().date()
    template = get_best_template_for_device(device)
    if not template:
        return []

    start_due_date = device.next_maintenance or reference_date
    horizon = reference_date + timedelta(days=horizon_days)

    created = []
    due_date = start_due_date
    while due_date <= horizon:
        reminder_date = due_date - timedelta(days=template.reminder_days_before)
        task, was_created = MaintenanceTask.objects.get_or_create(
            device=device,
            template=template,
            due_date=due_date,
            defaults={'reminder_date': reminder_date},
        )
        if was_created:
            created.append(task)
        due_date += timedelta(days=template.interval_days)

    return created


def refresh_all_task_statuses(reference_date=None):
    reference_date = reference_date or timezone.now().date()
    tasks = MaintenanceTask.objects.exclude(status__in=['completed', 'cancelled']).select_related('template')
    for task in tasks:
        previous = (task.status, task.urgency)
        task.refresh_status(reference_date=reference_date)
        if previous != (task.status, task.urgency):
            task.save(update_fields=['status', 'urgency', 'updated_at'])


def sync_calendar(horizon_days=180):
    for device in Device.objects.all():
        schedule_device_tasks(device, horizon_days=horizon_days)
    refresh_all_task_statuses()
