"""Genera routes."""

import os
from collections import OrderedDict
from datetime import datetime, timedelta
import requests
import pandas as pd
from flask import redirect, flash, session, render_template, url_for, request, send_file
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
    apts = utils.get_apt_table(records, data_dict=data_dict, study=study)
    ppts = utils.get_ppt_table(records, data_dict=data_dict, study=study)
    quest = utils.get_que_table(records, data_dict=data_dict)
    ppts["age_days"] = round(
        ppts["age_now_days"] + (ppts["age_now_months"] * 30.437), None
    ).astype(int)
    age_bins = list(range(0, max(ppts["age_days"]), 15))
    labels = [f"{int(a // 30)}:{int(a % 30)}" for a in age_bins]
    ppts["age_days_binned"] = pd.cut(
        ppts["age_days"],
        bins=age_bins,
        labels=labels[:-1],
        include_lowest=True,
    )
    classes = "table table-hover table-responsives"
    apts["modify_button"] = [
        utils.fmt_modify_button(p, a)
        for p, a in zip(apts.index, apts["appointment_id"])
    ]
    apts["appointment_id"] = [utils.fmt_apt_id(i) for i in apts["appointment_id"]]
    apts["record_id"] = [utils.fmt_ppt_id(i) for i in apts.index]
    apts = apts[
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
    apts = apts.sort_values("date", ascending=False)
    age_dist = {}
    for k, v in utils.count_col(ppts, "age_days_binned").items():
        months = k.split(":")[0]
        months = "0" + months if len(months) == 1 else months
        age_dist[months + ":" + k.split(":")[1]] = v

    variables = {
        "age_dist": dict(sorted(age_dist.items())),
        "sex_dist": utils.count_col(ppts, "sex", values_sort=True),
        "status_dist": utils.count_col(apts, "status", values_sort=True),
        "lang1_dist": utils.count_col(
            quest, "lang1", values_sort=True, missing_label="None"
        ),
        "lang2_dist": utils.count_col(
            quest, "lang2", values_sort=True, missing_label="None"
        ),
    }

    apts["status"] = [utils.fmt_apt_status(s) for s in apts["status"]]
    apts = apts.rename(
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
    table = utils.replace_labels(apts, data_dict)
    table = table.to_html(
        classes=f'{classes}" id = "apttable',
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    ts = apts["Date"].value_counts().to_dict()
    ts = OrderedDict(sorted(ts.items()))
    for idx, (k, v) in enumerate(ts.items()):
        if idx > 0:
            ts[k] = v + list(ts.values())[idx - 1]
    n_apts_week = {
        x: utils.get_weekly_apts(
            records,
            data_dict=data_dict,
            study=data_dict["appointment_study"][x],
        )
        for x in data_dict["appointment_study"]
    }

    n_apts_week_succ = {
        x: utils.get_weekly_apts(
            records,
            data_dict=data_dict,
            study=data_dict["appointment_study"][x],
            status=["Successful", "Successful - Good"],
        )
        for x in data_dict["appointment_study"]
    }
    n_apts_week_canc = {
        x: utils.get_weekly_apts(
            records,
            data_dict=data_dict,
            study=data_dict["appointment_study"][x],
            status=["Cancelled - Reschedule", "Cancelled - Drop", "No show"],
        )
        for x in data_dict["appointment_study"]
    }
    return {
        "n_apts": apts.shape[0],
        "n_apts_week": n_apts_week[study],
        "n_apts_succ": sum(
            v
            for k, v in variables["status_dist"].items()
            if k in ["Successful", "Successful - Good"]
        ),
        "n_apts_week_succ": n_apts_week_succ[study],
        "n_apts_canc": sum(
            v
            for k, v in variables["status_dist"].items()
            if k in ["Cancelled - Reschedule", "Cancelled - Drop", "No show"]
        ),
        "n_apts_week_canc": n_apts_week_canc[study],
        "date_labels": [str(d) for d in ts.keys()],
        "date_values": [str(d) for d in ts.values()],
        "status_dist_labels": list(variables["status_dist"].keys()),
        "status_dist_values": list(variables["status_dist"].values()),
        "age_dist_labels": list(variables["age_dist"].keys()),
        "age_dist_values": list(variables["age_dist"].values()),
        "sex_dist_labels": list(variables["sex_dist"].keys()),
        "sex_dist_values": list(variables["sex_dist"].values()),
        "lang1_dist_labels": list(variables["lang1_dist"].keys())[:24],
        "lang1_dist_values": list(variables["lang1_dist"].values())[:24],
        "lang2_dist_labels": list(variables["lang2_dist"].keys())[:24],
        "lang2_dist_values": list(variables["lang2_dist"].values())[:24],
        "table": table,
    }


def prepare_dashboard(records: api.Records = None, data_dict: dict = None) -> dict:
    """Prepare data for dashboard.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict, optional): Data dictionary as returned by ``api.get_data_dictionary``. Defaults to None.

    Returns:
        dict: Parameters for the dashboard endpoint.
    """  # pylint: disable=line-too-long
    ppts = utils.get_ppt_table(records, data_dict=data_dict)
    apts = utils.get_apt_table(records, data_dict=data_dict)
    quest = utils.get_que_table(records, data_dict=data_dict)
    ppts["age_days"] = round(
        ppts["age_now_days"] + (ppts["age_now_months"] * 30.437), None
    ).astype(int)
    age_bins = list(range(0, max(ppts["age_days"]), 15))
    labels = [f"{int(a // 30)}:{int(a % 30)}" for a in age_bins]
    ppts["age_days_binned"] = pd.cut(
        ppts["age_days"],
        bins=age_bins,
        labels=labels[:-1],
        include_lowest=True,
    )
    n_ppts_week = sum(
        utils.get_week_n(v.data["date_created"]) == utils.get_week_n(datetime.today())
        for v in records.participants.records.values()
    )
    n_apts_week = sum(
        utils.get_week_n(v.data["date_created"]) == utils.get_week_n(datetime.today())
        for v in records.appointments.records.values()
    )

    age_dist = {}
    for k, v in utils.count_col(ppts, "age_days_binned").items():
        months = k.split(":")[0]
        months = "0" + months if len(months) == 1 else months
        age_dist[months + ":" + k.split(":")[1]] = v

    variables = {
        "age_dist": dict(sorted(age_dist.items())),
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

    for var in ["ppts_date_created", "apts_date_created"]:
        variables[var] = {str(k): v for k, v in variables[var].items()}

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

    @app.route("/setlang")
    def setlang():
        """Language selector."""
        lang = request.args.get("lang", "en")
        session["lang"] = lang
        return redirect(request.referrer)

    @app.errorhandler(404)
    def error_404(error):
        """Error 404 page."""
        return render_template("404.html", error=error), 404

    @app.errorhandler(requests.exceptions.ReadTimeout)
    def error_443(error):
        """Error 403 page."""
        return render_template("443.html", error=error), 443

    @app.errorhandler(500)
    def error_500(error):
        """Error 500 page."""
        return render_template("500.html", error=error), 500

    @app.route("/", methods=["GET", "POST"])
    def index():
        """Index page"""
        token = app.config["API_KEY"]
        version = api.get_redcap_version(token=token)
        if request.method == "POST":
            finput = request.form
            token = finput["apiToken"]
            app.config["API_KEY"] = token
            try:
                version = api.get_redcap_version(token=token)
                if version:
                    flash("Logged in.", "success")
                    app.config["RECORDS"] = api.Records(token=token)
                    return render_template("index.html", redcap_version=version)
                flash("Incorrect token", "error")
            except ValueError as e:
                flash(f"Incorrect token: {e}", "error")

        return render_template(
            "index.html", redcap_version=version, current_locale=conf.get_locale()
        )

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
            "Successful - Good": "black",
            "Cancelled - Reschedule": "red",
            "No show": "grey",
            "Cancelled - Drop": "grey",
        }
        for apt in list(records.appointments.records.values()):
            data = utils.replace_labels(apt.data, data_dict)
            start = data["date"]
            end = start + timedelta(minutes=60)

            events.append(
                {
                    "title": f"{data['status']} | {data['id']}",
                    "start": datetime.strftime(start, fmt_str),
                    "end": datetime.strftime(end, fmt_str),
                    "timeStart": datetime.strftime(start, "%H:%M"),
                    "timeEnd": datetime.strftime(end, "%H:%M"),
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
    def studies(study: str = None, data: dict = None):
        """Studies page"""
        token = app.config["API_KEY"]
        recs = app.config["RECORDS"]
        data_dict = api.get_data_dict(token=token)

        if request.method == "POST":
            finput = request.form
            study = finput["inputStudy"]
            data = prepare_studies(recs, data_dict=data_dict, study=study)
            return render_template(
                "studies.html", data_dict=data_dict, selected_study=study, data=data
            )
        return render_template("studies.html", data_dict=data_dict, data=data)

    @app.route("/other", methods=["GET", "POST"])
    @conf.token_required
    def other():
        """Other pages"""
        token = app.config["API_KEY"]
        timestamp = datetime.now()
        fn_fmt = "backup_%Y-%m-%d-%H-%M.zip"
        fn = datetime.strftime(timestamp, fn_fmt)
        if request.method == "post":
            path = os.path.join("temp", fn)
            backup_file = api.redcap_backup(dirpath=path, token=token)
            return send_file(backup_file, as_attachment=True)
        return render_template("other.html")

    @app.route("/download_backup", methods=["GET", "POST"])
    @conf.token_required
    def download_backup():
        """Download backup"""
        token = app.config["API_KEY"]
        utils.clean_tmp("tmp")
        utils.clean_tmp("../tmp")
        backup_file = api.redcap_backup(dirpath="/tmp", token=token)
        return send_file(backup_file, as_attachment=False)

    @app.route("/logout", methods=["GET", "POST"])
    @conf.token_required
    def logout():
        """Log out."""
        app.config["API_KEY"] = "BADTOKEN"
        flash("You have logged out.", category="error")
        return redirect(url_for("index"))

    @app.route("/age_calculator", methods=["GET", "POST"])
    def age_calculator():
        """Age calculator."""
        return render_template("age_calculator.html")
