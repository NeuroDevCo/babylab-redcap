## v0.2.1

- Fixes bug in which appointments were not being properly modified #64
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


