"""Appointments routes."""

import os
import datetime
import requests
from flask import flash, redirect, render_template, url_for, request
from babylab.src import api, utils
from babylab.app import config as conf


def prepare_appointments(
    records: api.Records, data_dict: dict = None, study: str = None, **kwargs
):
    """Prepare record ID page.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        study (str, optional): Study to filter for. Defaults to None.
        **kwargs: Extra arguments passed to ``get_participants_table``, ``get_appointments_table``, and ``get_questionnaires_table``

    Returns:
        dict: Parameters for the participants endpoint.
    """  # pylint: disable=line-too-long
    df = utils.get_appointments_table(
        records, data_dict=data_dict, study=study, **kwargs
    )
    classes = "table table-hover table-responsive"
    df["record_id"] = [utils.format_ppt_id(i) for i in df.index]
    df["modify_button"] = [
        utils.format_modify_button(p, a) for p, a in zip(df.index, df["appointment_id"])
    ]
    df["appointment_id"] = [utils.format_apt_id(i) for i in df["appointment_id"]]
    # df["status"] = [utils.format_status(s) for s in df["status"]]

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
    df = df.sort_values("date_updated", ascending=False)

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

    return {"table": table}


def appointments_routes(app):
    """Appointments routes."""

    @app.route("/appointments/")
    @conf.token_required
    def apt_all():
        """Appointments database"""
        token = app.config["API_KEY"]
        records = api.Records(token=token)
        data_dict = api.get_data_dict(token=token)
        data = prepare_appointments(records, data_dict=data_dict, n=20)
        return render_template(
            "apt_all.html",
            data=data,
            n_apt=len(records.appointments.records),
        )

    @app.route("/appointments/<string:apt_id>", methods=["GET", "POST"])
    @conf.token_required
    def apt(apt_id: str = None):
        """Show the record_id for that appointment"""
        token = app.config["API_KEY"]
        data_dict = api.get_data_dict(token=token)
        records = conf.get_records_or_index(token=token)
        data = records.appointments.records[apt_id].data
        data = utils.replace_labels(data, data_dict)
        participant = records.participants.records[data["record_id"]].data
        participant["age_now_months"] = str(participant["age_now_months"])
        participant["age_now_days"] = str(participant["age_now_days"])
        if request.method == "POST":
            try:
                ppt_id, apt_id = apt_id.split(":")
                api.delete_appointment(
                    data={"record_id": ppt_id, "redcap_repeat_instance": apt_id},
                    token=app.config["API_KEY"],
                )
                flash("Appointment deleted!", "success")
                return redirect(url_for("apt_all"))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return redirect(url_for("apt_all"))
        return render_template(
            "apt.html",
            apt_id=apt_id,
            ppt_id=data["record_id"],
            data=data,
            participant=participant,
        )

    @app.route("/participants/<string:ppt_id>/appointment_new", methods=["GET", "POST"])
    @conf.token_required
    def apt_new(ppt_id: str):
        """New appointment page"""
        token = app.config["API_KEY"]
        records = conf.get_records_or_index(token=token)
        data_dict = api.get_data_dict(token=token)
        if request.method == "POST":
            finput = request.form
            date_now = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"
            )
            data = {
                "record_id": finput["inputId"],
                "redcap_repeat_instance": "new",
                "redcap_repeat_instrument": "appointments",
                "appointment_study": finput["inputStudy"],
                "appointment_date_created": date_now,
                "appointment_date_updated": date_now,
                "appointment_date": finput["inputDate"],
                "appointment_taxi_address": finput["inputTaxiAddress"],
                "appointment_taxi_isbooked": (
                    "1" if "inputTaxiIsbooked" in finput else "0"
                ),
                "appointment_status": finput["inputStatus"],
                "appointment_comments": finput["inputComments"],
                "appointments_complete": "2",
            }

            # try to add appointment: if success try to send email
            try:
                api.add_appointment(data, token=token)
                flash("Appointment added!", "success")
                if os.name == "nt" and "EMAIL" in app.config and app.config["EMAIL"]:
                    records = conf.get_records_or_index(token=token)
                    ppt_records = records.participants.records[ppt_id]
                    apt_id = list(ppt_records.appointments.records)[-1]
                    utils.send_email_or_exception(
                        email_from=app.config["EMAIL"],
                        ppt_id=ppt_id,
                        apt_id=apt_id,
                        data=records.appointments.records[apt_id].data,
                        data_dict=data_dict,
                    )
                    calname = (
                        "Appointments - Test"
                        if app.config["TESTING"]
                        else "Appointments"
                    )
                    utils.create_event_or_exception(
                        account=app.config["EMAIL"],
                        calendar_name=calname,
                        ppt_id=ppt_id,
                        apt_id=apt_id,
                        data=records.appointments.records[apt_id].data,
                        data_dict=data_dict,
                    )
                return redirect(url_for("apt_all", records=records))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return render_template(
                    "apt_new.html", ppt_id=ppt_id, data_dict=data_dict
                )

        return render_template("apt_new.html", ppt_id=ppt_id, data_dict=data_dict)

    @app.route(
        "/participants/<string:ppt_id>/<string:apt_id>/appointment_modify",
        methods=["GET", "POST"],
    )
    @conf.token_required
    def apt_modify(apt_id: str, ppt_id: str):
        """Modify appointment page"""
        token = app.config["API_KEY"]
        data_dict = api.get_data_dict(token=token)
        data = api.Records(token=token).appointments.records[apt_id].data
        data = utils.replace_labels(data, data_dict)
        if request.method == "POST":
            finput = request.form
            date_now = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d %H:%M"
            )
            data = {
                "record_id": finput["inputId"],
                "redcap_repeat_instance": finput["inputAptId"].split(":")[1],
                "redcap_repeat_instrument": "appointments",
                "appointment_study": finput["inputStudy"],
                "appointment_date_updated": date_now,
                "appointment_date": finput["inputDate"],
                "appointment_taxi_address": finput["inputTaxiAddress"],
                "appointment_taxi_isbooked": (
                    "1" if "inputTaxiIsbooked" in finput.keys() else "0"
                ),
                "appointment_status": finput["inputStatus"],
                "appointment_comments": finput["inputComments"],
                "appointments_complete": "2",
            }

            # try to add appointment: if success try to send email
            try:
                api.add_appointment(data, token=token)
                records = conf.get_records_or_index(token=token)
                flash("Appointment modified!", "success")
                if "EMAIL" in app.config and app.config["EMAIL"]:
                    ppt_records = records.participants.records[ppt_id]
                    apt_id = list(ppt_records.appointments.records)[-1]
                    calname = (
                        "Appointments - Test"
                        if app.config["TESTING"]
                        else "Appointments"
                    )
                    utils.send_email_or_exception(
                        email_from=app.config["EMAIL"],
                        ppt_id=ppt_id,
                        apt_id=apt_id,
                        data=records.appointments.records[apt_id].data,
                        data_dict=data_dict,
                    )
                    utils.modify_event_or_exception(
                        account=app.config["EMAIL"],
                        calendar_name=calname,
                        ppt_id=ppt_id,
                        apt_id=apt_id,
                        data=records.appointments.records[apt_id].data,
                        data_dict=data_dict,
                    )
                return redirect(url_for("apt_all", records=records))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return render_template(
                    "apt_new.html", ppt_id=ppt_id, data_dict=data_dict
                )

        return render_template(
            "apt_modify.html",
            ppt_id=ppt_id,
            apt_id=apt_id,
            data=data,
            data_dict=data_dict,
        )
