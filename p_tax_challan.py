from pyfcm import FCMNotification
from flask import Flask, request, jsonify, json,render_template
from flask_api import status
from jinja2._compat import izip
from jinja2 import Environment, FileSystemLoader
from datetime import datetime,timedelta,date
import pymysql
from smtplib import SMTP
from flask_cors import CORS, cross_origin
from flask import Blueprint
from flask_restplus import Api, Resource, fields
from werkzeug.utils import cached_property
from werkzeug.datastructures import FileStorage
from werkzeug import secure_filename
import requests
import calendar
import json
from instamojoConfig import CLIENT_ID,CLIENT_SECRET,referrer
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os
import hashlib
import random, string
import math
from datetime import datetime
import boto3
from botocore.config import Config

p_tax_challan = Blueprint('p_tax_challan_api', __name__)
api = Api(p_tax_challan,  title='Dms API',description='DMS API')
name_space = api.namespace('pTaxChallan',description='Dms Section')

#----------------------database-connection---------------------#

def mysql_connection():
	connection = pymysql.connect(host='dms-project.cdcuaa7mp0jm.us-east-2.rds.amazonaws.com',
	                             user='admin',
	                             password='nIfnIEUwhlw0ZNQSpofJ',
	                             db='dms_project',
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)
	return connection

#----------------------database-connection---------------------#

read_from_file_and_save_postmodel = api.model('read_from_file_and_save_postmodel', {	
	"request_no":fields.Integer,
	"documentName":fields.String,
	"file_path":fields.String
})

#----------------------Read-From-Text-File-And-Save-Into-Database--------------------#

