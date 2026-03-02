from flask import Blueprint, jsonify, render_template


api_bp = Blueprint("api", __name__)


@api_bp.route("/species")
def get_species():
    return render_template("species.html")


@api_bp.route("/api/items/<int:item_id>")
def get_item(item_id: int):
    return jsonify(
        {
            "item": {
                "id": item_id,
                "name": f"Sample Item {item_id}",
                "value": item_id * 100,
            },
            "timestamp": "2024-01-01T00:00:00Z",
        }
    )
