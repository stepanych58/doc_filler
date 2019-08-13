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

function generateReport(message) {
    console.log(message)
    csrftoken = getCookie('csrftoken')
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/generateReport/", true)
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    var generateTemplateContext = JSON.stringify({mes: message});;
    cl_checkboxes = document.getElementsByName('cl_checked');
    console.log(cl_checkboxes)
   var checkedClients = [];
    cl_checkboxes.forEach(function (element) {
      console.log(element)
      if (element.checked)
      {
        console.log('checked: ' + element.value)
        checkedClients.push(String(element.value) )
      }
    })
   console.log(checkedClients)
    xhr.send(checkedClients)
}