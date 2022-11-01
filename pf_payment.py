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

pf_payment = Blueprint('pf_payment_api', __name__)
api = Api(pf_payment,  title='Dms API',description='DMS API')
name_space = api.namespace('pfPayment',description='Dms Section')

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

		trrn_key = 0
		trrn_data = ''
		challan_status_key = 0
		challan_status_daa = ''
		challan_generated_on_key = 0
		challan_generated_on_data = ''
		establishment_id_key = 0
		establishment_id_data = ''
		esablishment_name_key = 0
		esablishment_name_data = ''
		challan_type_key = 0
		challan_type_data = ''
		total_members_key = 0
		total_members_data = ''
		wages_month_key = 0
		wages_month_data = ''
		total_amount_rs_key = 0
		total_amount_rs_data = ''
		account_1_amount_rs_key = 0
		account_1_amount_rs_data = ''
		account_2_amount_rs_key = 0
		account_2_amount_rs_data = ''
		account_10_amount_rs_key = 0
		account_10_amount_rs_data = ''
		account_21_amount_rs_key = 0
		account_21_amount_rs_data = ''
		account_22_amount_rs_key = 0
		account_22_amount_rs_data = ''
		payment_confirmation_bank_key = 0
		payment_confirmation_bank_data = ''
		crn_key = 0
		crn_data = ''
		payment_date_key = 0
		payment_date_data = ''
		payment_confirmation_date_key = 0
		payment_confirmation_date_data = ''
		total_pmrpy_benefit_key = 0
		total_pmrpy_benefit_data = ''


		for key,data in enumerate(inputFile):
			if "TRRN No :" in data:
				trrn_key = key+1
			if "Challan Status :" in data:
				challan_status_key = key+1
			if "Challan Generated On :" in data:
				challan_generated_on_key = key+1
			if "Establishment ID :" in data:
				establishment_id_key = key+1
			if "Establishment Name :" in data:
				esablishment_name_key = key+1
			if "Challan Type :" in data:
				challan_type_key = key+1
			if "Wage Month :" in data:
				wages_month_key = key+1
			if "Total Amount (Rs) :" in data:
				total_amount_rs_key = key+1
			if "Account-1 Amount (Rs) :" in data:
				account_1_amount_rs_key = key+1
			if "Account-2 Amount (Rs) :" in data:
				account_2_amount_rs_key = key+1
			if "Account-10 Amount (Rs) :" in data:
				account_10_amount_rs_key = key+1
			if "Account-21 Amount (Rs) :" in data:
				account_21_amount_rs_key = key+1
			if "Account-22 Amount (Rs) :" in data:
				account_22_amount_rs_key = key+1
			if "Payment Confirmation Bank :" in data:
				payment_confirmation_bank_key = key+1
			if "CRN :" in data:
				crn_key = key+1
			if "Payment Date :" in data:
				payment_date_key = key+1
			if "Payment Confirmation Date :" in data:
				payment_confirmation_date_key = key+1
			if "Total PMRPY Benefit :" in data:
				total_pmrpy_benefit_key = key+1

			if trrn_key == key:
				trrn_data = data
			if challan_status_key == key:
				challan_status_data = data
			if challan_generated_on_key == key:
				challan_generated_on_data = data
			if establishment_id_key == key:
				establishment_id_data = data
			if esablishment_name_key == key:
				esablishment_name_data = data
			if challan_type_key == key:
				challan_type_data = data
			if wages_month_key == key:
				wages_month_data = data
			if total_amount_rs_key == key:
				total_amount_rs_data = data
			if account_1_amount_rs_key == key:
				account_1_amount_rs_data = data
			if account_2_amount_rs_key == key:
				account_2_amount_rs_data = data
			if account_10_amount_rs_key == key:
				account_10_amount_rs_data = data
			if account_21_amount_rs_key == key:
				account_21_amount_rs_data = data
			if account_22_amount_rs_key == key:
				account_22_amount_rs_data = data
			if payment_confirmation_bank_key == key:
				payment_confirmation_bank_data = data
			if crn_key == key:
				crn_data = data
			if payment_date_key == key:
				payment_date_data = data
			if payment_confirmation_date_key == key:
				payment_confirmation_date_data = data
			if total_pmrpy_benefit_key == key:
				total_pmrpy_benefit_data = data

		print(trrn_data)
		print(challan_status_data)		
		print(challan_generated_on_data)
		print(establishment_id_data)
		print(esablishment_name_data)
		print(challan_type_data)
		print(wages_month_data)
		print(total_amount_rs_data)
		print(account_1_amount_rs_data)
		print(account_2_amount_rs_data)
		print(account_10_amount_rs_data)
		print(account_21_amount_rs_data)
		print(account_22_amount_rs_data)
		print(payment_confirmation_bank_data)
		print(crn_data)
		print(payment_date_data)
		print(payment_confirmation_date_data)
		print(total_pmrpy_benefit_data)


		insert_query = ("""INSERT INTO `pf_payment_data`(`trrn_data`,`challan_status_data`,`challan_generated_on_data`,`establishment_id_data`,
			`esablishment_name_data`,`challan_type_data`,`wages_month_data`,
			`total_amount_rs_data`,`account_1_amount_rs_data`,`account_2_amount_rs_data`,
			`account_10_amount_rs_data`,`account_21_amount_rs_data`,`account_22_amount_rs_data`,`payment_confirmation_bank_data`,
			`crn_data`,`payment_date_data`,`total_pmrpy_benefit_data`,`uploading_track_details_id`,`last_update_id`) 
								VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
		data = (trrn_data,challan_status_data,challan_generated_on_data,establishment_id_data,esablishment_name_data,challan_type_data,wages_month_data,
			total_amount_rs_data,account_1_amount_rs_data,account_2_amount_rs_data,account_10_amount_rs_data,account_21_amount_rs_data,
			account_22_amount_rs_data,payment_confirmation_bank_data,crn_data,payment_date_data,total_pmrpy_benefit_data,
			uploading_track_details_id,last_update_id)
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
