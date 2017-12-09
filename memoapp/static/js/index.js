// function readFile(image_file, callback) {
//   var reader = new FileReader();
//   reader.onload = function() {
//     var image_file_content = reader.result;
//     callback(image_file_content);
//   };

//   try {
//     reader.readAsBinaryString(image_file);
//   } catch(err) {
//     callback(null);
//   }
// }

function hide_all_messages() {
  var error = $('#form_error');
  var success = $('#form_success');

  success.hide();
  error.hide();
}

function show_success(msg) {
  var error = $('#form_error');
  error.hide();

  var success = $('#form_success');
  success.html(msg);
  success.show();
}

function show_error(msg) {
  var success = $('#form_success');
  success.hide();

  var error = $('#form_error');
  error.html(msg);
  error.show();
}

function create_memo(theForm) {
  hide_all_messages();

  var notes = theForm.memo_notes.value;
  var notes_date = theForm.memo_date.value;

  if (!notes) {
    show_error('Error! You should provide notes content');
  } else {
    var data = {
      "memo-notes": notes,
      "memo-date": notes_date,
      "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]')[0].value,
    };

    $.ajax({
      type: "POST",
      url: '/create-memo',
      data: data,
      success: function() {
        show_success('Memo created!');
        theForm.reset();
      },
      error: function(e) {
        show_error("Error: " + e.responseText);
      }
    });
  }

  return false;
}

$(document).ready(function() {
  hide_all_messages();

  var date_input=$('#memo-date'); //our date input has the name "date"
  var d = new Date();
  date_input.attr('value', d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate());

  var container=$('.bootstrap-iso form .form-group .col-sm-10').length>0 ? $('.bootstrap-iso form').parent() : "body";
  var options={
    format: 'yyyy-mm-dd',
    container: container,
    todayHighlight: true,
    autoclose: true,
    orientation: 'top right',
  };

  date_input.datepicker(options);
})
