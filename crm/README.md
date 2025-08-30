1. Install Redis and dependencies.
2. Run migrations (`python manage.py migrate`).
3. Start Celery worker (`celery -A crm worker -l info`).
4. Start Celery Beat (`celery -A crm beat -l info`).
5. Verify logs in `/tmp/crm_report_log.txt`.

# CRM Project Setup: Crons - Scheduling and Automating Tasks

## Setup Steps

1. **Install Redis and dependencies**
   - Ensure Redis is installed and running.  
   - Example (Ubuntu/Debian):
     ```bash
     sudo apt update
     sudo apt install redis-server
     ```
   - Example (macOS with Homebrew):
     ```bash
     brew install redis
     brew services start redis
     ```
   - Example (Windows):
     Download from [Redis releases](https://github.com/microsoftarchive/redis/releases) and run:
     ```bash
     redis-server
     ```

   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

---

2. **Run migrations**
   ```bash
   python manage.py migrate
````

---

3. **Start Celery worker**

   ```bash
   celery -A crm worker -l info
   ```

---

4. **Start Celery Beat**

   ```bash
   celery -A crm beat -l info
   ```

---

5. **Verify logs**

   * Confirm that task output is written to:

     ```
     /tmp/crm_report_log.txt
     ```


verify crm/README.md includes all setup steps.

