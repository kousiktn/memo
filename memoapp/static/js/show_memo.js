function show_memo(memo_id) {
	var converter = new showdown.Converter();
	$.ajax({
		type: 'GET',
		url: `/get-memo/?id=${memo_id}`,
		success: function(memo) {
			$('#modal-title').html(`Memo on ${memo.date}`);
			var modal_body_text = '';
			const has_image = Boolean(memo.image);
			const has_notes = Boolean(memo.notes);
			const has_attendees = Boolean(memo.with) && Boolean(memo.with.length);
			if (has_image) {
				modal_body_text += `<img src=${memo.image} style="max-width: 100%; max-height: 100%;"></img><br><br>`;
			}
			if (has_notes) {
				if (has_image) {
					modal_body_text += '<hr>';
				}
				modal_body_text += `<p>${memo.notes}</p>`;
			}

			if (has_attendees) {
				if (has_notes || has_image) {
					modal_body_text += '<hr>';
				}
				modal_body_text += `<footer>Attendees: ${memo.with}</footer>`;
			}

			// pfft clean up data here
			modal_body_text = modal_body_text.replace('<p>', '').replace('</p>', '');

    		var markdown_formatted_html = converter.makeHtml(modal_body_text);
			$('#modal-body').html(markdown_formatted_html);
			$('#popup-modal').modal('show');
		},
	});
}
