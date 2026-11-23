# OmniPulse Commerce & Metrics Dashboard (Ansible-Automated)

A production-grade Python web application featuring secure session-based authentication, direct CRUD operations for users and catalog products, dummy ecommerce analytics, live CPU hardware telemetry, and an automated zero-touch deployment pipeline driven **strictly through Ansible**, with **MySQL** and **Nginx**.

---

> [!IMPORTANT]
> **Strict Ansible-Only Configuration & Deployment**:
> Do not manually edit any configuration files (such as `.env`, systemd services, or Nginx virtual hosts). All environment variables, database credentials, server ports, and reverse proxy settings are strictly managed, rendered, and deployed via **Ansible**. Any manual file changes will be automatically overwritten by the deployment automation.

---

## High-Level Architecture

```
[ Client / Web Browser ]
           │ (HTTP / HTTPS - Port 80 / 443)
           ▼
[ Nginx Web Server / Reverse Proxy ] ─── (Managed strictly by Ansible)
     ├───► Static Assets (`/static/`) ────► Direct from Disk (Optimized Cache)
     └───► Dynamic Requests ──────────────► Reverse Proxy: http://127.0.0.1:5000
                                                    │
                                                    ▼
                                    [ Gunicorn WSGI Application Server ]
                                     (Managed via Systemd by Ansible)
                                                    │
                                                    ▼
                                       [ Flask App (app.py + ProxyFix) ]
                                                    │
                                                    ▼
                                      [ MySQL Database: `dashboard` ]
                                (Auto-provisioned & Seeded by Ansible)
```

---

## Core Features

- **Zero-Touch Automated Provisioning via Ansible**:
  - Automatically provisions the Python virtual environment, installs dependencies, renders `.env`, generates systemd services, and configures Nginx.
  - Automatically connects to MySQL, provisions the database (`CREATE DATABASE IF NOT EXISTS dashboard`), and initializes all schema tables.
  - Automatically seeds rich initial datasets (Users, Products, Orders, Daily Trends) directly into MySQL.
- **Direct Database CRUD Operations**:
  - **User Accounts (`/users`)**: Create, list, search, filter, update, and delete users directly in MySQL.
  - **Product Catalog (`/items`)**: Create, list, filter by category, monitor low-stock alerts, edit, and delete items directly in MySQL.
- **Executive Analytics Dashboard (`/dashboard`)**:
  - KPI metric cards (Total Revenue, Total Orders, Active Users, Avg. Order Value, Conversion Rate).
  - Interactive Chart.js graphs for 7-day revenue/order trends and sales by product category.
  - Recent orders and top-selling catalog tables.
- **Hardware & Database Telemetry Window (`/statistics`)**:
  - Opens in a **separate window** (`target="_blank"`).
  - Live dummy CPU usage gauge with 4-core allocation bars, clock speed, and CPU temperature.
  - Live RAM and disk storage consumption gauges.
  - Real-time database telemetry (ping latency, QPS throughput, cache hit ratio, active connection pool).
  - One-click dataset re-seeding triggers (`standard` or `large` scale).

---

## Project Structure

```
ansibleWebApp/
├── app.py                      # Flask application factory, routes, auth & CRUD handlers
├── config.py                   # Environment variable loader (.env) & app config
├── database.py                 # Multi-engine DB connector (MySQL/SQLite) & CRUD functions
├── requirements.txt            # Python dependencies (Flask, PyMySQL, gunicorn, etc.)
├── .env.example                # Reference template of environment variables
├── .env                        # Active environment configuration (Managed strictly by Ansible)
├── run.sh                      # Standalone local startup script
├── static/
│   └── css/
│       └── style.css           # Custom styling, responsive badges & animations
├── templates/
│   ├── base.html               # Master layout with navbar, telemetry link & toasts
│   ├── login.html              # Authentication page with demo credentials helper
│   ├── dashboard.html          # Analytics dashboard with Chart.js & data tables
│   ├── statistics.html         # Dedicated separate window for CPU & DB telemetry
│   ├── users/
│   │   ├── index.html          # Users directory with search & filter
│   │   └── form.html           # Add / Edit User form
│   └── items/
│       ├── index.html          # Product catalog inventory directory
│       └── form.html           # Add / Edit Catalog Item form
├── ansible/
│   ├── ansible.cfg             # Ansible engine configuration
│   ├── inventory.ini           # Deployment targets (localhost or remote servers)
│   ├── playbook.yml            # Main deployment & configuration playbook
│   ├── deploy.sh               # Quick execution helper script
│   ├── group_vars/
│   │   └── all.yml             # Central Ansible variables default
│   └── templates/
│       ├── env.j2              # Jinja2 template for rendering .env
│       ├── nginx.conf.j2       # Jinja2 template for Nginx reverse proxy virtual host
│       └── webapp.service.j2   # Systemd service unit template for Gunicorn
└── README.md                   # Documentation
```

