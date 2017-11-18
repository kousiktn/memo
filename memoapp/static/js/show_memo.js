function show_memo(memo_id) {
	$.ajax({
		type: 'GET',
		url: `/get-memo/${memo_id}`,
		success: function(memo) {
			$('#modal-title').html(`Memo on ${memo.date}`);
			var modal_body = '';
			const has_image = Boolean(memo.image);
			const has_notes = Boolean(memo.notes);
			const has_attendees = Boolean(memo.with.length);
			if (has_image) {
				modal_body += `<img src=${memo.image} style="max-width: 100%; max-height: 100%;"></img><br><br>`;
			}
			if (has_notes) {
				if (has_image) {
					modal_body += '<hr>';
				}
				modal_body += `<p>${memo.notes}</p>`;
			}

			if (has_attendees) {
				if (has_notes || has_image) {
					modal_body += '<hr>';
				}
				modal_body += `<footer>Attendees: ${memo.with}</footer>`;
			}
			$('#modal-body').html(modal_body);
			$('#popup-modal').modal('show');
		},
	});
}
