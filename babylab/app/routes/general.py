"""Genera routes."""

import os
import datetime
from collections import OrderedDict
import requests
import pandas as pd
from flask import redirect, flash, render_template, url_for, request, send_file
from babylab.src import api, utils
from babylab.app import config as conf


def prepare_studies(records: api.Records, data_dict: dict, study: str = None):
    """Prepare appointments page.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        study (str, optional): Study to filter for. Defaults to None.

    Returns:
        dict: Parameters for the participants endpoint.
    """  # pylint: disable=line-too-long
    df = utils.get_appointments_table(records, data_dict=data_dict, study=study)
    classes = "table table-hover table-responsives"
    df["appointment_id"] = [utils.format_apt_id(i) for i in df["appointment_id"]]
    df["record_id"] = [utils.format_ppt_id(i) for i in df.index]
    df["modify_button"] = [
        utils.format_modify_button(p, a) for p, a in zip(df.index, df["appointment_id"])
    ]

    df = df[
        [
            "appointment_id",
            "record_id",
            "study",
            "status",
            "date",
            "date_created",
            "date_updated",
            "taxi_address",
            "taxi_isbooked",
            "comments",
            "modify_button",
        ]
    ]
    df = df.sort_values("date", ascending=False)

    df = df.rename(
        columns={
            "appointment_id": "Appointment",
            "record_id": "Participant",
            "study": "Study",
            "status": "Appointment status",
            "date": "Date",
            "date_created": "Made on the",
            "date_updated": "Last updated",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "comments": "Comments",
            "modify_button": "",
        }
    )

    table = df.to_html(
        classes=f'{classes}" id = "apttable',
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    date = df["Date"].value_counts().to_dict()
    date = OrderedDict(sorted(date.items()))
    for idx, (k, v) in enumerate(date.items()):
        if idx > 0:
            date[k] = v + list(date.values())[idx - 1]

    return {
        "n_apts": df.shape[0],
        "date_labels": list(date.keys()),
        "date_values": list(date.values()),
        "table": table,
    }


def get_year_weeks(year: int):
    """Get week numbers of the year"""
    date_first = datetime.date(year, 1, 1)
    date_first += datetime.timedelta(days=6 - date_first.weekday())
    while date_first.year == year:
        yield date_first
        date_first += datetime.timedelta(days=7)


def get_week_number(date: datetime.date):
    """Get current week number"""
    weeks = {}
    for wn, d in enumerate(get_year_weeks(date.year)):
        weeks[wn + 1] = [
            (d + datetime.timedelta(days=k)).isoformat() for k in range(0, 7)
        ]
    for k, v in weeks.items():
        if datetime.datetime.strftime(date, "%Y-%m-%d") in v:
            return k
    return None


def prepare_dashboard(records: api.Records = None, data_dict: dict = None) -> dict:
    """Prepare data for dashboard.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict, optional): Data dictionary as returned by ``api.get_data_dictionary``. Defaults to None.

    Returns:
        dict: Parameters for the dashboard endpoint.
    """  # pylint: disable=line-too-long
    ppts = utils.get_participants_table(records, data_dict=data_dict)
    apts = utils.get_appointments_table(records, data_dict=data_dict)
    quest = utils.get_questionnaires_table(records, data_dict=data_dict)
    ppts["age_days"] = round(
        ppts["age_now_days"] + (ppts["age_now_months"] * 30.437), None
    ).astype(int)
    age_bins = list(range(0, max(ppts["age_days"]), 15))
    labels = [f"{int(a // 30)}:{int(a % 30)}" for a in age_bins]
    ppts["age_days_binned"] = pd.cut(
        ppts["age_days"], bins=age_bins, labels=labels[:-1]
    )

    current_week = get_week_number(datetime.datetime.today())
    n_ppts_week = sum(
        get_week_number(
            datetime.datetime.strptime(v.data["date_created"], "%Y-%m-%d %H:%M:%S")
        )
        == current_week
        for v in records.participants.records.values()
    )
    n_apts_week = sum(
        get_week_number(
            datetime.datetime.strptime(v.data["date_created"], "%Y-%m-%d %H:%M:%S")
        )
        == current_week
        for v in records.appointments.records.values()
    )

    variables = {
        "age_dist": utils.count_col(ppts, "age_days_binned"),
        "sex_dist": utils.count_col(ppts, "sex", values_sort=True),
        "source_dist": utils.count_col(ppts, "source", values_sort=True),
        "ppts_date_created": utils.count_col(ppts, "date_created", cumulative=True),
        "apts_date_created": utils.count_col(apts, "date_created", cumulative=True),
        "status_dist": utils.count_col(apts, "status", values_sort=True),
        "lang1_dist": utils.count_col(
            quest, "lang1", values_sort=True, missing_label="None"
        ),
        "lang2_dist": utils.count_col(
            quest, "lang2", values_sort=True, missing_label="None"
        ),
    }

    return {
        "n_ppts": ppts.shape[0],
        "n_apts": apts.shape[0],
        "n_ppts_week": n_ppts_week,
        "n_apts_week": n_apts_week,
        "age_dist_labels": list(variables["age_dist"].keys()),
        "age_dist_values": list(variables["age_dist"].values()),
        "sex_dist_labels": list(variables["sex_dist"].keys()),
        "sex_dist_values": list(variables["sex_dist"].values()),
        "source_dist_labels": list(variables["source_dist"].keys()),
        "source_dist_values": list(variables["source_dist"].values()),
        "ppts_date_created_labels": list(variables["ppts_date_created"].keys()),
        "ppts_date_created_values": list(variables["ppts_date_created"].values()),
        "apts_date_created_labels": list(variables["apts_date_created"].keys()),
        "apts_date_created_values": list(variables["apts_date_created"].values()),
        "status_dist_labels": list(variables["status_dist"].keys()),
        "status_dist_values": list(variables["status_dist"].values()),
        "lang1_dist_labels": list(variables["lang1_dist"].keys())[:24],
        "lang1_dist_values": list(variables["lang1_dist"].values())[:24],
        "lang2_dist_labels": list(variables["lang2_dist"].keys())[:24],
        "lang2_dist_values": list(variables["lang2_dist"].values())[:24],
    }


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
            token = finput["apiToken"]
            app.config["API_KEY"] = token
            app.config["EMAIL"] = finput["email"]
            try:
                redcap_version = api.get_redcap_version(token=token)
                if redcap_version:
                    flash("Logged in.", "success")
                    app.config["RECORDS"] = api.Records(token=token)
                    return render_template("index.html", redcap_version=redcap_version)
                flash("Incorrect token", "error")
            except ValueError as e:
                flash(f"Incorrect token: {e}", "error")
        return render_template("index.html", redcap_version=redcap_version)

    @app.route("/dashboard")
    @conf.token_required
    def dashboard():
        """Dashboard page"""
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
        data = prepare_dashboard(app.config["RECORDS"], data_dict)
        return render_template("dashboard.html", data=data)

    @app.route("/calendar")
    @conf.token_required
    def calendar(data_dict: dict = None):
        """Calendar page"""
        token = app.config["API_KEY"]
        if data_dict is None:
            data_dict = api.get_data_dict(token=token)
        if app.config["RECORDS"] is None:
            app.config["RECORDS"] = api.Records(token)
        records = app.config["RECORDS"]
        events = []
        fmt_str = "%Y-%m-%d %H:%M"
        cols = [
            "#36a2eb",
            "#ff6384",
            "#ff9f40",
            "#4bc0c0",
            "#9966ff",
            "#ffcd56",
            "#c9cbcf",
        ]
        ecols = dict(zip(data_dict["appointment_study"].values(), cols))
        scols = {
            "Scheduled": "black",
            "Confirmed": "black",
            "Successful": "black",
            "Cancelled - Reschedule": "red",
            "No show": "grey",
            "Cancelled - Drop": "grey",
        }
        for apt in list(records.appointments.records.values()):
            data = utils.replace_labels(apt.data, data_dict)
            start = datetime.datetime.strptime(data["date"], fmt_str)
            end = start + datetime.timedelta(minutes=60)

            events.append(
                {
                    "title": f"{data['status']} | {data['id']}",
                    "start": datetime.datetime.strftime(start, fmt_str),
                    "end": datetime.datetime.strftime(end, fmt_str),
                    "timeStart": datetime.datetime.strftime(start, "%H:%M"),
                    "timeEnd": datetime.datetime.strftime(end, "%H:%M"),
                    "groupID": data["study"],
                    "display": "block",
                    "location": "Barcelona",
                    "url": f"/appointments/{data['id']}",
                    "borderColor": "white",
                    "textColor": scols[data["status"]],
                    "backgroundColor": ecols[data["study"]],
                },
            )
        data = {"events": events, "colors_dict": ecols}

        return render_template("calendar.html", data=data, data_dict=data_dict)

    @app.route("/studies", methods=["GET", "POST"])
    @conf.token_required
    def studies(selected_study: str = None, data: dict = None):
        """Studies page"""
        token = app.config["API_KEY"]
        data_dict = api.get_data_dict(token=token)

        if request.method == "POST":
            finput = request.form
            selected_study = finput["inputStudy"]
            data = prepare_studies(
                app.config["RECORDS"], data_dict=data_dict, study=selected_study
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
