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
import xlrd

tds_payment = Blueprint('tds_payment_api', __name__)
api = Api(tds_payment,  title='Dms API',description='DMS API')
name_space = api.namespace('tdsPayment',description='Dms Section')

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


@name_space.route("/readFromFileDataAndSave")	
class readFromFileDataAndSave(Resource):
	@api.expect(read_from_file_and_save_postmodel)
	def post(self):
		connection = mysql_connection()
		cursor = connection.cursor()

		details = request.get_json()
		loc = ("TDS STATEMENT- APR-20 _FINAL.xls")

		wb = xlrd.open_workbook(loc)
		sheet = wb.sheet_by_index(0)
		'''sheet.cell_value(0, 0)
		tan_data = sheet.cell_value(2, 1)
		split_tan_data = tan_data.split()
		tan_data = split_tan_data[2]
		print(tan_data)
		contactor_section = sheet.cell_value(5, 3)
		print(contactor_section)'''

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

		i = 3

		while i <= 9:
		    i += 1
		    nature_of_the_payment = sheet.cell_value(i, 2)
		    section = sheet.cell_value(i, 3)
		    company = sheet.cell_value(i, 4)
		    interest = sheet.cell_value(i, 5)
		    total = sheet.cell_value(i, 6)
		    non_company = sheet.cell_value(i, 7)
		    grand_total = sheet.cell_value(i, 9)
		    '''print(nature_of_the_payment)
		    print(section)
		    print(company)
		    print(interest)
		    print(total)
		    print(non_company)
		    print(grand_total)'''

		    insert_query = ("""INSERT INTO `tds_payment_data`(`nature_of_the_payment`,`section`,`company`,`interest`,`total`,`non_company`,`grand_total`,
								`uploading_track_details_id`,`last_update_id`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

		    data = (nature_of_the_payment,section,company,interest,total,non_company,grand_total,uploading_track_details_id,last_update_id)

		    cursor.execute(insert_query,data)
		    print(cursor._last_executed)

				
		
		for j in range(14,sheet.nrows):	
					
			pan_no = sheet.cell_value(j, 0)
			date = sheet.cell_value(j, 1)
			name_of_deductee = sheet.cell_value(j, 2)
			section = sheet.cell_value(j, 3)
			status_of_deduction = sheet.cell_value(j, 4)
			rate = sheet.cell_value(j, 5)
			bill_amount = sheet.cell_value(j, 6)
			tds_amount = sheet.cell_value(j, 7)
			pan_available = sheet.cell_value(j, 8)
			total_amount = sheet.cell_value(j, 9)
			
			insert_query = ("""INSERT INTO `tds_payment_deduction_details_data`(`pan_no`,`date`,`name_of_deductee`,`section`,`status_of_deduction`,
		    	`rate`,`bill_amount`,`tds_amount`,`pan_available`,`total_amount`,`uploading_track_details_id`,`last_update_id`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
			
			data = (pan_no,date,name_of_deductee,section,status_of_deduction,rate,bill_amount,tds_amount,pan_available,total_amount,uploading_track_details_id,last_update_id)

			cursor.execute(insert_query,data)

			print(cursor._last_executed)

		uploading_data_into_database = 1
			
		update_query = ("""UPDATE `uploading_track_details` SET `uploading_data_into_database` = %s WHERE `uploading_track_details_id` = %s""")
		update_data = (uploading_data_into_database,uploading_track_details_id)
		cursor.execute(update_query,update_data)
			

		connection.commit()
		cursor.close()

		return ({"attributes": {
				    "status_desc": "tds_payment_details",
				    "status": "success"
				},
				"responseList":details}), status.HTTP_200_OK

		    

		
 
		