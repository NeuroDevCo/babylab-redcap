"""Genera routes."""

import os
import datetime
import requests
from flask import redirect, flash, render_template, url_for, request, send_file
from babylab.src import api, utils
from babylab.app import config as conf


def general_routes(app):
    """General routes."""

    @app.errorhandler(404)
    def error_404(error):
        """Error 404 page."""
        return render_template("404.html", error=error), 404

    @app.errorhandler(requests.exceptions.ReadTimeout)
    def error_443(error):
        """Error 403 page."""
        return render_template("443.html", error=error), 443

    @app.route("/", methods=["GET", "POST"])
    def index():
        """Index page"""
        redcap_version = api.get_redcap_version(token=app.config["API_KEY"])
        if request.method == "POST":
            finput = request.form
            app.config["API_KEY"] = finput["apiToken"]
            app.config["EMAIL"] = finput["email"]
            try:
                redcap_version = api.get_redcap_version(token=app.config["API_KEY"])
                if redcap_version:
                    flash("Logged in.", "success")
                    return render_template("index.html", redcap_version=redcap_version)
                flash("Incorrect token", "error")
            except ValueError as e:
                flash(f"Incorrect token: {e}", "error")
        return render_template("index.html", redcap_version=redcap_version)

    @app.route("/dashboard")
    @conf.token_required
    def dashboard():
        """Dashboard page"""
        records = conf.get_records_or_index(token=app.config["API_KEY"])
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
        data = utils.prepare_dashboard(records, data_dict)
        return render_template("dashboard.html", data=data)

    @app.route("/studies", methods=["GET", "POST"])
    @conf.token_required
    def studies(
        selected_study: str = None,
        data: dict = None,
    ):
        """Studies page"""
        token = app.config["API_KEY"]
        data_dict = api.get_data_dict(token=token)

        if request.method == "POST":
            finput = request.form
            selected_study = finput["inputStudy"]
            records = conf.get_records_or_index(token)
            data = utils.prepare_studies(
                records, data_dict=data_dict, study=selected_study
            )

            return render_template(
                "studies.html",
                data_dict=data_dict,
                selected_study=selected_study,
                data=data,
            )
        return render_template("studies.html", data_dict=data_dict, data=data)

    @app.route("/other", methods=["GET", "POST"])
    @conf.token_required
    def other():
        """Other pages"""
        fname = datetime.datetime.strftime(
            datetime.datetime.now(), "backup_%Y-%m-%d-%H-%M.zip"
        )
        if request.method == "post":
            backup_file = api.redcap_backup(
                dirpath=os.path.join("temp", fname), token=app.config["API_KEY"]
            )
            return send_file(
                backup_file,
                as_attachment=True,
            )
        return render_template(
            "other.html",
        )

    @app.route("/download_backup", methods=["GET", "POST"])
    @conf.token_required
    def download_backup():
        """Download backup"""
        utils.clean_tmp("tmp")
        utils.clean_tmp("../tmp")
        backup_file = api.redcap_backup(dirpath="/tmp", token=app.config["API_KEY"])
        return send_file(
            backup_file,
            as_attachment=False,
        )

    @app.route("/logout", methods=["GET", "POST"])
    @conf.token_required
    def logout():
        """Log out."""
        app.config["API_KEY"] = "BADTOKEN"
        flash("You have logged out.", category="error")
        return redirect(url_for("index"))
