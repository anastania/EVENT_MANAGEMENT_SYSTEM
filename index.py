from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "super_secret_key"

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="event_management",
        user="postgres",
        password="root"
    )

@app.route("/")
def index():
    # Récupérer le numéro de page depuis les paramètres de requête, par défaut 1
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Nombre d'événements par page
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtenir le nombre total d'événements
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]
    
    # Calculer le nombre total de pages
    total_pages = (total_events + per_page - 1) // per_page
        # Calculer l'offset pour la pagination
    offset = (page - 1) * per_page
    
    # Modifier la requête pour inclure la pagination
    cur.execute("""
        SELECT e.id, e.name, e.date, e.location, e.description, o.name AS organizer
        FROM events e
        JOIN organizers o ON e.organizer_id = o.id
        ORDER BY e.date
        LIMIT %s OFFSET %s;
    """, (per_page, offset))
    
    events = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template(
        "index.html",
        events=events,
        page=page,
        total_pages=total_pages
    )

@app.route("/events")
def events():
    # Récupérer le numéro de page depuis les paramètres de l'URL
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Nombre d'événements par page

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtenir le nombre total d'événements
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]
    
    # Calculer le nombre total de pages
    total_pages = (total_events + per_page - 1) // per_page
    
    # Calculer l'offset pour la pagination
    offset = (page - 1) * per_page
    
    # Récupérer les événements pour la page courante
    cur.execute("""
        SELECT e.*, o.name as organizer_name 
        FROM events e 
        LEFT JOIN organizers o ON e.organizer_id = o.id 
        ORDER BY e.date DESC 
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    
    events = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "events.html",
        events=events,
        page=page,
        total_pages=total_pages
    )

@app.route("/events/<int:event_id>")
def view_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Récupérer les détails de l'événement
    cur.execute("""
        SELECT e.*, o.name as organizer_name 
        FROM events e
        LEFT JOIN organizers o ON e.organizer_id = o.id 
        WHERE e.id = %s
    """, (event_id,))
    event = cur.fetchone()
    
    # Récupérer les participants inscrits
    cur.execute("""
        SELECT a.* FROM attendees a
        JOIN tickets t ON a.id = t.attendee_id
        WHERE t.event_id = %s
        ORDER BY a.name
    """, (event_id,))
    registered_attendees = cur.fetchall()
    
    cur.close()
    conn.close()
    
    if event is None:
        flash("⚠️ Événement non trouvé!", "danger")
        return redirect(url_for("events"))
        
    return render_template(
        "view_event.html", 
        event=event,
        registered_attendees=registered_attendees
    )

@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM organizers ORDER BY name;")
    organizers = cur.fetchall()
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]
        description = request.form["description"]
        organizer_id = request.form["organizer_id"]
        if not name or not date or not location or not organizer_id:
            flash("⚠️ All fields except description are required!", "danger")
            return redirect(url_for("create_event"))
        cur.execute(
            "INSERT INTO events (name, date, location, description, organizer_id) VALUES (%s, %s, %s, %s, %s)",
            (name, date, location, description, organizer_id),
        )
        conn.commit()
        flash("✅ Event added successfully!", "success")
        return redirect(url_for("index"))
    cur.close()
    conn.close()
    return render_template("create_event.html", organizers=organizers)

@app.route("/events/delete/<int:event_id>")
def delete_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("🗑️ Event deleted!", "info")
    return redirect(url_for("index"))

@app.route("/events/update/<int:event_id>", methods=["GET", "POST"])
def update_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM organizers ORDER BY name;")
    organizers = cur.fetchall()
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]
        description = request.form["description"]
        organizer_id = request.form["organizer_id"]
        cur.execute(
            "UPDATE events SET name=%s, date=%s, location=%s, description=%s, organizer_id=%s WHERE id=%s",
            (name, date, location, description, organizer_id, event_id),
        )
        conn.commit()
        flash("✏️ Event updated!", "success")
        return redirect(url_for("index"))
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("edit_event.html", event=event, organizers=organizers)

@app.route("/organizers")
def organizers():
    # Récupérer le numéro de page depuis les paramètres de l'URL
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Nombre d'organisateurs par page

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtenir le nombre total d'organisateurs
    cur.execute("SELECT COUNT(*) FROM organizers")
    total_organizers = cur.fetchone()[0]
    
    # Calculer le nombre total de pages
    total_pages = (total_organizers + per_page - 1) // per_page
    
    # Calculer l'offset pour la pagination
    offset = (page - 1) * per_page
    
    # Récupérer les organisateurs pour la page courante avec le nombre d'événements
    cur.execute("""
        SELECT o.*, COUNT(e.id) as event_count
        FROM organizers o
        LEFT JOIN events e ON o.id = e.organizer_id
        GROUP BY o.id
        ORDER BY o.name ASC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    
    organizers = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "organizers.html",
        organizers=organizers,
        page=page,
        total_pages=total_pages
    )

