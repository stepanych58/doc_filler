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
return id

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
        alert('Адрес регистрации совпадает с адресом проживания');
    } else {
        alert('Адрес регистрации не совпадает с адресом проживания');
        //todo создать форму и вставить в документ
    }
}