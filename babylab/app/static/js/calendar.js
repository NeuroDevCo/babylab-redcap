function calendar(events) {

    document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            themeSystem: 'bootstrap5',
            headerToolbar: {
                left: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay,list',
                center: 'title',
                right: 'prev,today,next',
            },
            footerToolbar: {
                right: 'prev,next',
            },
            buttonText: {
                today: 'Today',
                year: 'Year',
                month: 'Month',
                week: 'Week',
                day: 'Day',
                list: 'List',
            },
            eventRender: function (info) {
                var tooltip = new Tooltip(info.el, {
                    title: info.event.extendedProps.description,
                    placement: 'top',
                    trigger: 'hover',
                    container: 'body'
                });
            },
            contentHeight: "700px",
            weekNumbers: true,
            stickyHeaderDates: true,
            weekText: '',
            firstDay: '1',
            slotDuration: '00:30:00',
            droppable: true,
            navLinks: false,
            events: events,
            eventMaxStack: 4,
            dayMaxEvents: 4,
            dayMaxEventRows: 4,
            nowIndicator: true,
            eventTimeFormat: {
                hour: 'numeric',
                minute: '2-digit',
                hour12: false,
            },
            slotLabelFormat: {
                hour: 'numeric',
                minute: '2-digit',
                hour12: false,
            },

        });
        calendar.render();
    });
}