## v0.2.2

- Fix age display in participant and appointment pages #67
- Fixes language questionnaires not being saved #73
- Removes e-mail sending and calendar event creation #55
- Adds `make_id` function to simplify testing
- Add better handling of 500 error #63
- Adds Ubuntu and macOS to GitHub Actions workflows
- Fixes modifying record pages not saving default values in text areas #78
- Adds `get_participant`, `get_appointment`, and `get_questionnaire` to fetch information from individual records
- Cleans Python dependencies
- More severe tests for adding and modifying records #57 #76
- Adds .sh and .bat launchers for Windows, Linux, and macOS #77
- Use Roboto for body text and as fallback font #71
- Fix dashboard age plot ordering of age bins #74
- Fix card footers in index
- Fixes head circumference not showing in participant page #70

## v0.2.1

- Fixes bug in which appointments were not being properly modified #64
- Fixes missing information in appointment page #66
- Uses waitress as WSGI server
- Makes some styling changes
- Adds a .bat file for desktop shortcut

## v0.2.0

- Speeds up by avoiding unnecessary requests #48
- Uses DataTables.js to display and filter tables #48
- Implements a basic calendar to display appointments using FullCalendar.js #43 
- Adds new function to API to fetch a single participant (and associated records) #48
- Some styling changes
- Adds extra information to the Dashboard
- Adds unit and functional testing for all features

## v0.1.5

- Fixes deleting function #46 
- Adds "source" field to new participant and modify participant pages #45 
- Use Noto Sans font for headers
- Simplifies README file

## v0.1.4

- Add record-deleting functions to API
- Calendar events using the Python API #43
- Fix PyPi URLs #40
- Allow 0m0d age #44
- Delete events/appointments/emails after testing #46
- Add dev scripts for convenience during test development
- Fixes table width

## v0.1.3

- Minor fixes

## v0.1.2

- Fixes participant table position (#36)
- Updates README file
- Fixes questionnaire ID page (#38)
- Removes Dockerfile
- Renames studies to new standard

## v0.1.1

- Make command for updating CHANGELOG
- Simplify utils
- Add testing for `api.send_email` locally
- Add client testing for emails

## v0.1.0

- Restructure the routes into modules.
- Add pytest suite to API, utils, and main routes in the app.
- Add coverage analysis to pytest routines.
- Add coverage report to GitHub workflows.
- Add circle plot for appointment status.


