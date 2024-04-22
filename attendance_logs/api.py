import requests
import xml.etree.ElementTree as ET
import json
import frappe
from frappe import _

@frappe.whitelist()
def sync_records(from_date,to_date):
	url = "http://smb.esslhost.com/smb.asmx"

	SOAPEnvelope = f""" 
			<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
			<soap:Body>
				<GetDeviceLogs xmlns="http://tempuri.org/">
				<FromDate>{from_date}</FromDate>
				<ToDate>{to_date}</ToDate>
				<clientId>2191211</clientId>
				<clientSeceret>SMB@2023</clientSeceret>
				</GetDeviceLogs>
			</soap:Body>
			</soap:Envelope>"""

	options = {
		"Content-type": "text/xml; text/xml; charset=utf-8"
	}

	response = requests.post(url, data = SOAPEnvelope, headers=options )

	root = ET.fromstring(response.text)

	res = ""
	for child in root.iter("{http://tempuri.org/}GetDeviceLogsResult"):
		res = json.loads(child.text)
	
	status = res['status']
	print(status)
	if status:
		data = res['data']
		data = json.loads(data)
		for log in data:
			new_att_log = frappe.new_doc("Attendance Logs")
			new_att_log.devicelogid = log["DeviceLogId"]
			new_att_log.deviceid = log["DeviceId"]
			new_att_log.userid = log["UserId"]
			new_att_log.logdate = log["LogDate"]
			new_att_log.direction = log["Direction"]
			new_att_log.attdirection = log["AttDirection"]
			new_att_log.alternateattdirection = log["AlternateAttDirection"]
			new_att_log.employeename = log["EmployeeName"]
			new_att_log.employeecode = log["EmployeeCode"]
			new_att_log.devicefname = log["DeviceFName"]
			new_att_log.devicesname = log["DeviceSName"]
			new_att_log.serialnumber = log["SerialNumber"]
			new_att_log.save()

		frappe.msgprint(_("Records Synced Successfully"))
	else:
		frappe.msgprint(_("Date format is not valid"))		
