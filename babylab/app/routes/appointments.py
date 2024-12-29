"""Appointments routes."""

import datetime
import requests
from flask import flash, redirect, render_template, url_for, request
from babylab.src import api, utils
from babylab.app import config as conf


def appointments_routes(app):
    """Appointments routes."""

    @app.route("/appointments/")
    @conf.token_required
    def apt_all():
        """Appointments database"""
        records = api.Records(token=app.config["API_KEY"])
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
        data = utils.prepare_appointments(records, data_dict=data_dict)
        return render_template("apt_all.html", data=data)

    @app.route("/appointments/<string:appt_id>")
    @conf.token_required
    def apt(appt_id: str = None):
        """Show the record_id for that appointment"""
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
        records = conf.get_records_or_index(token=app.config["API_KEY"])
        data = records.appointments.records[appt_id].data
        for k, v in data.items():
            dict_key = "appointment_" + k
            if dict_key in data_dict and v:
                data[k] = data_dict[dict_key][v]
            if dict_key == "appointment_taxi_isbooked":
                data[k] = "Yes" if v == "1" else "No"
        participant = records.participants.records[data["record_id"]].data
        participant["age_now_months"] = str(participant["age_now_months"])
        participant["age_now_days"] = str(participant["age_now_days"])
        return render_template(
            "apt.html",
            appt_id=appt_id,
            ppt_id=data["record_id"],
            data=data,
            participant=participant,
        )

    @app.route("/participants/<string:ppt_id>/appointment_new", methods=["GET", "POST"])
    @conf.token_required
    def apt_new(ppt_id: str):
        """New appointment page"""
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
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

            try:
                api.add_appointment(data, token=app.config["API_KEY"])
                flash(f"Appointment added! {finput['inputDate']}", "success")
                records = api.Records(token=app.config["API_KEY"])
                appt_id = list(
                    records.participants.records[ppt_id].appointments.records
                )[-1]
                if "EMAIL" in app.config and app.config["EMAIL"]:
                    email_data = {
                        "record_id": ppt_id,
                        "appointment_id": appt_id,
                        "status": data["appointment_status"],
                        "date": datetime.datetime.strptime(
                            data["appointment_date"], "%Y-%m-%dT%H:%M"
                        ).isoformat(),
                        "study": data["appointment_study"],
                        "taxi_address": data["appointment_taxi_address"],
                        "taxi_isbooked": data["appointment_taxi_isbooked"],
                        "comments": data["appointment_comments"],
                    }
                    data = utils.replace_labels(email_data, data_dict)
                    api.send_email(data=email_data, email_from=app.config["EMAIL"])
                return redirect(url_for("apt_all", records=records))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return render_template(
                    "apt_new.html", ppt_id=ppt_id, data_dict=data_dict
                )
            except api.MailDomainException as e:
                flash(
                    f"Appointment modified successfully, but e-mail was not sent: {e}",
                    "warning",
                )
                return render_template(
                    "apt_new.html", ppt_id=ppt_id, data_dict=data_dict
                )
            except api.MailAddressException as e:
                flash(
                    f"Appointment modified successfully, but e-mail was not sent: {e}",
                    "warning",
                )
                return render_template(
                    "apt_new.html", ppt_id=ppt_id, data_dict=data_dict
                )
        return render_template("apt_new.html", ppt_id=ppt_id, data_dict=data_dict)

    @app.route(
        "/participants/<string:ppt_id>/<string:appt_id>/appointment_modify",
        methods=["GET", "POST"],
    )
    @conf.token_required
    def apt_modify(
        appt_id: str,
        ppt_id: str,
    ):
        """Modify appointment page"""
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
        data = (
            api.Records(token=app.config["API_KEY"]).appointments.records[appt_id].data
        )
        for k, v in data.items():
            dict_key = "appointment_" + k
            if dict_key in data_dict and v:
                data[k] = data_dict[dict_key][v]
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
            try:
                api.add_appointment(
                    data,
                    token=app.config["API_KEY"],
                )
                email_data = {
                    "record_id": finput["inputId"],
                    "appointment_id": finput["inputAptId"],
                    "status": data["appointment_status"],
                    "date": datetime.datetime.strptime(
                        data["appointment_date"], "%Y-%m-%dT%H:%M"
                    ).isoformat(),
                    "study": data["appointment_study"],
                    "taxi_address": data["appointment_taxi_address"],
                    "taxi_isbooked": data["appointment_taxi_isbooked"],
                    "comments": data["appointment_comments"],
                }
                data = utils.replace_labels(email_data, data_dict)
                if "EMAIL" in app.config and app.config["EMAIL"]:
                    api.send_email(data=email_data, email_from=app.config["EMAIL"])
                flash("Appointment modified!", "success")
                return redirect(url_for("apt_all"))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return render_template(
                    "appointment_new.html", ppt_id=ppt_id, data_dict=data_dict
                )
            except api.MailDomainException as e:
                flash(
                    f"Appointment modified successfully, but e-mail was not sent: {e}",
                    "warning",
                )
                return render_template(
                    "apt_new.html", ppt_id=ppt_id, data_dict=data_dict
                )
            except api.MailAddressException as e:
                flash(
                    f"Appointment modified successfully, but e-mail was not sent: {e}",
                    "warning",
                )
                return render_template(
                    "apt_new.html", ppt_id=ppt_id, data_dict=data_dict
                )
        return render_template(
            "apt_modify.html",
            ppt_id=ppt_id,
            appt_id=appt_id,
            data=data,
            data_dict=data_dict,
        )
