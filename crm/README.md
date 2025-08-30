verify crm/README.md includes all setup steps.

# CRM - Celery Report Setup

This README describes how to install Redis and dependencies, run migrations, start Celery worker and Celery Beat, and verify the weekly CRM report logs for the `crm` app.

> **Important:** These instructions assume you're running from the project root and that the Django app package is named `crm`.

---

## Prerequisites

* Python 3.8+ (3.10+ recommended)
* Git
* Virtual environment tool (`venv`, `virtualenv`)
* Redis (running on `localhost:6379`) or a Redis instance accessible to your machine

---

## 1. Install Redis and dependencies

### Option A — Install dependencies only (if Redis already available)

```bash
# Create & activate virtual environment
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
# venv\Scripts\Activate.ps1

# Install Python dependencies from requirements.txt
pip install -r requirements.txt
```

### Option B — Install Redis locally

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
# verify
redis-cli ping  # should print PONG
```

#### macOS (Homebrew)

```bash
brew install redis
brew services start redis
redis-cli ping
```

#### Windows

* Recommended: use **WSL2** and install Redis inside the WSL distro, or run Redis via Docker:

```bash
# Run Redis in Docker (works on Windows, macOS, Linux)
docker run -d --name redis -p 6379:6379 redis:7
```

If you prefer a hosted Redis provider, update your Django `CELERY_BROKER_URL` accordingly in `crm/settings.py`.

---

## 2. Run migrations

From the project root:

```bash
# Ensure venv is activated
python manage.py migrate
```

If you need to create a superuser:

```bash
python manage.py createsuperuser
```

---

## 3. Start Celery worker

Run the Celery worker for the `crm` app (open a terminal with your virtualenv active):

```bash
celery -A crm worker -l info
```

This will connect to Redis (as configured in `crm/settings.py`) and begin processing tasks.

If you see connection errors like `Error 10061` (cannot connect to `localhost:6379`), ensure Redis is running and accessible.

---

## 4. Start Celery Beat

In a separate terminal (with virtualenv active), start the scheduler:

```bash
celery -A crm beat -l info
```

Celery Beat will schedule periodic tasks defined in `crm/settings.py` (`CELERY_BEAT_SCHEDULE`), including the weekly `generate_crm_report` task.

---

## 5. Verify logs in `/tmp/crm_report_log.txt`

The weekly report task writes to `/tmp/crm_report_log.txt`. To check the file:

```bash
# Show file contents
cat /tmp/crm_report_log.txt

# Or tail to watch new entries as they arrive:
tail -f /tmp/crm_report_log.txt
```

> On Windows using native PowerShell, `/tmp` might not exist — when using Docker or WSL, `/tmp/crm_report_log.txt` inside that environment will be used. Adjust paths accordingly.

---

## Manual Test (trigger the task immediately)

If you want to trigger the report generation without waiting for the scheduled time, run from Django shell or a script:

```bash
# From project root, activate venv first
python manage.py shell
# In the shell:
from crm.tasks import generate_crm_report
generate_crm_report.delay()  # enqueue task
# or run synchronously (for quick local test):
from crm.tasks import generate_crm_report
generate_crm_report()
```

Then check `/tmp/crm_report_log.txt` for an immediate entry.

---

## Troubleshooting

* **Celery cannot connect to Redis:** Ensure Redis is running. If using Docker, the `docker run` command must be active. Check firewall rules if running on a remote machine.
* **No log entries:** Confirm `generate_crm_report` is registered and the Celery worker is running. Verify `CELERY_BEAT_SCHEDULE` in `crm/settings.py` has an entry for `generate-crm-report`.
* **Permissions:** If your environment blocks writing to `/tmp`, change the path in `crm/tasks.py` to a writable location.

---

## Notes

* This README intentionally focuses on Redis, Celery worker, Celery Beat, migrations, and log verification as requested.
* If your Django project uses a different settings module name or project layout, adjust `-A crm` to match your Django project package.

---

**End of CRM Celery Report Setup**

