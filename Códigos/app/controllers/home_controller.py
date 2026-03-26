from flask import Blueprint

from app.views.dashboard_view import render_dashboard
from app.views.home_view import render_home

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def home():
    context = {"title": "Secretaria Escolar DF"}
    return render_home(context)


@home_blueprint.route("/dashboard", methods=["GET"])
def dashboard():
    context = {"title": "Dashboard da Secretaria"}
    return render_dashboard(context)
