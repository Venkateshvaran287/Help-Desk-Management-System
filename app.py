from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Python list is used for ticket storage.
# Note: tickets are temporary and reset when the app restarts.
ticket_details = []


def find_ticket(ticket_id):
    for ticket in ticket_details:
        if ticket["ticket id"] == ticket_id:
            return ticket
    return None


@app.route("/")
def home():
    total = len(ticket_details)
    open_count = sum(t["status"] == "open" for t in ticket_details)
    progress_count = sum(t["status"] == "in progress" for t in ticket_details)
    closed_count = sum(t["status"] == "closed" for t in ticket_details)
    high_count = sum(t["priority"] == "high" for t in ticket_details)
    medium_count = sum(t["priority"] == "medium" for t in ticket_details)
    low_count = sum(t["priority"] == "low" for t in ticket_details)

    stats = {
        "total": total,
        "open": open_count,
        "progress": progress_count,
        "closed": closed_count,
        "high": high_count,
        "medium": medium_count,
        "low": low_count,
    }
    return render_template("index.html", tickets=ticket_details, stats=stats)


@app.route("/create", methods=["POST"])
def create_ticket():
    try:
        ticket_id = int(request.form.get("ticket_id", "").strip())
    except ValueError:
        flash("Ticket ID must be a number.", "error")
        return redirect(url_for("home"))

    if find_ticket(ticket_id):
        flash("Ticket ID already exists. Please use a unique ID.", "error")
        return redirect(url_for("home"))

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    problem = request.form.get("problem", "").strip()
    priority = request.form.get("priority", "").lower()
    status = request.form.get("status", "").lower()

    if not all([name, category, problem]):
        flash("Please complete all ticket details.", "error")
        return redirect(url_for("home"))
    if priority not in ["low", "medium", "high"]:
        flash("Please select a valid priority.", "error")
        return redirect(url_for("home"))
    if status not in ["open", "in progress", "closed"]:
        flash("Please select a valid status.", "error")
        return redirect(url_for("home"))

    ticket_details.append({
        "ticket id": ticket_id,
        "employee name": name,
        "category": category,
        "problem": problem,
        "priority": priority,
        "status": status,
    })
    flash(f"Ticket #{ticket_id} created successfully.", "success")
    return redirect(url_for("home"))


@app.route("/search")
def search_ticket():
    query = request.args.get("ticket_id", "").strip()
    ticket = None
    if query:
        try:
            ticket = find_ticket(int(query))
        except ValueError:
            flash("Enter a numeric Ticket ID to search.", "error")
    if query and ticket is None:
        flash("Ticket not found.", "error")
    return render_template("search.html", ticket=ticket, query=query)


@app.route("/update/<int:ticket_id>", methods=["GET", "POST"])
def update_ticket(ticket_id):
    ticket = find_ticket(ticket_id)
    if ticket is None:
        flash("Ticket not found.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        status = request.form.get("status", "").lower()
        priority = request.form.get("priority", "").lower()
        problem = request.form.get("problem", "").strip()

        if status not in ["open", "in progress", "closed"]:
            flash("Select a valid status.", "error")
            return redirect(url_for("update_ticket", ticket_id=ticket_id))
        if priority not in ["low", "medium", "high"]:
            flash("Select a valid priority.", "error")
            return redirect(url_for("update_ticket", ticket_id=ticket_id))
        if not problem:
            flash("Problem description cannot be empty.", "error")
            return redirect(url_for("update_ticket", ticket_id=ticket_id))

        ticket["status"] = status
        ticket["priority"] = priority
        ticket["problem"] = problem
        flash(f"Ticket #{ticket_id} updated successfully.", "success")
        return redirect(url_for("home"))

    return render_template("edit.html", ticket=ticket)


@app.route("/delete/<int:ticket_id>", methods=["POST"])
def delete_ticket(ticket_id):
    ticket = find_ticket(ticket_id)
    if ticket is None:
        flash("Ticket not found.", "error")
    else:
        ticket_details.remove(ticket)
        flash(f"Ticket #{ticket_id} deleted successfully.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
