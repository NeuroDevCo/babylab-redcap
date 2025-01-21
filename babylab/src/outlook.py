"""Outlook utils"""

import win32com.client as win
import pythoncom


class MailDomainException(Exception):
    """If e-mail address does not have SJD domain."""

    def __init__(self, email, domain):
        msg = f"E-mail provided '{email}' does not have domain '{domain}'"
        super().__init__(msg)


class MailAddressException(win.pywintypes.com_error):  # pylint: disable=no-member
    """If e-mail address is not authorized in local Outlook app."""

    def __init__(self, email):
        msg = f"E-mail provided '{email}' is not authorized in local Outlook app'"
        super().__init__(msg)


def check_email_address(email: str):
    """Check if e-mail address is authorized in local Outlook app.

    Args:
        email (str): Email address to check.
    """  # pylint: disable=line-too-long
    pythoncom.CoInitialize()  # pylint: disable=no-member
    ol_app = win.Dispatch("Outlook.Application")
    ol_ns = ol_app.GetNameSpace("MAPI")
    mail_item = ol_app.CreateItem(0)
    try:
        mail_item._oleobj_.Invoke(  # pylint: disable=protected-access
            *(64209, 0, 8, 0, ol_ns.Accounts.Item(email))
        )
    except win.pywintypes.com_error as e:  # pylint: disable=no-member
        raise MailAddressException(email) from e


def check_email_domain(email: str, target_domain: str = "sjd.es"):
    """Assert that provided email has certain domain.

    Args:
        email (str): E-mail address provided.
        target_domain (str, optional): Domain to find. Defaults to "sjd.es".

    Raises:
        MailDomainException: If e-mail address does not have target domain.
    """
    email_domain = email.split("@")[1]
    if email_domain != target_domain:
        raise MailDomainException(email, target_domain)


def compose_outlook(data: dict) -> dict:
    """Compose e-mail or event subject and body based on data dictionary

    Args:
        data (dict): Appointment and participant data to fill in the subject and body.

    Returns:
        dict: Dictionary with composed subject and body.
    """  # pylint: disable=line-too-long
    out = dict(data)
    out["subject"] = (
        f"Appointment { out['id'] } ({ out['status'] }) | { out['study'] } (ID: { out['record_id'] }) - { out['date'] }"  # pylint: disable=line-too-long
    )
    out["body"] = (
        f"The appointment {out['id']} (ID: {out['record_id']}) from study {out['study']} has been created or modified. "
        f"Here are the details:\n\n"
        f"- Appointment ID: {out['id']}\n"
        f"- Appointment date: {out['date']}\n"
        f"- Participant ID: {out['record_id']}\n"
        f"- Current status: {out['status']}\n"
        f"- Taxi: {out['taxi_address']}\n"
        f"- Taxi booked?: {out['taxi_isbooked']}\n"
        f"- Notes: {out['comments']}\n"
    )
    return out


def send_email(
    data: dict,
    email_from: str = "gonzalo.garcia@sjd.es",
    email_to: str = "gonzalo.garcia@sjd.es",
):
    """Send e-mail using Outlook.

    Args:
        data (dict): Dictionary with the subject, body, and other properties of the e-mail.
        email_from (str, optional): E-mail address to send the e-mail from. Defaults to "gonzalo.garcia@sjd.es".
        email_to (str, optional): E-mail address to send the e-mail to. . Defaults to "gonzalo.garcia@sjd.es".
    """  # pylint: disable=line-too-long
    check_email_domain(email_from)
    check_email_domain(email_to)
    composed = compose_outlook(data)
    pythoncom.CoInitialize()  # pylint: disable=no-member

    ol_app = win.Dispatch("Outlook.Application")
    ol_ns = ol_app.GetNameSpace("MAPI")
    mail_item = ol_app.CreateItem(0)
    mail_item.Subject = composed["subject"]
    mail_item.Body = composed["body"]
    mail_item.To = email_to
    mail_item._oleobj_.Invoke(  # pylint: disable=protected-access
        *(64209, 0, 8, 0, ol_ns.Accounts.Item(email_from))
    )
    mail_item.Send()


def create_event(
    data: dict,
    account: str = "gonzalo.garcia@sjd.es",
    calendar_name: str = "Appointments",
) -> None:
    """Create a calendar event on Outlook.

    Args:
        data (dict): Dictionary with the subject, body, and other properties of the event.
        account (str, optional): E-mail address from which the event will be created. Defaults to "gonzalo.garcia@sjd.es".
        calendar_name (str, optional): Calendar name. Defaults to "Appointments".

    """  # pylint: disable="line-too-long"
    check_email_domain(account)
    composed = compose_outlook(data)

    ol_app = win.Dispatch("Outlook.Application")
    namespace = ol_app.GetNamespace("MAPI")

    recipient = namespace.createRecipient(account)
    shared_cal = namespace.GetSharedDefaultFolder(recipient, 9).Folders(calendar_name)

    apt = shared_cal.Items.Add(1)
    apt.Start = " ".join(composed["date"].split("T"))
    apt.Subject = composed["subject"]
    apt.Duration = 60
    apt.BodyFormat = 1
    apt.Body = composed["body"]
    apt.MeetingStatus = "5" if "Cancelled" in data["status"] else "1"
    apt.Location = "Barcelona, Spain"
    apt.ResponseRequested = "true"
    apt.Save()


def modify_event(
    data: dict,
    account: str = "gonzalo.garcia@sjd.es",
    calendar_name: str = "Appointments",
) -> None:
    """Create a calendar event on Outlook.

    Args:
        data (dict): Dictionary with the subject, body, and other properties of the event.
        account (str, optional): E-mail address from which the event will be created. Defaults to "gonzalo.garcia@sjd.es".
        calendar_name (str, optional): Calendar name. Defaults to "Appointments".
    """  # pylint: disable="line-too-long"
    check_email_domain(account)
    composed = compose_outlook(data)

    ol_app = win.Dispatch("Outlook.Application")
    namespace = ol_app.GetNamespace("MAPI")

    recipient = namespace.createRecipient(account)
    shared_cal = namespace.GetSharedDefaultFolder(recipient, 9).Folders(calendar_name)

    for apt in shared_cal.Items:
        detected = composed["id"] in apt.Subject
        if detected:
            apt.Start = " ".join(composed["date"].split("T"))
            apt.Subject = composed["subject"]
            apt.Duration = 60
            apt.BodyFormat = 2
            apt.Body = composed["body"]
            apt.MeetingStatus = "5" if "Cancelled" in data["status"] else "1"
            apt.Save()
