<!-- Copilot instructions — hospital_system (concise, merged & updated) -->

This Django monolith manages hospital device inventory & maintenance. Use these repo-specific rules to be immediately productive.

## Big picture
- Single Django project at hospital_system/ with main app devices/.
- Read first: hospital_system/settings.py, devices/models.py, devices/views.py, devices/urls.py, devices/utils/prediction.py, templates/devices/.
- Key domain objects: Device, Department, Maintenance (see devices/models.py). Prediction and QR generation are centralized on the model & utils.

## Data flow & architecture
- Views call the Django ORM directly and pass context dicts to templates. Expect context keys like devices, departments, status_choices.
- Reuse compute_failure_prediction(device, maintenances_qs) from devices/utils/prediction.py for failure heuristics.
- Device.generate_qr_code() writes ImageField Device.qr_code under MEDIA_ROOT/qr_codes/.

## Development & runtime (Windows PowerShell)
- Activate virtualenv:
  & venv\Scripts\Activate.ps1
- Common commands:
  - python manage.py makemigrations
  - python manage.py migrate
  - python manage.py runserver
  - python manage.py test devices
  - python manage.py collectstatic --noinput
- DB: db.sqlite3 by default. Use management script reset_db.py to reset + seed samples.

## Conventions & patterns (must follow)
- Use function-based views only; preserve decorators (@login_required, @require_GET, @require_POST).
- API responses: JsonResponse with explicit status codes (see device_lookup_api in devices/views.py).
- Template names and context keys are stable — follow templates/devices/*.html keys used by existing views.
- Reuse domain helpers: Device.generate_qr_code() and compute_failure_prediction().
- Excel exports use openpyxl (devices/views.py::devices_export_excel). Avoid loading huge querysets into memory — use batching/streaming.

## Integration points & infra
- Admin customizations: devices/admin.py.
- Migrations: devices/migrations/ — do not manually edit generated migration files.
- Media files depend on MEDIA_ROOT/MEDIA_URL in settings.py for QR images and uploads.

## Testing & changes
- Add tests in devices/tests.py for behavioral or endpoint changes.
- Keep diffs minimal and consistent: function-based views, same decorators, messages + redirects pattern.
- Follow URL naming convention in devices/urls.py (e.g., control-center/api/stats/ -> control_center_stats_api).

## Quick references (examples)
- Prediction: devices/utils/prediction.py::compute_failure_prediction(device, maintenances_qs)
- QR generation: devices/models.py::Device.generate_qr_code()
- Example API view: devices/views.py::device_lookup_api (JsonResponse)
- Export: devices/views.py::devices_export_excel (openpyxl)
- Template dir: templates/devices/ (views expect keys like devices, departments, form)

If any section is unclear or you want unit test templates, CI steps, lint rules, or inline comment cleanup examples, tell me which area to expand.
