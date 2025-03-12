function get_age(birth, test) {
    let date_birth = new Date(date = moment(birth));
    let date_test = new Date(date = moment(test));

    console.log(date_birth)
    console.log(date_test)

    let diff = date_test - date_birth;
    console.log(diff)

    let mm = Math.floor(diff / 1000 / 60) % 60;
    let hh = Math.floor(diff / 1000 / 60 / 60);
    let dd = Math.floor(diff / 1000 / 60 / 60 / 24);
    let mo = Math.floor(diff / 1000 / 60 / 60 / 24 / 30.34) % 30.34;

    output = `${mo}mo, ${dd}d, ${hh}h, ${mm}min`
    console.log(output);
    return output
};

