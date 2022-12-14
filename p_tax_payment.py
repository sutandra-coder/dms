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

p_tax_payment = Blueprint('p_tax_payment_api', __name__)
api = Api(p_tax_payment,  title='Dms API',description='DMS API')
name_space = api.namespace('pTaxPayment',description='Dms Section')

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

		name_of_the_depositor_key = 0
		name_of_the_depositor_data = ''
		challan_amount_key = 0
		challan_amount_data = ''
		challan_amount_extension_key = 0
		challan_amount_extension_data = ''
		goverment_ref_no_key = 0
		goverment_ref_no_data = ''
		bank_reference_number_key = 0
		bank_reference_number_data = ''
		transaction_date_and_time_key = 0
		transaction_date_time_data = ''

		for key,data in enumerate(inputFile):
			if "Name of The Depositor" in data:
				name_of_the_depositor_key = key+1
			if "Challan Amount" in data:
				challan_amount_key = key+1
				challan_amount_extension_key = key+2
			if "Government Reference No" in data:
				goverment_ref_no_key = key+1
			if "Bank Reference Number ( Net Banking)" in data:
				bank_reference_number_key = key+1
			if "Transaction Date and Time" in data:
				transaction_date_and_time_key = key+1

			if name_of_the_depositor_key == key:
				name_of_the_depositor_data = data
			if challan_amount_key == key:
				challan_amount_data = data
			if challan_amount_extension_key == key:
				challan_amount_extension_data = data
			if goverment_ref_no_key == key:
				goverment_ref_no_data = data
			if bank_reference_number_key == key:
				bank_reference_number_data = data
			if transaction_date_and_time_key == key:
				transaction_date_time_data = data

		print(name_of_the_depositor_data)
		challan_amount_data = challan_amount_data+challan_amount_extension_data
		print(challan_amount_data)
		print(goverment_ref_no_data)
		print(bank_reference_number_data)
		print(transaction_date_time_data)

		insert_query = ("""INSERT INTO `p_tax_payment_data`(`name_of_the_depositor`,`challan_amount`,`goverment_ref_no`,`bank_ref_no`,`transaction_date_time`,`uploading_track_details_id`,`last_update_id`) 
								VALUES(%s,%s,%s,%s,%s,%s,%s)""")
		data = (name_of_the_depositor_data,challan_amount_data,goverment_ref_no_data,bank_reference_number_data,transaction_date_time_data,uploading_track_details_id,last_update_id)
		cursor.execute(insert_query,data)
		print(cursor._last_executed)

		uploading_data_into_database = 1
		
		update_query = ("""UPDATE `uploading_track_details` SET `uploading_data_into_database` = %s WHERE `uploading_track_details_id` = %s""")
		update_data = (uploading_data_into_database,uploading_track_details_id)
		cursor.execute(update_query,update_data)

		connection.commit()
		cursor.close()

		connection.commit()
		cursor.close()

		return ({"attributes": {
				    "status_desc": "p_tax_payment_details",
				    "status": "success"
				},
				"responseList":details}), status.HTTP_200_OK

#----------------------Read-From-Text-File-And-Save-Into-Database--------------------#


		
