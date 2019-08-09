function post(path, params, method='post') {

  // The rest of this code assumes you are not using a library.
  // It can be made less wordy if you use one.
  const form = document.createElement('form');
  form.method = method;
  form.action = path;

  for (const key in params) {
    if (params.hasOwnProperty(key)) {
      const hiddenField = document.createElement('input');
      hiddenField.type = 'hidden';
      hiddenField.name = key;
      hiddenField.value = params[key];

      form.appendChild(hiddenField);
    }
  }

  document.body.appendChild(form);
  form.submit();
}






function generateReport(message) {
  cl_checkboxes = document.getElementsByName('cl_checked');

  // for (var i = 0; i < cl_checkboxes.length; i++)
  // {
  //   client_ch = cl_checkboxes[i];
    // var form = document.createElement("form");
    // form.setAttribute('method', 'POST') ;
    // form.setAttribute('action', '/generateReport/') ;
    // form.setAttribute('cl_ids', '/generateReport/') ;
    // form.setAttribute('data', 'csrfmiddlewaretoken={{csrf_token}}') ;
    // if(client_ch.checked)
    // {
    //   var input = document.createElement("input");
    //   input.setAttribute("type", "hidden");
    //   input.setAttribute("name", client_ch.name);
    //   input.setAttribute("value", client_ch.value);
    //   form.appendChild(input);
    // }
    // document.body.appendChild(form);
    // form.submit();
    // method = 'POST';
    // var form = document.createElement('form');
    // Move the submit function to another variable
    // so that it doesn't get overwritten.
    // form._submit_function_ = form.submit;
    //
    // form.setAttribute('method', method);
    // form.setAttribute('action', '/generateReport/');
    // form.setAttribute('target', '_blank');
    //
    // for(var i =0; i<cl_checkboxes.length; i++) {
    //   client_ch = cl_checkboxes[i];
    //   if(client_ch.checked){
    //     var hiddenField = document.createElement('input');
    //     hiddenField.setAttribute('type', 'hidden');
    //     hiddenField.setAttribute('name', client_ch.name);
    //     hiddenField.setAttribute('value', client_ch.value);
    //     form.appendChild(hiddenField);
    //   }
    // }
    // document.body.appendChild(form);
    // form._submit_function_();
  // }
}