from flask import Blueprint, redirect, render_template, request, url_for

from ..db import get_db
from ..utils import get_current_user, login_required, onboarding_required

bp = Blueprint("checklist", __name__, url_prefix="/checklist")


@bp.route("/", methods=("GET", "POST"))
@login_required
@onboarding_required
def lista():
    db = get_db()
    user = get_current_user()

    if request.method == "POST":
        item_id = int(request.form["item_id"])
        checked = 1 if request.form.get("checked") == "1" else 0
        existing = db.execute(
            "SELECT 1 FROM user_checklist WHERE user_id = ? AND item_id = ?", (user["id"], item_id)
        ).fetchone()
        if existing:
            db.execute(
                "UPDATE user_checklist SET checked = ? WHERE user_id = ? AND item_id = ?",
                (checked, user["id"], item_id),
            )
        else:
            db.execute(
                "INSERT INTO user_checklist (user_id, item_id, checked) VALUES (?, ?, ?)",
                (user["id"], item_id, checked),
            )
        db.commit()
        return redirect(url_for("checklist.lista"))

    items = db.execute("SELECT * FROM checklist_template ORDER BY ordine").fetchall()
    checked_ids = {
        r["item_id"]
        for r in db.execute(
            "SELECT item_id FROM user_checklist WHERE user_id = ? AND checked = 1", (user["id"],)
        ).fetchall()
    }
    return render_template("checklist/lista.html", items=items, checked_ids=checked_ids)