@name_space.route("/readFromFileDataAndSave")	
class readFromFileDataAndSave(Resource):
	@api.expect(read_from_file_and_save_postmodel)
	def post(self):

		connection = mysql_connection()
		cursor = connection.cursor()

		details = request.get_json()

		inputFile = open(details['file_path'])
		request_no = details['request_no']
		documentName = details['documentName']

		file_name = documentName.split('/')
		uploading_file_name = file_name[1]

		get_query = ("""SELECT *
			FROM `uploading_track_details` WHERE `request_no` = %s and `uploadig_file_name` = %s""")
		getData = (details['request_no'],uploading_file_name)
		count_track_details = cursor.execute(get_query,getData)
		
		uploading_track_details = cursor.fetchone()		
		uploading_track_details_id = uploading_track_details['uploading_track_details_id']
		last_update_id = uploading_track_details['last_update_id']

		grn_key = 0
		grn_data = ''
		payment_mode_key = 0
		payment_mode_data = ''
		grn_date_key = 0
		grn_date_data = ''
		bank_gateway_key = 0
		bank_gateway_data = ''
		brn_key = 0
		brn_data = ''
		brn_date_key = 0
		brn_date_data = ''
		payment_status_key = 0 
		payment_status_data = ''
		payment_ref_key = 0
		payment_ref_data = ''
		depositor_name_key = 0
		depositor_name_data = ''
		address_key = 0
		address_data = ''
		mobile_key = 0
		mobile_data = ''
		email_key = 0
		email_data = ''
		depositor_status_key = 0
		depositor_status_data = ''
		period_from_key = 0 
		period_from_data = ''
		period_to_key = 0
		period_to_data = ''
		payment_id_key = 0
		payment_id_data = ''
		payment_ref_id_key = 0
		payment_ref_id_data = ''
		sl_no_key = 0
		sl_no_data = ''
		head_of_account_description_key = 0
		head_of_account_description_data = ''
		head_of_account_key = 0
		head_of_account_data = ''
		amount_key = 0
		amount_data = ''


		for key,data in enumerate(inputFile):
			if "GRN:" in data:
				grn_key = key+1
				payment_mode_key = key+3
			if "GRN Date:" in data:
				grn_date_key = key+1
			if "Bank/Gateway:" in data:
				bank_gateway_key = key+1
			if "BRN :" in data:
				brn_key = key+1
			if "BRN Date:" in data:
				brn_date_key = key+1
			if "Payment Status:" in data:
				payment_status_key = key+1
			if "Payment Ref. No:" in data:
				payment_ref_key = key+1
				depositor_name_key = key+5
			if "Address:" in data:
				address_key = key+1		
			if "Mobile:" in data:
				mobile_key = key+1	
			if "EMail:" in data:
				email_key = key+1
			if "Depositor Status:" in data:
				depositor_status_key = key+1
			if "Period From (dd/mm/yyyy):" in data:
				period_from_key = key+1
			if "Period To (dd/mm/yyyy):" in data:
				period_to_key = key+1
			if "Payment ID:" in data:
				payment_id_key = key+1
			if "Payment Ref ID:" in data:
				payment_ref_id_key = key+1
			if "SI. No." in data:
				sl_no_key = key+6
				head_of_account_description_key = key+8
				head_of_account_key = key+9
				amount_key = key+10


			if grn_key == key:
				grn_data = data
			if payment_mode_key == key:
				payment_mode_data = data
			if grn_date_key == key:
				grn_date_data = data
			if bank_gateway_key == key:
				bank_gateway_data = data
			if brn_key == key:
				brn_data = data
			if brn_date_key == key:
				brn_date_data = data
			if payment_status_key == key:
				payment_status_data = data
			if payment_ref_key == key:
				payment_ref_data = data
			if address_key == key:
				address_data = data
			if mobile_key == key:
				mobile_data = data
			if email_key == key:
				email_data = data
			if depositor_status_key == key:
				depositor_status_data = data
			if period_from_key == key:
				period_from_data = data
			if period_to_key == key:
				period_to_data = data
			if payment_id_key == key:
				payment_id_data = data
			if payment_ref_id_key == key:
				payment_ref_id_data = data
			if sl_no_key == key:
				sl_no_data = data
			if head_of_account_description_key == key:
				head_of_account_description_data = data
			if head_of_account_key == key:
				head_of_account_data = data
			if amount_key == key:
				amount_data = data

		print(grn_data)
		print(payment_mode_data)
		print(grn_date_data)
		print(bank_gateway_data)
		print(brn_data)
		print(payment_status_data)
		print(payment_ref_data)
		print(depositor_name_data)
		print(address_data)
		print(mobile_data)
		print(email_data)
		print(depositor_status_data)
		print(period_from_data)
		print(period_to_data)
		print(payment_id_data)
		print(payment_ref_id_data)
		print(sl_no_data)
		print(head_of_account_description_data)
		print(head_of_account_data)
		print(amount_data)

		insert_query = ("""INSERT INTO `p_tax_challan_data`(`grn`,`payment_mode`,`grn_date`,`bank_gateway`,`brn`,`brn_date`,`payment_status`,`payment_ref_no`,`depositors_name`,`adress`,`mobile`,`email`,`depositor_status`,`period_from`,`period_to`,`payment_id`,`payment_ref_id`,`sl.No`,`paymnet_id`,`head_of_a/c_description`,`head_of_ac`,`amount`,`uploading_track_details_id`,`last_update_id`) 
								VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
		data = (grn_data,payment_mode_data,grn_date_data,bank_gateway_data,brn_data,brn_date_data,payment_status_data,payment_ref_data,depositor_name_data,address_data,mobile_data,email_data,depositor_status_data,period_from_data,period_to_data,payment_id_data,payment_ref_id_data,sl_no_data,payment_id_data,head_of_account_description_data,head_of_account_data,amount_data,uploading_track_details_id,last_update_id)
		cursor.execute(insert_query,data)
		print(cursor._last_executed)

		uploading_data_into_database = 1
		
		update_query = ("""UPDATE `uploading_track_details` SET `uploading_data_into_database` = %s WHERE `uploading_track_details_id` = %s""")
		update_data = (uploading_data_into_database,uploading_track_details_id)
		cursor.execute(update_query,update_data)

		connection.commit()
		cursor.close()

		return ({"attributes": {
				    "status_desc": "esic_payment_details",
				    "status": "success"
				},
				"responseList":details}), status.HTTP_200_OK

#----------------------Read-From-Text-File-And-Save-Into-Database--------------------#


		
