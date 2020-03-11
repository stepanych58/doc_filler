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

function addClientChildForm() {
    var childDiv = document.getElementById('childs_id');
    var newdiv = document.createElement('div');
    newdiv.id = "child_id_" + counter;

    newdiv.innerHTML =
    "<div class=\"row\" id=\"\">\n" +
        "                    <div class=\"col-md-4 mb-3\"><label for=\"id_last_name\">Фамилия</label><input type=\"None\"\n" +
        "                                                                                               name=\"last_name\"\n" +
        "                                                                                               class=\"form-control\"\n" +
        "                                                                                               id=\"id_last_name\"></div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Фамилия is required.</div>\n" +
        "                    <div class=\"col-md-4 mb-3\"><label for=\"id_first_name\">Имя</label><input type=\"None\"\n" +
        "                                                                                            name=\"first_name\"\n" +
        "                                                                                            class=\"form-control\"\n" +
        "                                                                                            id=\"id_first_name\"></div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Имя is required.</div>\n" +
        "                    <div class=\"col-md-4 mb-3\"><label for=\"id_part_name\">Отчество</label><input type=\"None\"\n" +
        "                                                                                                name=\"part_name\"\n" +
        "                                                                                                class=\"form-control\"\n" +
        "                                                                                                id=\"id_part_name\"></div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Отчество is required.</div>\n" +
        "                    <div class=\"col-md-4 mb-3\" style=\"display:none;\"><label for=\"id_position\">Должность</label><input type=\"None\"\n" +
        "                                                                                                name=\"position\"\n" +
        "                                                                                                class=\"form-control\"\n" +
        "                                                                                                id=\"id_position\"></div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Должность is required.</div>\n" +
        "                    <div class=\"col-md-4 mb-3\"><label for=\"id_phone_number\">Телефонный номер</label><input type=\"None\"\n" +
        "                                                                                                           name=\"phone_number\"\n" +
        "                                                                                                           class=\"form-control\"\n" +
        "                                                                                                           id=\"id_phone_number\">\n" +
        "                    </div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Телефонный номер is required.</div>\n" +
        "                    <div class=\"col-md-4 mb-3\"><label for=\"id_email_v\">Email</label><input type=\"email\" name=\"email_v\"\n" +
        "                                                                                           class=\"form-control\"\n" +
        "                                                                                           id=\"id_email_v\"></div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Email is required.</div>\n" +
        "                    <div class=\"col-md-4 mb-3\"><label for=\"id_relation_degree\">Степень родства</label><select\n" +
        "                            name=\"relation_degree\" class=\"form-control\" id=\"id_relation_degree\">\n" +
        "                        <option value=\"1\" style=\"display:none;\">Муж</option>\n" +
        "                        <option value=\"2\" style=\"display:none;\">Жена</option>\n" +
        "                        <option value=\"3\" selected>Сын</option>\n" +
        "                        <option value=\"4\">Дочь</option>\n" +
        "                        <option value=\"5\" style=\"display:none;\">Брат</option>\n" +
        "                        <option value=\"6\" style=\"display:none;\">Сестра</option>\n" +
        "                        <option value=\"7\" style=\"display:none;\">Мать</option>\n" +
        "                        <option value=\"8\" style=\"display:none;\">Отец</option>\n" +
        "                    </select></div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Степень родства is required.</div>\n" +
        "                    <div class=\"col-md-4 mb-3\"><label for=\"id_birthday\">Дата рождения</label><input type=\"date\"\n" +
        "                                                                                                    name=\"birthday\"\n" +
        "                                                                                                    value=\"\"\n" +
        "                                                                                                    class=\"form-control\"\n" +
        "                                                                                                    id=\"id_birthday\">\n" +
        "                    </div>\n" +
        "                    <div class=\"invalid-feedback\">Valid Дата рождения is required.</div>\n" +
        "                </div>" +
        "<button type=\"button\" onclick=\"deleteChild('" + newdiv.id.toString() + "')\" class=\"btn btn-outline-primary\">-</button>";
    childDiv.appendChild(newdiv);
    counter++;
}

function deleteChild(elemId) {
    console.log("id to delete: " + elemId);
    let elementById = document.getElementById(elemId);
    console.log("elem to delete: " + elementById);

    var parentContainer = elementById.parentNode;
    console.log("parentContainer: " + parentContainer);
    return parentContainer.removeChild(elementById)
    console.log("remove was ok");

    // childContainer2.removeChild(childContainer);
}

function createInputIfOther(elem, selectedIndex) {
    // use one of possible conditions
    // if (elem.value == 'Other')
    console.log('createInputIfOther start');
    var selectedValue = elem.options[selectedIndex].text;
    console.log(elem);
    console.log('selectedValue: ' + selectedValue);
    if (selectedValue == "иное") {
        // document.getElementById("other-div").style.display = 'block';
    } else {
        // document.getElementById("other-div").style.display = 'none';
    }
    console.log('createInputIfOther end');

}

function showIpotekaForm(elem) {
    var selectedValue = elem.options[elem.selectedIndex].text;
    if (selectedValue === 'Ипотечный') {
        console.log('selectedValue === Ипотечный');
        var ipotekaForm = document.getElementById('creditForm');
        // if (actualAddressField) {
        //     actualAddressField.style = 'display: none'
        // }
    } else {
        // console.log('Адрес регистрации не совпадает с адресом проживания');
        // var actualAddressField = document.getElementById('actualAddress_');
        // if (actualAddressField) {
        //     actualAddressField.style = ''
        // } else {
        // }
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
        }
    }
}

function rentalPropertyForm() {
    console.log('rentalPropertyForm()');
    return;
}