function validate() {
    var result = validatePassword();
    return result;
}

function validatePassword() {
    var pass = document.getElementById("password").value;
    var cpass = document.getElementById("cpassword").value;
    if (pass == cpass) {
        return validateEmailAddress()
    } else {
        alert("Passwords do not match");
        document.getElementById("cpassword").focus();
        return false;
    }
}

function validateEmailAddress() {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.getElementById("email").value)) {
        return validatePhoneNumber()
    }
    alert("You have entered an invalid email address!")
    document.getElementById("email").focus();
    return (false)
}

// Allowed Format
// (123) 456-7890
// 123-456-7890
// 123.456.7890
// 1234567890
function validatePhoneNumber() {
    if (/^[(]{0,1}[0-9]{3}[)]{0,1}[-\s\.]{0,1}[0-9]{3}[-\s\.]{0,1}[0-9]{4}$/.test(document.getElementById("phone").value)) {
        return (true)
    }
    alert("You have entered an invalid phone number!")
    document.getElementById("phone").focus();
    return (false)
}


var countryStateInfo = {
    "USA": {
        "California": {
            "Los Angeles": ["90001", "90002", "90003", "90004"],
            "San Diego": ["92093", "92101"]
        },
        "Texas": {
            "Dallas": ["75201", "75202"],
            "Austin": ["73301", "73344"]
        }
    },
    "India": {
        "Assam": {
            "Dispur": ["781005"],
            "Guwahati": ["781030", "781030"]
        },
        "Gujarat": {
            "Vadodara": ["390011", "390020"],
            "Surat": ["395006", "395002"]
        }
    }
}



window.onload = function () {

    //Get html elements
    var countySel = document.getElementById("countySel");
    var stateSel = document.getElementById("stateSel");
    var citySel = document.getElementById("citySel");
    var zipSel = document.getElementById("zipSel");

    //Load countries
    for (var country in countryStateInfo) {
        countySel.options[countySel.options.length] = new Option(country, country);
    }

    //County Changed
    countySel.onchange = function () {

        stateSel.length = 1; // remove all options bar first
        citySel.length = 1; // remove all options bar first
        zipSel.length = 1; // remove all options bar first

        if (this.selectedIndex < 1)
            return; // done

        for (var state in countryStateInfo[this.value]) {
            stateSel.options[stateSel.options.length] = new Option(state, state);
        }
    }

    //State Changed
    stateSel.onchange = function () {

        citySel.length = 1; // remove all options bar first
        zipSel.length = 1; // remove all options bar first

        if (this.selectedIndex < 1)
            return; // done

        for (var city in countryStateInfo[countySel.value][this.value]) {
            citySel.options[citySel.options.length] = new Option(city, city);
        }
    }

    //City Changed
    citySel.onchange = function () {
        zipSel.length = 1; // remove all options bar first

        if (this.selectedIndex < 1)
            return; // done

        var zips = countryStateInfo[countySel.value][stateSel.value][this.value];
        for (var i = 0; i < zips.length; i++) {
            zipSel.options[zipSel.options.length] = new Option(zips[i], zips[i]);
        }
    }

}