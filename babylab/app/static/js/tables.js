function dt(id, searchCols, hideCols, lookupCols, queStatusCol, aptStatusCol) {


    let table = new DataTable(id, {
        fixedHeader: true,
        layout: {
            topStart: {
                buttons: [
                    {
                        extend: 'searchPanes',
                        config: {
                            cascadePanes: true,
                            combiner: 'or',
                            collapse: true,
                            controls: false,
                            viewTotal: true,
                            columns: searchCols,
                        }
                    }
                ]
            },
        },
        language: {
            searchPanes: {
                collapse: '<i class="fa fa-filter fa-lg"></i>&nbsp;&nbsp;Filter'
            },
        },
        columnDefs: [
            {
                visible: false,
                targets: hideCols,
            },
            {
                searchable: true,
                targets: lookupCols,
            },
            {
                searchable: false,
                targets: '_all',
            },
        ],
        rowCallback: (row, data) => {
            if (typeof queStatusCol !== "undefined") {
                c = format_que_status(data[queStatusCol])
                $('td:eq(2)', row).css('color', c);
            }
            if (typeof aptStatusCol !== "undefined") {
                c = format_apt_status(data[aptStatusCol])
                $('td:eq(2)', row).css('color', c);
            }
        },
    });
    return table;
}

function format_que_status(x) {
    switch (x) {
        case 'Estimated':
            return '#d62728'
        case 'Calculated':
            return '#0ea844'
        default:
            return '#000000'
    }
}

function format_apt_status(x) {
    switch (x) {
        case 'Scheduled':
            return '#000000'
        case 'Confirmed':
            return '#ffb700'
        case 'Successful':
            return '#0ea844'
        case 'Cancelled - Reschedule':
            return '#d62728'
        default:
            return '#acabab'
    }
}




function format_ppt(d) {
    const initial = arr => arr.slice(0, -1);
    cols = ['', 'ID', 'Name', 'Age (months)', 'Age (days)', 'Sex', 'Source', 'E-mail 1', 'E-mail 2', 'Phone1', 'Phone 2', 'Date created', 'Date updated', 'Comments']
    x = '<div class="card-table"><div class="card-title">Participant ' + d[1] + '</div><table class="tbl-record table-hover table-responsive" style="user-select: none">'
    d = initial(d)
    for (let i = 0; i < d.length; i++) {
        x += '<tr><td width="50%"><em>' + cols[i] + '</em></td><td>' + d[i] + '</td></tr>';
    };
    return x + '</table></div>';
}

function format_apt(d) {
    const initial = arr => arr.slice(0, -1);
    x = '<div class="card-table"><div class="card-title">Appointment ' + d[1] + '</div><table class="tbl-record table-hover table-responsive" style="user-select: none">'
    cols = ['', 'Appointment ID', 'Participant ID', 'Study', 'Status', 'Date', 'Date created', 'Date updated', 'Taxi address', 'Taxi booked?', 'Comments']
    d = initial(d)
    for (let i = 0; i < d.length; i++) {
        x += '<tr><td width="50%"><em>' + cols[i] + '</em></td><td>' + d[i] + '</td></tr>';
    };
    return x + '</table></div>';
}

function format_que(d) {
    const initial = arr => arr.slice(0, -1);
    x = '<div class="card-table"><div class="card-title">Questionaire ' + d[1] + '</div><table class="tbl-record table-hover table-responsive" style="user-select: none">'
    cols = ['', 'Questionnaire ID', 'Participant ID', 'Is estimated?', 'L1', 'L1 (%)', 'L2', 'L2 (%)', 'L3', 'L3 (%)', 'L4', 'L4 (%)', 'Created', 'Updated', 'Comments']
    d = initial(d)
    for (let i = 0; i < d.length; i++) {
        x += '<tr><td width="50%"><em>' + cols[i] + '</em></td><td>' + d[i] + '</td></tr>';
    };
    return x + '</table></div>';
}

