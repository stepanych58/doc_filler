// window.onload = function () {
//   var generateReportButton = document.getElementById('genRep')
//   generateReportButton.addEventListener("click", function () {
//     csrftoken = getCookie('csrftoken')
//     var xhr = new XMLHttpRequest();
//     xhr.open("POST", "/generateReport/", true)
//     xhr.setRequestHeader("X-CSRFToken", csrftoken);
//     var generateTemplateContext;
//
//     cl_checkboxes = document.getElementsByName('cl_checked');
//
//     xhr.send(generateTemplateContext)
//   })
// }
//https://www.youtube.com/watch?v=FVEtgUNVhGk

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function generateReport(doc_id) {
    csrftoken = getCookie('csrftoken')//in future we can change name of cookie
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/generateReport/")
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Location", '/clients/');
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    cl_checkboxes = document.getElementsByName('cl_checked');
    var checkedClients = [];
    var checkedDocs = [doc_id];
    cl_checkboxes.forEach(function (element) {
        if (element.checked) {
            checkedClients.push(String(element.value))
        }
    })
    var viewParams = JSON.stringify({
        'checkedClients': checkedClients,
        'checkedDocs': checkedDocs
    });
    xhr.send(viewParams)
    xhr.onreadystatechange = function () {
        location = location //to reload page
    }
}


function showButton() {
    var checkboxes = document.getElementsByClassName('ch');
    var deleteButton = document.getElementById('delete');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].onchange = function () {
            var checked = false;
            for (var i = 0; i < checkboxes.length; i++) {
                if (checkboxes[i].checked) {
                    checked = true;
                    break;
                }
            }
            deleteButton.style.display = checked ? 'block' : 'none';
        }
    }


}

var counter = 0;

function createChild() {
    var childDiv = document.getElementById('childs_id');
    var newdiv = document.createElement('div');
    newdiv.id = "child_id_" + counter;

    newdiv.innerHTML =
        "<div class=\"input-group\">\n" +
        "<div class=\"input-group-prepend\">\n" +
        "    <span class=\"input-group-text\" id=\"\">First and last name</span>\n" +
        "  </div>\n" +
        "  <input type=\"text\" class=\"form-control\">\n" +
        "  <input type=\"text\" class=\"form-control\">" +
        "  <input type=\"text\" class=\"form-control\">" +
        "<div class=\"input-group-prepend\">\n" +
        "    <span class=\"input-group-text\" id=\"\">First and last name</span>\n" +
        "  </div>\n" +
        "  <input type=\"text\" class=\"form-control\">" +
        "  <div class=\"input-group-append\">\n" +
        "    <input type=\"button\" class=\"btn btn-outline-secondary\" value=\"-\" id=" + "\"chld_" + counter + "\" onClick=\"removeInput(this);\" />\n" +
        "  </div>\n" +
        "</div>";
    // = "Entry " + (counter + 1) + " <br>" +
    // "<input type='text' class='form-control' name='myInputs[]'>"+
    // "<input type='button' value='-' class='btn btn-outline-primary' onClick='removeInput(this);'>";
    childDiv.appendChild(newdiv);
    counter++;
}

function removeInput(elem) {
    //var elem = document.getElementById(id);
    var childContainer = elem.parentNode;
    var count_id = elem.id.replace("chld_", "")
    var forDeleteElem = document.getElementById("child_id_" + count_id)
    var childContainer2 = forDeleteElem.parentNode;
    return childContainer2.removeChild(forDeleteElem)
    // childContainer2.removeChild(childContainer);
}

function createInputIfOther(elem) {
    // use one of possible conditions
    // if (elem.value == 'Other')
    var selectedValue = elem.options[elem.selectedIndex].text;
    if (selectedValue == "иное") {
        document.getElementById("other-div").style.display = 'block';
    } else {
        document.getElementById("other-div").style.display = 'none';
    }
}

function showFactAddressForm(elem) {
    var selectedValue = elem.options[elem.selectedIndex].text;
    if (selectedValue === 'Да') {
        // console.log('Адрес регистрации совпадает с адресом проживания');
        var actualAddressField = document.getElementById('actualAddress_');
        if (actualAddressField) {
            actualAddressField.style = 'display: none'
        }
    } else {
        // console.log('Адрес регистрации не совпадает с адресом проживания');
        var actualAddressField = document.getElementById('actualAddress_');
        if (actualAddressField) {
            actualAddressField.style = ''
        } else {
            var childDiv = document.getElementById('actualAddress');
            var addr2 = document.createElement('div');
            addr2.id = "actualAddress_";
            console.log("ураааа!!")
            addrBlock = "<div class=\"row\"><div class=\"col-md-4 mb-3\"><label for=\"id_index\">Индекс</label><input type=\"None\" name=\"index\" class=\"form-control\" id=\"id_index\"></div><div class=\"invalid-feedback\">Valid Индекс is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_country\">Страна</label><input type=\"None\" name=\"country\" class=\"form-control\" id=\"id_country\"></div><div class=\"invalid-feedback\">Valid Страна is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_city\">Город</label><input type=\"None\" name=\"city\" class=\"form-control\" id=\"id_city\"></div><div class=\"invalid-feedback\">Valid Город is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_street\">Улица</label><input type=\"None\" name=\"street\" class=\"form-control\" id=\"id_street\"></div><div class=\"invalid-feedback\">Valid Улица is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_buildingNumber\">Номер дома</label><input type=\"None\" name=\"buildingNumber\" class=\"form-control\" id=\"id_buildingNumber\"></div><div class=\"invalid-feedback\">Valid Номер дома is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_housing\">Корпус</label><input type=\"None\" name=\"housing\" class=\"form-control\" id=\"id_housing\"></div><div class=\"invalid-feedback\">Valid Корпус is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_structure\">Строение</label><input type=\"None\" name=\"structure\" class=\"form-control\" id=\"id_structure\"></div><div class=\"invalid-feedback\">Valid Строение is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_flat\">Квартира</label><input type=\"None\" name=\"flat\" class=\"form-control\" id=\"id_flat\"></div><div class=\"invalid-feedback\">Valid Квартира is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_oblast\">Область</label><input type=\"None\" name=\"oblast\" class=\"form-control\" id=\"id_oblast\"></div><div class=\"invalid-feedback\">Valid Область is required.</div><div class=\"col-md-4 mb-3\"><label for=\"id_rayon\">Район</label><input type=\"None\" name=\"rayon\" class=\"form-control\" id=\"id_rayon\"></div><div class=\"invalid-feedback\">Valid Район is required.</div></div>"
            addr2.innerHTML = addrBlock;
            childDiv.appendChild(addr2);
        }
    }
}