@app.route("/create_organizer", methods=["GET", "POST"])
def create_organizer():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form.get("phone", "")  # phone est optionnel
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO organizers (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash("✅ Organisateur créé avec succès!", "success")
        return redirect(url_for("organizers"))
        
    return render_template("create_organizer.html")

@app.route("/organizers/update/<int:organizer_id>", methods=["GET", "POST"])
def update_organizer(organizer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form.get("phone")
        cur.execute(
            "UPDATE organizers SET name=%s, email=%s, phone=%s WHERE id=%s",
            (name, email, phone, organizer_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("✏️ Organizer updated!", "success")
        return redirect(url_for("organizers"))
    cur.execute("SELECT * FROM organizers WHERE id=%s", (organizer_id,))
    organizer = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("edit_organizer.html", organizer=organizer)

@app.route("/organizers/delete/<int:organizer_id>")
def delete_organizer(organizer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Vérifier si l'organisateur a des événements
    cur.execute("SELECT COUNT(*) FROM events WHERE organizer_id = %s", (organizer_id,))
    event_count = cur.fetchone()[0]
    
    if event_count > 0:
        flash("⚠️ Impossible de supprimer cet organisateur car il a des événements associés.", "danger")
    else:
        cur.execute("DELETE FROM organizers WHERE id = %s", (organizer_id,))
        conn.commit()
        flash("🗑️ Organisateur supprimé avec succès!", "success")
    
    cur.close()
    conn.close()
    return redirect(url_for("organizers"))

@app.route("/attendees")
def attendees():
    # Récupérer le numéro de page depuis les paramètres de l'URL
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Nombre de participants par page
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtenir le nombre total de participants
    cur.execute("SELECT COUNT(*) FROM attendees")
    total_attendees = cur.fetchone()[0]
    
    # Calculer le nombre total de pages
    total_pages = (total_attendees + per_page - 1) // per_page
    
    # Calculer l'offset pour la pagination
    offset = (page - 1) * per_page
    
    # Récupérer les participants pour la page courante avec le nombre d'événements
    cur.execute("""
        SELECT a.*, COUNT(t.event_id) as event_count
        FROM attendees a
        LEFT JOIN tickets t ON a.id = t.attendee_id
        GROUP BY a.id
        ORDER BY a.name ASC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    
    attendees = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "attendees.html",
        attendees=attendees,
        page=page,
        total_pages=total_pages
    )

@app.route("/create_attendee", methods=["GET", "POST"])
def create_attendee():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form.get("phone")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO attendees (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone),
        )
        conn.commit()
        conn.close()
        flash("✅ Attendee created successfully!", "success")
        return redirect(url_for("attendees"))
    return render_template("create_attendee.html")

@app.route("/attendees/update/<int:attendee_id>", methods=["GET", "POST"])
def update_attendee(attendee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form.get("phone")
        cur.execute(
            "UPDATE attendees SET name=%s, email=%s, phone=%s WHERE id=%s",
            (name, email, phone, attendee_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("✏️ Attendee updated!", "success")
        return redirect(url_for("attendees"))
    cur.execute("SELECT * FROM attendees WHERE id=%s", (attendee_id,))
    attendee = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("edit_attendee.html", attendee=attendee)

@app.route("/attendees/<int:attendee_id>")
def attendee_details(attendee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Récupérer les informations de l'participant
    cur.execute("""
        SELECT * FROM attendees 
        WHERE id = %s
    """, (attendee_id,))
    attendee = cur.fetchone()
    
    # Récupérer les événements auxquels l'participant est inscrit
    cur.execute("""
        SELECT e.* FROM events e
        JOIN tickets t ON e.id = t.event_id
        WHERE t.attendee_id = %s
        ORDER BY e.date
    """, (attendee_id,))
    registered_events = cur.fetchall()
    
    cur.close()
    conn.close()
    
    if attendee is None:
        flash("⚠️ Participant non trouvé!", "danger")
        return redirect(url_for("attendees"))
        
    return render_template(
        "attendee_details.html",
        attendee=attendee,
        registered_events=registered_events
    )

@app.route("/dashboard")
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()

    # Statistiques de base
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attendees")
    total_attendees = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM organizers")
    total_organizers = cur.fetchone()[0]

    # Événements par organisateur
    cur.execute("""
        SELECT o.name, COUNT(e.id)
        FROM organizers o
        LEFT JOIN events e ON o.id = e.organizer_id
        GROUP BY o.id, o.name
        ORDER BY o.name
    """)
    organizer_stats = cur.fetchall()
    organizer_names = [row[0] for row in organizer_stats] or []
    events_per_organizer = [row[1] for row in organizer_stats] or []

    # Top 5 événements populaires
    cur.execute("""
        SELECT e.name, COUNT(t.id)
        FROM events e
        LEFT JOIN tickets t ON e.id = t.event_id
        GROUP BY e.id, e.name
        ORDER BY COUNT(t.id) DESC
        LIMIT 5
    """)
    popular_events = cur.fetchall()
    popular_event_names = [row[0] for row in popular_events] or []
    popular_event_counts = [row[1] for row in popular_events] or []

    # Inscriptions par mois
    cur.execute("""
        SELECT TO_CHAR(date_trunc('month', e.date), 'Mon YYYY') as month,
               COUNT(DISTINCT t.attendee_id)
        FROM events e
        LEFT JOIN tickets t ON e.id = t.event_id
        WHERE e.date >= NOW() - INTERVAL '1 year'
        GROUP BY date_trunc('month', e.date)
        ORDER BY date_trunc('month', e.date)
    """)
    monthly_stats = cur.fetchall()
    months = [row[0] for row in monthly_stats] or []
    attendees_over_time = [row[1] for row in monthly_stats] or []

    cur.close()
    conn.close()

    return render_template(
        "stats.html",
        total_events=total_events,
        total_attendees=total_attendees,
        total_organizers=total_organizers,
        organizer_names=organizer_names,
        events_per_organizer=events_per_organizer,
        popular_event_names=popular_event_names,
        popular_event_counts=popular_event_counts,
        months=months,
        attendees_over_time=attendees_over_time
    )

@app.route("/register_event/<int:event_id>", methods=["GET", "POST"])
def register_event(event_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == "POST":
        attendee_id = request.form.get("attendee_id")
        try:
            cur.execute(
                "INSERT INTO tickets (event_id, attendee_id) VALUES (%s, %s)",
                (event_id, attendee_id)
            )
            conn.commit()
            flash("✅ Successfully registered for event!", "success")
        except psycopg2.IntegrityError:
            flash("⚠️ Already registered for this event!", "danger")
        return redirect(url_for("view_event", event_id=event_id))

    # Get event details
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()
    
    # Get all attendees not registered for this event
    cur.execute("""
        SELECT * FROM attendees 
        WHERE id NOT IN (
            SELECT attendee_id FROM tickets WHERE event_id = %s
        )
        ORDER BY name
    """, (event_id,))
    available_attendees = cur.fetchall()
    
    # Get registered attendees
    cur.execute("""
        SELECT a.* FROM attendees a
        JOIN tickets t ON a.id = t.attendee_id
        WHERE t.event_id = %s
        ORDER BY a.name
    """, (event_id,))
    registered_attendees = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template(
        "register_event.html",
        event=event,
        available_attendees=available_attendees,
        registered_attendees=registered_attendees
    )

@app.route("/unregister_event/<int:event_id>/<int:attendee_id>")
def unregister_event(event_id, attendee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tickets WHERE event_id = %s AND attendee_id = %s",
        (event_id, attendee_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    flash("🗑️ Successfully unregistered from event!", "info")
    return redirect(url_for("view_event", event_id=event_id))

@app.route("/attendees/delete/<int:attendee_id>", methods=["POST"])
def delete_attendee(attendee_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Vérifier si le participant est inscrit à des événements
    cur.execute("SELECT COUNT(*) FROM tickets WHERE attendee_id = %s", (attendee_id,))
    ticket_count = cur.fetchone()[0]
    
    if ticket_count > 0:
        flash("⚠️ Impossible de supprimer ce participant car il est inscrit à des événements.", "danger")
    else:
        cur.execute("DELETE FROM attendees WHERE id = %s", (attendee_id,))
        conn.commit()
        flash("🗑️ Participant supprimé avec succès!", "success")
    
    cur.close()
    conn.close()
    return redirect(url_for("attendees"))

if __name__ == "__main__":
    app.run(debug=True, port=5002)
