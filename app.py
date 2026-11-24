from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from config import Config
from database import (
    init_db,
    get_dashboard_data,
    get_db_connection,
    get_system_statistics,
    test_db_connection,
    seed_dummy_data,
    # User CRUD
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user,
    # Product CRUD
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product,
)
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Configure proxy headers support when running behind Nginx / reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Initialize database schema and dummy seed data directly in the target database
try:
    init_db()
except Exception as e:
    print(f"[WARNING] Database initialization deferred: {e}")


def login_required(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function


@app.context_processor
def inject_global_vars():
    """Injects common variables into all templates."""
    return {
        "app_name": Config.APP_NAME,
        "app_env": Config.APP_ENV,
        "current_user": session.get("username", "Guest"),
        "db_info": Config.get_db_info(),
    }


@app.route("/")
def index():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            flash(f"Welcome back, {username}! You have successfully logged in.", "success")
            next_url = request.args.get("next") or url_for("dashboard")
            return redirect(next_url)
        else:
            flash("Invalid username or password. Please verify your credentials.", "danger")

    return render_template(
        "login.html",
        demo_user=Config.ADMIN_USERNAME,
        demo_pass=Config.ADMIN_PASSWORD,
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    data = get_dashboard_data()
    db_info = Config.get_db_info()
    return render_template(
        "dashboard.html",
        kpis=data["kpis"],
        recent_orders=data["recent_orders"],
        recent_users=data["recent_users"],
        top_products=data["top_products"],
        charts=data["charts"],
        db_info=db_info,
    )


# ==============================================================================
# CRUD ROUTES: USER ACCOUNTS
# ==============================================================================

@app.route("/users")
@login_required
def users_list():
    """Read: List all users with optional search and status filters."""
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()
    users = get_all_users(search=search, status_filter=status_filter)
    return render_template(
        "users/index.html",
        users=users,
        search_query=search,
        status_filter=status_filter,
    )


@app.route("/users/new", methods=["GET", "POST"])
@login_required
def users_create():
    """Create: Add a new user directly to the database."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "Customer")
        status = request.form.get("status", "Active")
        country = request.form.get("country", "").strip()
        try:
            total_spent = float(request.form.get("total_spent", 0.0))
        except ValueError:
            total_spent = 0.0

        if not name or not email:
            flash("Name and email are required fields.", "danger")
            return render_template("users/form.html", user=None)

        try:
            user_id = create_user(name, email, role, status, country, total_spent)
            flash(f"User '{name}' (ID: #{user_id}) created successfully in {Config.DB_TYPE.upper()} database!", "success")
            return redirect(url_for("users_list"))
        except Exception as e:
            flash(f"Database Error creating user: {str(e)}", "danger")

    return render_template("users/form.html", user=None)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def users_edit(user_id):
    """Update: Modify an existing user record in the database."""
    user = get_user_by_id(user_id)
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for("users_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "Customer")
        status = request.form.get("status", "Active")
        country = request.form.get("country", "").strip()
        try:
            total_spent = float(request.form.get("total_spent", 0.0))
        except ValueError:
            total_spent = 0.0

        try:
            update_user(user_id, name, email, role, status, country, total_spent)
            flash(f"User #{user_id} ('{name}') updated successfully!", "success")
            return redirect(url_for("users_list"))
        except Exception as e:
            flash(f"Error updating user: {str(e)}", "danger")

    return render_template("users/form.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def users_delete(user_id):
    """Delete: Remove a user record from the database."""
    try:
        delete_user(user_id)
        flash(f"User #{user_id} deleted successfully from database.", "info")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "danger")
    return redirect(url_for("users_list"))


# ==============================================================================
# CRUD ROUTES: PRODUCTS / ITEMS
# ==============================================================================

@app.route("/items")
@login_required
def items_list():
    """Read: List all products/items with optional search and category filters."""
    search = request.args.get("search", "").strip()
    category_filter = request.args.get("category", "").strip()
    items = get_all_products(search=search, category_filter=category_filter)
    return render_template(
        "items/index.html",
        items=items,
        search_query=search,
        category_filter=category_filter,
    )


@app.route("/items/new", methods=["GET", "POST"])
@login_required
def items_create():
    """Create: Add a new catalog item directly to the database."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        sku = request.form.get("sku", "").strip()
        category = request.form.get("category", "Electronics")
        try:
            price = float(request.form.get("price", 0.0))
            stock = int(request.form.get("stock", 0))
            rating = float(request.form.get("rating", 5.0))
        except ValueError:
            flash("Invalid numeric value provided for price, stock, or rating.", "danger")
            return render_template("items/form.html", item=None)

        if not name or not sku:
            flash("Product name and SKU are required.", "danger")
            return render_template("items/form.html", item=None)

        try:
            item_id = create_product(name, sku, category, price, stock, rating)
            flash(f"Item '{name}' (SKU: {sku}) added successfully to {Config.DB_TYPE.upper()} database!", "success")
            return redirect(url_for("items_list"))
        except Exception as e:
            flash(f"Database error creating item: {str(e)}", "danger")

    return render_template("items/form.html", item=None)


@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def items_edit(item_id):
    """Update: Modify an existing item in the catalog database."""
    item = get_product_by_id(item_id)
    if not item:
        flash("Item not found.", "warning")
        return redirect(url_for("items_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        sku = request.form.get("sku", "").strip()
        category = request.form.get("category", "Electronics")
        try:
            price = float(request.form.get("price", 0.0))
            stock = int(request.form.get("stock", 0))
            rating = float(request.form.get("rating", 5.0))
        except ValueError:
            flash("Invalid numeric value provided.", "danger")
            return render_template("items/form.html", item=item)

        try:
            update_product(item_id, name, sku, category, price, stock, rating)
            flash(f"Item #{item_id} ('{name}') updated successfully!", "success")
            return redirect(url_for("items_list"))
        except Exception as e:
            flash(f"Error updating item: {str(e)}", "danger")

    return render_template("items/form.html", item=item)


@app.route("/items/<int:item_id>/delete", methods=["POST"])
@login_required
def items_delete(item_id):
    """Delete: Remove an item from the catalog database."""
    try:
        delete_product(item_id)
        flash(f"Item #{item_id} deleted successfully from database.", "info")
    except Exception as e:
        flash(f"Error deleting item: {str(e)}", "danger")
    return redirect(url_for("items_list"))


# ==============================================================================
# TELEMETRY & SYSTEM MONITORING ROUTES
# ==============================================================================

@app.route("/statistics")
@login_required
def statistics():
    """Dedicated window showing real-time dummy CPU usage and database telemetry."""
    stats = get_system_statistics()
    db_info = Config.get_db_info()
    return render_template(
        "statistics.html",
        stats=stats,
        db_info=db_info,
    )


@app.route("/database/seed", methods=["GET", "POST"])
@login_required
def database_seed():
    """Endpoint to trigger database connection test and dummy data seeding."""
    scale = request.args.get("scale", "standard")
    if request.method == "POST":
        scale = request.form.get("scale", "standard")

    try:
        result = seed_dummy_data(scale=scale)
        flash(
            f"Database successfully re-seeded ({scale} scale) directly into {Config.DB_TYPE.upper()} ({Config.DB_NAME})! "
            f"Created {result['users_count']} users, {result['orders_count']} orders, and {result['products_count']} products.",
            "success",
        )
    except Exception as e:
        flash(f"Error seeding database: {str(e)}", "danger")

    referer = request.referrer
    if referer and ("statistics" in referer or "dashboard" in referer):
        return redirect(referer)
    return redirect(url_for("statistics"))


@app.route("/database/test-connection")
@login_required
def database_test():
    """Tests the database connection and returns diagnostic latency and health."""
    diagnostics = test_db_connection()
    return jsonify(diagnostics)


@app.route("/api/system-stats")
@login_required
def api_system_stats():
    """JSON API endpoint providing real-time CPU, memory, and database telemetry."""
    stats = get_system_statistics()
    return jsonify(stats)


@app.route("/api/metrics")
@login_required
def api_metrics():
    """API endpoint providing current dashboard metrics in JSON format."""
    data = get_dashboard_data()
    return jsonify(data)


@app.route("/health")
def health():
    """Health check endpoint used by deployment/monitoring tools (Ansible/Docker/LoadBalancers)."""
    db_status = "ok"
    try:
        diag = test_db_connection()
        if diag["status"] != "ok":
            db_status = diag["error"] or "connection failed"
    except Exception as e:
        db_status = f"error: {str(e)}"

    status_code = 200 if db_status == "ok" else 500
    return jsonify({
        "status": "healthy" if db_status == "ok" else "unhealthy",
        "app_name": Config.APP_NAME,
        "environment": Config.APP_ENV,
        "database_type": Config.DB_TYPE,
        "database_name": Config.DB_NAME,
        "database_status": db_status,
    }), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
