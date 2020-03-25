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

function addIfChecked(checkedClients) {
    return function (element) {
        if (element.checked) {
            checkedClients.push(String(element.value))
        }
    };
}

function generateReport() {
    csrftoken = getCookie('csrftoken')//in future we can change name of cookie
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/generateReport/")
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Location", '/clients/');
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    cl_checkboxes = document.getElementsByName('cl_checked');
    doc_checkboxes = document.getElementsByName('doc_checked');
    var checkedClients = [];
    var checkedDocs = [];
    cl_checkboxes.forEach(addIfChecked(checkedClients))
    doc_checkboxes.forEach(addIfChecked(checkedDocs))
    var viewParams = JSON.stringify({
        'checkedClients': checkedClients,
        'checkedDocs': checkedDocs
    });
    console.log(viewParams)
    xhr.send(viewParams)
    xhr.onreadystatechange = function () {
        location = location //to reload page
    }
}

function deleteChecked() {
    csrftoken = getCookie('csrftoken')//in future we can change name of cookie
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/deleteChecked/")
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("Location", '/clients/');
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    cl_checkboxes = document.getElementsByName('cl_checked');
    doc_checkboxes = document.getElementsByName('doc_checked');
    var checkedClients = [];
    var checkedDocs = [];
    cl_checkboxes.forEach(addIfChecked(checkedClients))
    doc_checkboxes.forEach(addIfChecked(checkedDocs))
    var viewParams = JSON.stringify({
        'checkedClients': checkedClients,
        'checkedDocs': checkedDocs
    });
    console.log(viewParams)
    xhr.send(viewParams)
    xhr.onreadystatechange = function () {
        location = location //to reload page
    }
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
    if (!selectedIndex) {
        let chosedElem = elem.options[elem.selectedIndex];
        let parentNode = elem.parentNode;
        let otherId = elem.id + '_other';
        otherInput = undefined
        for (const child of parentNode.children) {
            if (child.id == otherId) {
                otherInput = child;
                break;
            }
        }
        if (chosedElem.text === 'Иное') {
            if (!otherInput) {
                otherInput = document.createElement('input')
                otherInput.type = 'text'
                otherInput.id = otherId
                otherInput.setAttribute('class', 'form-control')
                parentNode.appendChild(otherInput)
            } else {
                otherInput.setAttribute('style', '')
            }
        } else if (chosedElem.text != 'Иное' && otherInput) {
            otherInput.setAttribute('style', 'display:none')
        }
    } else {
        var selectedValue = elem.options[selectedIndex].text;
        console.log(elem);
        console.log('selectedValue: ' + selectedValue);
        if (selectedValue == "иное") {
            // document.getElementById("other-div").style.display = 'block';
        } else {
            // document.getElementById("other-div").style.display = 'none';
        }
    }
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

function showFactAddressForm(elem, id) {
    var selectedValue = elem.options[elem.selectedIndex].text;
    var actualAddressField = document.getElementById(id);
    if (selectedValue === 'Да') {
        // console.log('Адрес регистрации совпадает с адресом проживания');
        if (actualAddressField) {
            actualAddressField.style = 'display: none'
        }
    } else {
        // console.log('Адрес регистрации не совпадает с адресом проживания');
        if (actualAddressField) {
            actualAddressField.style = ''
        }
    }
}

var counter = 0;

function cloneCreditForm(elem) {
    var ipotekaForm = document.getElementById('ipotekaForm')
    var ipotekaFormClone = ipotekaForm.cloneNode(true)
    for (var formLabel of ipotekaFormClone.getElementsByTagName('label')) {
        var formLabelFOR = formLabel.getAttribute('for')
        formLabelFOR = formLabelFOR.replace(new RegExp('id_', 'g'), '')
        ipotekaFormClone.innerHTML = ipotekaFormClone.innerHTML.replace(new RegExp(formLabelFOR, 'g'), formLabelFOR.concat(counter))
    }
    ipotekaForm.parentNode.appendChild(ipotekaFormClone);
    counter++;
}

function rentalPropertyForm() {
    console.log('rentalPropertyForm()');
    return;
}

function check(name)
{
 var check=document.getElementsByName(name);
 for(var i=0;i<check.length;i++)
 {
  if(check[i].type=='checkbox')
  {
   check[i].checked=true;
  }
 }
}


function uncheck(name)
{
 var uncheck=document.getElementsByName(name);
 for(var i=0;i<uncheck.length;i++)
 {
  if(uncheck[i].type=='checkbox')
  {
   uncheck[i].checked=false;
  }
 }
}

function checkUncheck(name) {
    var chk=document.getElementsByName(name)
    if (chk.id=='1'){
        uncheck(name)
        chk.id = '2'
    }
    else{
        check(name)
        chk.id = '1'
    }


}
