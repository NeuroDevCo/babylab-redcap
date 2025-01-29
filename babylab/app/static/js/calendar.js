function calendar(events) {

    document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            themeSystem: 'bootstrap5',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,dayGridWeek',
            },
            weekNumbers: true,
            weekText: '',
            firstDay: '1',
            slotDuration: '00:30:00',
            droppable: true,
            navLinks: false,
            events: events,
            eventMaxStack: 4,
            dayMaxEvents: 4,
            dayMaxEventRows: 4,
            eventTimeFormat: {
                hour: 'numeric',
                minute: '2-digit',
                meridiem: 'short'
            },
        });
        calendar.render();
    });
}