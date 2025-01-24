function dt(id, searchCols, hideCols) {
    let panes = {
        extend: 'searchPanes',
        config: {
            cascadePanes: true,
            combiner: 'and',
            collapse: false,
            controls: false,
            viewTotal: true,
            columns: searchCols,
        },
        text: '<i class="fa fa-filter fa-lg"></i>&nbsp;&nbsp;Filter',

    };

    let table = new DataTable(id, {
        fixedHeader: true,
        layout: {
            topStart: 'buttons',
        },
        buttons: [panes],
        language: {
            searchPanes: {
                collapse: '<i class="fa fa-filter fa-lg"></i>&nbsp;&nbsp;Filter'
            },
        },
        columnDefs: [
            {
                visible: false,
                targets: hideCols,
            }
        ]
    });
    return table;
}

function format_ppt(d) {
    const initial = arr => arr.slice(0, -1);
    x = '<div class="card-table"><table class="tbl-record table-hover table-responsive">'
    cols = ['<h3>Participant ' + d[1] + '</h3><br>', 'ID', 'Name', 'Age (months)', 'Age (days)', 'Sex', 'Source', 'E-mail 1', 'E-mail 2', 'Phone1', 'Phone 2', 'Date created', 'Date updated', 'Comments']
    for (let i = 0; i < initial(d).length; i++) {
        x += '<tr><th scope="row" style="width:50%">' + cols[i] + '</th><td>' + d[i] + '</td></tr>';
    };
    return x + '</table></div>';
}

function format_apt(d) {
    const initial = arr => arr.slice(0, -1);
    x = '<div class="card-table"><table class="tbl-record table-hover table-responsive">'
    cols = ['<h3>Appointment ' + d[1] + '</h3><br>', 'Appointment ID', 'Participant ID', 'Study', 'Status', 'Date', 'Date created', 'Date updated', 'Taxi address', 'Taxi booked?', 'Comments']
    for (let i = 0; i < initial(d).length; i++) {
        x += '<tr><th scope="row" style="width:50%">' + cols[i] + '</th><td>' + d[i] + '</td></tr>';
    };
    return x + '</table></div>';
}

function format_que(d) {
    const initial = arr => arr.slice(0, -1);
    x = '<div class="card-table"><table class="tbl-record table-hover table-responsive">'
    cols = ['<h3>Questionnaire ' + d[1] + '</h3><br>', 'Questionnaire ID', 'Participant ID', 'Is estimated?', 'L1', 'L1 (%)', 'L2', 'L2 (%)', 'L3', 'L3 (%)', 'L4', 'L4 (%)', 'Created', 'Updated', 'Comments']
    for (let i = 0; i < initial(d).length; i++) {
        x += '<tr><th scope="row" style="width:50%">' + cols[i] + '</th><td>' + d[i] + '</td></tr>';
    };
    return x + '</table></div>';
}