---

## Default Administrator Credentials

Configured and maintained by Ansible:

- **Username**: `admin`
- **Password**: `AnsibleAdmin2026!`

---

## Complete Deployment Guide (Ansible + MySQL + Nginx)

All deployment steps are strictly driven by Ansible. You do not need to manually edit `.env`, manually create MySQL tables, or manually write Nginx configuration files.

### Step 1: Ensure MySQL Service is Active

Ensure your MySQL database server is running on the target machine:

```bash
sudo systemctl status mysql
```

Ensure your MySQL administrative user (e.g., `root` with `password123`) has permission to connect:

```bash
sudo mysql -u root -e "
CREATE USER IF NOT EXISTS 'root'@'127.0.0.1' IDENTIFIED BY 'password123';
ALTER USER 'root'@'127.0.0.1' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1' WITH GRANT OPTION;
FLUSH PRIVILEGES;"
```

> **Note**: You do not need to create the database or tables manually. Ansible automatically handles database creation and table seeding!

---

### Step 2: Deploy Strictly Using Ansible

All configurations (database credentials, application name, ports, Nginx settings) are passed directly through Ansible.

#### Standard One-Click Production Deployment
Run the Ansible deployment script with privilege escalation:

```bash
cd /var/www/html/ansibleWebApp
./ansible/deploy.sh --become
```

#### Customizing Configuration via Ansible CLI Parameters
To customize any database credentials, application title, or server parameters, pass them directly via Ansible's `-e` / `--extra-vars` flag. **Do not edit any files manually**:

```bash
./ansible/deploy.sh --become -e "\
  db_type='mysql' \
  db_host='127.0.0.1' \
  db_port=3306 \
  db_user='root' \
  db_password='password123' \
  db_name='dashboard' \
  app_name='Enterprise Sales Portal' \
  admin_username='admin' \
  admin_password='AnsibleAdmin2026!' \
  manage_systemd_service=true \
  manage_nginx=true \
  nginx_port=80 \
  nginx_server_name='_'"
```

Alternatively, you can invoke `ansible-playbook` directly:

```bash
.venv/bin/ansible-playbook -i ansible/inventory.ini ansible/playbook.yml --become -e "\
  db_user='root' \
  db_password='password123' \
  db_name='dashboard' \
  manage_nginx=true"
```

---

### What Ansible Executes Automatically

When you trigger the playbook, Ansible executes the following tasks deterministically:

1. **System & Environment Provisioning**:
   - Ensures the application directory exists with correct permissions.
   - Provisions the Python virtual environment (`.venv`).
   - Installs all dependencies from `requirements.txt` (`Flask`, `PyMySQL`, `gunicorn`, `cryptography`).
