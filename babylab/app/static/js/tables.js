function tbl_ppt(id) {
    let table = new DataTable(id, {
        fixedHeader: true,
        autoWidth: false,
        columns: [
            { title: '' },
            { title: 'ID' },
            { title: 'Name' },
            { title: 'Months' },
            { title: 'Days' },
            { title: 'Sex' },
            { title: 'Source' },
            { title: 'E-mail' },
            { title: 'Phone' },
            { title: '' },
        ],
        keys: true,
        layout: {
            bottom: {
                searchPanes: {
                    layout: 'columns-4',
                    cascadePanes: true,
                    orderable: false,
                    collapse: false,
                    dtOpts: {
                        paging: true,
                        pagingType: 'numbers',
                        searching: true
                    }
                }
            }
        },
        columnDefs: [
            {
                visible: false,
                targets: 0
            },
            {
                searchPanes: {
                    show: true,
                },
                targets: [1, 2, 3, 4, 5, 6, 7, 8]
            },
        ]
    })
    return table;
}

function tbl_apt(id) {
    let table = new DataTable(id, {
        fixedHeader: true,
        autoWidth: false,
        columns: [
            { title: '' },
            { title: 'Appointment' },
            { title: 'ID' },
            { title: 'Study' },
            { title: 'Status' },
            { title: 'Date' },
            { title: 'Made on the' },
            { title: 'Last updated' },
            { title: 'Taxi address' },
            { title: 'Taxi booked' },
            { title: 'Comments' },
            { title: '' },

        ],
        layout: {
            bottom: {
                searchPanes: {
                    layout: 'columns-4',
                    cascadePanes: true,
                    orderable: false,
                    collapse: false,
                    dtOpts: {
                        paging: true,
                        pagingType: 'numbers',
                        searching: true
                    }
                }
            }
        },
        columnDefs: [
            {
                visible: false,
                searchPanes: {
                    show: false,
                },
                targets: [0, 5, 6, 7, 10]
            },
        ]
    })
    return table;
}

function tbl_que(id) {
    let table = new DataTable(id, {
        fixedHeader: true,
        autoWidth: true,
        columns: [
            { title: '' },
            { title: 'Questionnaire', width: "14%" },
            { title: 'ID', width: "5%" },
            { title: 'Status', width: "10%" },
            { title: 'L1' },
            { title: '%' },
            { title: 'L2' },
            { title: '%' },
            { title: 'L3' },
            { title: '%' },
            { title: 'L4' },
            { title: '%' },
            { title: 'Date updated' },
            { title: 'Date created' },
            { title: '' },
        ],
        keys: true,
        layout: {
            bottom: {
                searchPanes: {
                    layout: 'columns-6',
                    cascadePanes: true,
                    orderable: false,
                    collapse: false,
                    dtOpts: {
                        paging: true,
                        pagingType: 'numbers',
                        searching: true
                    }
                }
            }
        },
        columnDefs: [
            {
                visible: false,
                searchPanes: {
                    show: false,
                },
                targets: [0, 12, 13]
            },
            {
                searchPanes: {
                    show: false,
                },
                targets: [5, 7, 9, 11]
            },
        ]
    })
    return table;
}