function readFile(image_file, callback) {
  var reader = new FileReader();
  reader.onload = function() {
    var image_file_content = reader.result;
    callback(image_file_content);
  };

  try {
    reader.readAsBinaryString(image_file);
  } catch(err) {
    callback(null);
  }
}

function create_memo(theForm) {
  var notes = theForm.memo_notes.value;
  var notes_with = theForm.memo_with.value;
  var notes_date = theForm.memo_date.value;
  var image_file = theForm.memo_image.files[0];

  readFile(image_file, function(image_file_content) {
    var error = $('#form_error');
    var success = $('#form_success');
    if (!(notes || image_file_content)) {
      error.html(
        'Error! You should either provide Notes or Attach an Image'
      );
      error.show();
    } else {
      error.hide();
      var data = {
        "memo-notes": notes,
        "memo-image": image_file_content,
        "memo-with": notes_with,
        "memo-date": notes_date,
        "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]')[0].value,
      };

      $.ajax({
        type: "POST",
        url: '/create-memo',
        data: data,
        success: function() {
          error.hide();
          success.html("Memo created!");
          success.show();
        },
        error: function(e) {
          success.hide();
          error.html("Error: " + e.responseText);
          error.show();
        }
      });
    }
  });
  return false;
}

$(document).ready(function() {
  var error = $('#form_error');
  var success = $('#form_success');
  error.hide();
  success.hide();

  var date_input=$('#memo-date'); //our date input has the name "date"
  var d = new Date();
  date_input.attr('value', d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate());

  var container=$('.bootstrap-iso form .form-group .col-sm-10').length>0 ? $('.bootstrap-iso form').parent() : "body";
  var options={
    format: 'yyyy-mm-dd',
    container: container,
    todayHighlight: true,
    autoclose: true,
  };

  date_input.datepicker(options);
})
