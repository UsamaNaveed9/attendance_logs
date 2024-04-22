// Copyright (c) 2024, Usama and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Logs Sync', {
	sync_records: function(frm) {
		frappe.call({
			method:"attendance_logs.api.sync_records",
			args: {
				from_date: cur_frm.doc.from_date,
				to_date: cur_frm.doc.to_date
			},
			callback: function(r) {
				
			}
		});
	}
});