2. **Dynamic `.env` Generation**:
   - Compiles [`ansible/templates/env.j2`](file:///var/www/html/ansibleWebApp/ansible/templates/env.j2) using the supplied MySQL credentials and application settings.
   - Deploys the customized `.env` file with secure permissions (`0600`).
3. **Automated Database & Table Creation**:
   - Connects directly to MySQL.
   - Automatically executes `CREATE DATABASE IF NOT EXISTS dashboard`.
   - Creates the `users`, `products`, `orders`, `revenue_trends`, and `database_events` tables.
   - Seeds initial dummy datasets (users, catalog products, orders, and 7-day revenue metrics) into MySQL.
4. **Gunicorn Systemd Service Setup**:
   - Renders [`ansible/templates/webapp.service.j2`](file:///var/www/html/ansibleWebApp/ansible/templates/webapp.service.j2).
   - Installs and enables the `ecommerce-dashboard` systemd service to keep Gunicorn running on boot.
5. **Nginx Reverse Proxy Provisioning**:
   - Installs Nginx package (if not already installed).
   - Renders and deploys [`ansible/templates/nginx.conf.j2`](file:///var/www/html/ansibleWebApp/ansible/templates/nginx.conf.j2) to `/etc/nginx/sites-available/ecommerce-dashboard`.
   - Enables the site symlink in `/etc/nginx/sites-enabled/`.
   - Removes any conflicting default site.
   - Tests configuration syntax with `nginx -t` and reloads Nginx.
6. **Automated Verification**:
   - Queries the application's `/health` endpoint to confirm that the app, Nginx, and MySQL are operational.
   - Outputs a deployment summary banner in the terminal.

---

### Step 3: Verify the Deployment

After the playbook finishes, verify the operational state using standard system commands:

#### 1. Check Service Status
```bash
sudo systemctl status nginx
sudo systemctl status ecommerce-dashboard
```

#### 2. Verify Application Health Endpoint
```bash
curl http://localhost/health
```

Expected JSON response:
```json
{
  "app_name": "Nexus Commerce Dashboard",
  "database_name": "dashboard",
  "database_status": "ok",
  "database_type": "mysql",
  "environment": "production",
  "status": "healthy"
}
```

#### 3. Verify MySQL Data Ingestion
```bash
mysql -u root -p'password123' -h 127.0.0.1 -P 3306 -e "\
  USE dashboard; \
  SHOW TABLES; \
  SELECT COUNT(*) AS total_users FROM users; \
  SELECT COUNT(*) AS total_products FROM products;"
```

---

## Containerized Deployment with Docker & Docker Compose

A production-ready [`Dockerfile`](file:///var/www/html/ansibleWebApp/Dockerfile) and [`docker-compose.yml`](file:///var/www/html/ansibleWebApp/docker-compose.yml) are included for containerized environments.

### Option 1: Full Stack via Docker Compose (App + MySQL 8.0)
Spins up both the Flask application and a persistent MySQL database container:

```bash
docker compose up -d
```
- Web Application: **`http://localhost:5000`**
- Database: MySQL 8.0 running on `3306` with persistent volume `mysql_data`
- Automatically passes container health checks before routing traffic.

To stop the containers:
```bash
docker compose down
```

### Option 2: Build & Run Docker Image Standalone

1. **Build the Docker Image:**
   ```bash
   docker build -t omnipulse-webapp .
   ```

2. **Run Container with Environment Variables:**
   ```bash
   docker run -d \
     --name omnipulse-app \
     -p 5000:5000 \
     -e DB_TYPE=mysql \
     -e DB_HOST=host.docker.internal \
     -e DB_PORT=3306 \
     -e DB_USER=root \
     -e DB_PASSWORD=password123 \
     -e DB_NAME=dashboard \
     omnipulse-webapp
   ```

---

## Standalone Development Startup (Without Nginx)

If you are developing locally and want to test the app without running Nginx or systemd:

```bash
cd /var/www/html/ansibleWebApp
./run.sh
```
Or directly with Python:
```bash
source .venv/bin/activate
python3 app.py
```
Open your browser at **`http://localhost:5000`**.

---

## Application URL Navigation & CRUD Endpoints

| URL Path | Action | Description |
|---|---|---|
| `/login` | Auth | Administrator sign-in form (`admin` / `AnsibleAdmin2026!`) |
| `/logout` | Auth | Terminates session |
| `/dashboard` | View | Executive analytics dashboard with KPI cards & quick CRUD links |
| `/users` | Read | User directory with search bar, status filters, and action buttons |
| `/users/new` | Create | Form to add a new user record directly to MySQL |
| `/users/<id>/edit` | Update | Form to edit user record in MySQL |
| `/users/<id>/delete` | Delete | Removes user record from MySQL |
| `/items` | Read | Catalog items directory with category filter & inventory alerts |
| `/items/new` | Create | Form to add a new product directly to MySQL |
| `/items/<id>/edit` | Update | Form to edit product details in MySQL |
| `/items/<id>/delete` | Delete | Removes item from MySQL |
| `/statistics` | Monitor | **Separate window** for live CPU telemetry & DB statistics |
| `/database/seed` | Seed | Re-seeds dummy data directly into target DB (`scale=standard` or `large`) |
| `/database/test-connection` | Diagnostic | Pings database and returns connection latency and table counts |
| `/api/system-stats` | API | Real-time CPU %, core breakdown, memory, disk, and DB metrics in JSON |
| `/api/metrics` | API | Returns aggregated KPIs, orders, users, and chart points in JSON |
| `/health` | Health Check | Monitoring endpoint returning app name, environment, and DB status |

---

## Troubleshooting & FAQs

### 1. Re-running Ansible with Updated Credentials
To update database credentials or application branding, execute the playbook with the new variables:
```bash
./ansible/deploy.sh --become -e "db_user='root' db_password='password123' db_name='dashboard'"
```
Ansible will automatically update `.env`, re-authenticate with MySQL, and trigger a service reload.

### 2. MySQL Port Connection Issues (`111: Connection Refused`)
- Verify MySQL is listening on TCP port 3306:
  ```bash
  sudo ss -tlpn | grep 3306
  ```
- If your MySQL server binds only to `127.0.0.1`, set `db_host: "127.0.0.1"` in your Ansible execution.

### 3. Nginx 502 Bad Gateway
- Ensure the Gunicorn service is active:
  ```bash
  sudo systemctl status ecommerce-dashboard
  ```
- Inspect Gunicorn logs:
  ```bash
  sudo journalctl -u ecommerce-dashboard -n 50 --no-pager
  ```

### 4. Viewing Nginx Logs
```bash
sudo tail -f /var/log/nginx/*_error.log
sudo tail -f /var/log/nginx/*_access.log
```
