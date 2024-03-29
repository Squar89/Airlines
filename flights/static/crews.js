window.addEventListener("load", function() {
    document.getElementById("submit").addEventListener("click", function() {
        var req = new XMLHttpRequest();
        req.addEventListener("load", function() {
            if (req.status === 200) {
                var data = JSON.parse(req.responseText);

                var table = prepareTable(data);
                document.getElementById("content_flights").innerHTML = table;
                document.getElementById("show_flights").style.display = "block";

                var select = prepareSelect(data);
                document.getElementById("content_assign").innerHTML = select;
                document.getElementById("show_assign").style.display = "block";
            }
            else {
                alert("Error (status: " + req.status + ")");
            }
        });
        req.open("GET", "/flights/crews?date=" + document.getElementById("s_day").value, true);
        req.send();
    });

    document.getElementById("assign").addEventListener("click", function () {
        var requ = new XMLHttpRequest();
        requ.addEventListener("load", function () {
            if (requ.status === 200) {
                var data = JSON.parse(requ.responseText);

                if (data['success'] === 1) {
                    document.getElementById("result_message").innerText = "Crew assigned successfully";
                    document.getElementById("result_message").style.display = "block";
                }
                else {
                    alert("Error: " + data['message']);
                }
            }
            else {
                alert("Error (status: " + requ.status + ")");
            }
        });
        requ.open("POST", "/flights/crews", true);
        requ.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        var flight_id = document.getElementById("flight_select").value;
        var crew_id = document.getElementById("crew_select").value;
        requ.send("flight_id=" + encodeURIComponent(flight_id) + "&crew_id=" + encodeURIComponent(crew_id));
    })
});

function prepareTable(data) {
    var ret_string =
        "<table><tr><th>Id</th><th>From</th><th>To</th><th>Departure</th><th>Arrival</th><th>Airplane</th><th>Crew</th></tr>";
    data["flights"].sort(function (a, b) {
        var da = new Date(a.date_dep);
        var db = new Date(b.date_dep);

        if (da < db) return -1;
        if (da === db) return 0;
        if (da > db) return 1;
    });
    var i;
    for (i = 0; i < data["flights"].length; i++) {
        ret_string += "<tr><td>" + data["flights"][i].id + "</td><td>" + data["flights"][i].city_from + "</td><td>" + data["flights"][i].city_to +
        "</td><td>" + new Date(data["flights"][i].date_dep) + "</td><td>" + new Date(data["flights"][i].date_arr) + "</td><td>" +
        data["flights"][i].airplane + "</td><td>" + data["flights"][i].crew + "</td></tr>";
    }
    ret_string += "</table>";

    return ret_string;
}

function prepareSelect(data) {
    var ret_string = "Flight id: <select id='flight_select'>";
    var i;
    for (i = 0; i < data["flights"].length; i++) {
        ret_string += "<option value='" + data["flights"][i].id + "'>" + data["flights"][i].id + "</option>"
    }
    ret_string += "</select>";

    ret_string += "<select id='crew_select'>";
    for (i = 0; i < data['crews'].length; i++) {
        ret_string += "<option value='" + data['crews'][i].id + "'>" + data['crews'][i].c_first_name + " " +
                       data['crews'][i].c_last_name + "</option>"
    }
    ret_string += "</select>";

    return ret_string;
}