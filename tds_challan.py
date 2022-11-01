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

tds_challan = Blueprint('tds_challan_api', __name__)
api = Api(tds_challan,  title='Dms API',description='DMS API')
name_space = api.namespace('tdsChallan',description='Dms Section')

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

		details = request.get_json()
		inputFile = open(details['file_path'])

		connection = mysql_connection()
		cursor = connection.cursor()
		
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

		name_of_the_assessee_key = 0
		name_of_the_assessee_data = ''
		complete_address_1_key = 0
		complete_address_1_data = ''
		complete_address_2_key = 0
		complete_address_2_data = ''
		complete_address_3_key = 0
		complete_address_3_data = ''
		complete_address = ''
		tan_key_1 = 0
		tan_data_1 = ''
		tan_key_2 = 0
		tan_data_2 = ''
		tan_key_3 = 0
		tan_data_3 = ''
		tan_key_4 = 0
		tan_data_4 = ''
		tan_key_5 = 0
		tan_data_5 = ''
		tan_key_6 = 0
		tan_data_6 = ''
		tan_key_7 = 0
		tan_data_7 = ''
		tan_key_8 = 0
		tan_data_8 = ''
		tan_key_9 = 0
		tan_data_9 = ''
		tan_key_10 = 0
		tan_data_10 = ''
		tan_data = ''
		major_head_key = 0
		major_head_data = ''
		minor_head_key = 0
		minor_kead_data = ''
		nature_of_the_payment_key = 0
		nature_of_the_payment_data = ''
		basic_tax_key = 0
		basic_tax_data = ''
		surcharge_key = 0
		surcharge_data = ''
		education_cess_key = 0
		education_cess_data = ''
		penalty_key = 0
		penalty_data = ''
		others_key = 0
		oters_data = ''
		interest_key = 0
		interest_data = ''
		fee_under_Sec_e_key = 0
		fee_under_Sec_e_data = ''
		total_key = 0
		total_data = ''
		challan_no_key = 0
		challan_no_data = ''
		bsr_code_key = 0
		bsr_code_data = ''
		date_of_receipt_key = 0
		date_of_receipt_data = '' 
		challan_serial_no_key = 0
		challan_serial_no_data = ''
		assessment_year_key = 0
		assessment_year_data = ''
		bank_reference_key = 0
		bank_reference_data = ''
		drawn_on_key = 0
		drawn_on_data = ''
		rupees_in_words_key = 0 
		rupees_in_words_data = ''
		cin_key = 0
		cin_data = ''
		debit_acount_no_key = 0
		debit_account_no_data = ''
		payment_realization_date_key = 0
		payment_realization_date_data = ''



		for key,data in enumerate(inputFile):
			if "Name of the Assessee" in data:
				name_of_the_assessee_key = key+1

			if "Complete Address" in data:
				complete_address_1_key = key+1
				complete_address_2_key = key+2
				complete_address_3_key = key+3

			if "TAN" in data:
				tan_key_1 = key+1
				tan_key_2 = key+2
				tan_key_3 = key+3
				tan_key_4 = key+4
				tan_key_5 = key+5
				tan_key_6 = key+6
				tan_key_7 = key+7
				tan_key_8 = key+8
				tan_key_9 = key+9
				tan_key_10 = key+10

			if "Major Head" in data:
				major_head_key = key+1
			if "Minor Head" in data:
				minor_head_key = key+1
			if "Nature of Payment" in data:
				nature_of_the_payment_key = key+1
			if "Basic Tax" in data:
				basic_tax_key = key+1
			if "Surcharge" in data:
				surcharge_key = key+1
			if "Education Cess" in data:
				education_cess_key = key+1
			if "Penalty" in data:
				penalty_key = key+1
			if "Others" in data:
				others_key = key+1
			if "Interest" in data:
				interest_key = key+1
			if "Fee Under Sec. 234 E" in data:
				fee_under_Sec_e_key = key+1
			if "TOTAL" in data:
				total_key = key+1
			if "Challan No" in data:
				challan_no_key = key+1
			if "BSR Code" in data:
				bsr_code_key = key+1
			if "Date of Receipt" in data:
				date_of_receipt_key = key+1
			if "Challan Serial No" in data:
				challan_serial_no_key = key+1
			if "Assessment Year" in data:
				assessment_year_key = key+1
			if "Bank Reference" in data:
				bank_reference_key = key+1
			if "Drawn On" in data:
				drawn_on_key = key+1
			if "Rupees (In words)" in data:
				rupees_in_words_key = key+1
			if "CIN" in data:
				cin_key = key+1
			if "Debit Account No." in data:
				debit_acount_no_key = key+1
				payment_realization_date_key = key+3


			if name_of_the_assessee_key == key:
				name_of_the_assessee_data = data
			if complete_address_1_key == key:
				complete_address_1_data = data
			if complete_address_2_key == key:
				complete_address_2_data = data
			if complete_address_3_key == key:
				complete_address_3_data = data
			if tan_key_1 == key:
				tan_data_1 = data.strip()
			if tan_key_2 == key:
				tan_data_2 = data.strip()
			if tan_key_3 == key:
				tan_data_3 = data.strip()
			if tan_key_4 == key:
				tan_data_4 = data.strip()
			if tan_key_5 == key:
				tan_data_5 = data.strip()
			if tan_key_6 == key:
				tan_data_6 = data.strip()
			if tan_key_7 == key:
				tan_data_7 = data.strip()
			if tan_key_8 == key:
				tan_data_8 = data.strip()
			if tan_key_9 == key:
				tan_data_9 = data.strip()
			if tan_key_10 == key:
				tan_data_10 = data.strip()
			if major_head_key == key:
				major_head_data = data
			if minor_head_key == key:
				minor_head_data = data
			if nature_of_the_payment_key == key:
				nature_of_the_payment_data = data
			if basic_tax_key == key:
				basic_tax_data = data
			if surcharge_key == key:
				surcharge_data = data
			if education_cess_key == key:
				education_cess_data = data
			if penalty_key == key:
				penalty_data = data
			if others_key == key:
				oters_data = data
			if interest_key == key:
				interest_data = data
			if fee_under_Sec_e_key == key:
				fee_under_Sec_e_data = data
			if total_key == key:
				total_data = data
			if challan_no_key == key:
				challan_no_data = data
			if bsr_code_key == key:
				bsr_code_data = data
			if date_of_receipt_key == key:
				date_of_receipt_data = data
			if challan_serial_no_key == key:
				challan_serial_no_data = data
			if assessment_year_key == key:
				assessment_year_data = data
			if bank_reference_key == key:
				bank_reference_data = data
			if drawn_on_key == key:
				drawn_on_data = data
			if rupees_in_words_key == key:
				rupees_in_words_data = data
			if cin_key == key:
				cin_data = data
			if debit_acount_no_key == key:
				debit_acount_no_data = data
			if payment_realization_date_key == key:
				payment_realization_date_data = data


		print(name_of_the_assessee_data)		
		complete_address = complete_address_1_data+""+complete_address_2_data+""+complete_address_3_data
		print(complete_address)		
		tan_data = tan_data_1+tan_data_2+tan_data_3+tan_data_4+tan_data_5+tan_data_6+tan_data_7+tan_data_8+tan_data_9+tan_data_10
		print(tan_data)
		print(major_head_data)
		print(minor_head_data)
		print(nature_of_the_payment_data)
		print(basic_tax_data)
		print(surcharge_data)
		print(education_cess_data)
		print(penalty_data)
		print(oters_data)
		print(interest_data)
		print(fee_under_Sec_e_data)
		print(total_data)
		print(challan_no_data)
		print(bsr_code_data)
		print(date_of_receipt_data)
		print(assessment_year_data)
		print(bank_reference_data)
		print(drawn_on_data)
		print(rupees_in_words_data)
		print(cin_data)
		print(debit_acount_no_data)
		print(payment_realization_date_data)

		insert_query = ("""INSERT INTO `tds_challan_data`(`name_of_the_assessee_data`,`complete_address`,`tan_data`,`major_head_data`,
			`minor_head_data`,`nature_of_the_payment_data`,
			`basic_tax_data`,`surcharge_data`,`education_cess_data`,`penalty_data`,`oters_data`,`interest_data`,`fee_under_Sec_e_data`,
			`total_data`,`challan_no_data`,`bsr_code_data`,`date_of_receipt_data`,`challan_serial_no_data`,`assessment_year_data`,`bank_reference_data`,`drawn_on_data`,
			`rupees_in_words_data`,`cin_data`,`debit_acount_no_data`,`payment_realization_date_data`,`uploading_track_details_id`,`last_update_id`) 
								VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
		data = (name_of_the_assessee_data,complete_address,tan_data,major_head_data,minor_head_data,nature_of_the_payment_data,
			basic_tax_data,surcharge_data,education_cess_data,penalty_data,oters_data,interest_data,fee_under_Sec_e_data,
			total_data,challan_no_data,bsr_code_data,date_of_receipt_data,challan_serial_no_data,assessment_year_data,bank_reference_data,drawn_on_data,
			rupees_in_words_data,cin_data,debit_acount_no_data,payment_realization_date_data,uploading_track_details_id,last_update_id)
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