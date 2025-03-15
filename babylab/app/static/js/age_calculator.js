// const { default: moment } = await import("moment");

function get_age(date1, date2, units = "md") {

    let d1 = new Date(moment(date1));
    let d2 = new Date(moment(date2));
    let diff = d2 - d1;

    if (units == "md") {
        let d = Math.floor(diff / (1000 * 60 * 60 * 24));
        let m = Math.floor(d / 30.34);
        d = Math.floor(d % 30.34);
        if (isNaN(m) || isNaN(d)) {
            return "Incorrect dates provided."
        }
        return `${m} months, ${d} days`
    }
    if (units == "hm") {
        let d1 = new Date(moment(date1));
        let d2 = new Date(moment(date2));
        let diff = d2 - d1;
        let m = Math.floor(diff / (1000 * 60));
        let h = Math.floor(m / 60);
        m = Math.floor(m % 60);
        if (isNaN(h) || isNaN(m)) {
            return "Incorrect dates provided."
        }
        return `${h} hours, ${m} minutes`
    }


}


