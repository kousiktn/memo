function search(form) {
  var search_results_div = $('#search-results');
  var contains = form.memo_contains.value;
  var date = form.memo_date.value;
  var memo_with = form.memo_with.value;

  search_results_div.hide();
  $.ajax({
    type: 'GET',
    url: '/search-notes',
    data: {
      contains: contains,
      date: date,
      with: memo_with,
    },
    success: function(memos) {
      var result_div_content = `<div class="col-6 offset-md-3"><br><hr><br>`;
      var memo_content = "";
      for (var i in memos) {
        for (var j in memos[i][1]) {
          var memo = memos[i][1][j];
          var search_res_card = `<div class="card" onclick="show_memo(${memo.id})">`;
          if (memo.image) {
            search_res_card += `<img class="card-img-top" src="${memo.image}" /><hr>`
          }
          if (memo.notes) {
            search_res_card += `<div class="card-text" style="margin-top: 15px; margin-bottom: 15px; margin-left: 12px; margin-right: 12px">`;
            search_res_card += memo.notes;
            search_res_card += "</div>";
          }
          search_res_card += "</div><br>";
          memo_content += search_res_card;
        }
      }

      if (memo_content.length > 0) {
        result_div_content += 'Search results:<br><br>';
        result_div_content += memo_content;
      } else {
        result_div_content += 'No results found!';
      }
      result_div_content += "</div>";
      
      search_results_div.html(result_div_content);
      search_results_div.show();
    },
    error: function(err) {
      var error_message = 'Search Error: ' + err.responseText;
      var error_html = `<div class="col-6 offset-md-3"><br><hr><br>`;
      error_html += `<div class="alert alert-danger" role="alert" id="form_error">${error_message}</div>`;
      error_html += '</div>';
      search_results_div.html(error_html);
      search_results_div.show();
    },
  });
  return false;
}

$(document).ready(function() {
  var search_results=$('#search-results');
  search_results.hide();
 
  var date_input=$('#memo-date'); //our date input has the name "date"
  var options={
    format: 'yyyy-mm-dd',
    todayHighlight: true,
    autoclose: true,
    orientation: 'top right',
  };

  date_input.datepicker(options);

  $('#memo-contains').keypress(function( e ) {
    if (e.which === 32) {
      return false;
    }
  });
});
