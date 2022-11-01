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

dms_section = Blueprint('dms_section_api', __name__)
api = Api(dms_section,  title='Dms API',description='DMS API')
name_space = api.namespace('DmsSection',description='Dms Section')

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

user_postmodel = api.model('SelectUser', {	
	"user_name":fields.String,
	"phoneno":fields.String,
	"password":fields.String
})

user_login_postmodel = api.model('SelectUserLogin', {	
	"phoneno":fields.String,
	"password":fields.String
})

UploadingTrack_postmodel = api.model('UploadingTrack', {	
	"uploading_file_count":fields.Integer,
	"file_type":fields.String,
	"content_type":fields.String,
	"uploading_type":fields.String,
	"last_update_id":fields.Integer
})

convertjson_postmodel = api.model('convertjson_postmodel', {
	"document_name":fields.String,
	"user_id":fields.Integer,
	"request_no":fields.Integer
})

create_text_postmodel = api.model('create_text_postmodel', {	
	"request_no":fields.Integer,
	"key":fields.String,
	"job_id":fields.String,
	"documentName":fields.String
})

read_from_file_and_save_postmodel = api.model('read_from_file_and_save_postmodel', {	
	"request_no":fields.Integer,
	"documentName":fields.String,
	"file_path":fields.String
})

key_postmodel = api.model('key_postmodel', {	
	"job_id":fields.String
})

esic_table_putmodel = api.model('esic_table_putmodel',{
	"is_disable":fields.String,
	"ip_number":fields.String,
	"ip_name":fields.String,
	"no_of_days":fields.String,
	"total_wages":fields.String,
	"ip_contribution":fields.String,
	"reason":fields.String
})

esic_basic_putmodel = api.model('esic_basic_putmodel',{
	"history_no":fields.String,
	"challan_date":fields.String,
	"total_ip_contribution":fields.String,
	"total_employee_contribution":fields.String,
	"total_contribution":fields.String,
	"total_goverment_contribution":fields.String,
	"total_month_wages":fields.String
})

esic_table_postmodel = api.model('esic_table_postmodel',{
	"esic_basic_data_id":fields.Integer,
	"is_disable":fields.String,
	"ip_number":fields.String,
	"ip_name":fields.String,
	"no_of_days":fields.String,
	"total_wages":fields.String,
	"ip_contribution":fields.String,
	"reason":fields.String,
	"user_id":fields.Integer
})

esic_payment_putmodel = api.model('esic_payment_putmodel',{
	"transaction_status":fields.String,
	"employers_code_no":fields.String,
	"employers_name":fields.String,
	"challan_period":fields.String,
	"challan_number":fields.String,
	"challan_created_date":fields.String,
	"challan_submited_date":fields.String,
	"amount_paid":fields.String,
	"transaction_number":fields.String
})

ptax_challan_putmodel = api.model('ptax_challan_putmodel',{
	"grn":fields.String,
	"payment_mode":fields.String,
	"grn_date":fields.String,
	"bank_gateway":fields.String,
	"brn":fields.String,
	"brn_date":fields.String,
	"payment_status":fields.String,
	"payment_ref_no":fields.String,
	"depositors_name":fields.String,
	"adress":fields.String,
	"mobile":fields.String,
	"email":fields.String,
	"depositor_status":fields.String,
	"period_from":fields.String,
	"period_to":fields.String,
	"payment_id":fields.String,
	"payment_ref_id":fields.String,
	"slNo":fields.String,
	"paymnet_id":fields.String,
	"head_of_a/c_description":fields.String,
	"head_of_ac":fields.String,
	"amount":fields.String
})

ptax_payment_putmodel = api.model('ptax_payment_putmodel',{
	"name_of_the_depositor":fields.String,
	"challan_amount":fields.String,
	"goverment_ref_no":fields.String,
	"bank_ref_no":fields.String,
	"transaction_date_time":fields.String
})

pf_challan_putmodel = api.model('ptax_payment_putmodel',{
	"trn":fields.String,
	"establishment_code":fields.String,
	"establishment_name":fields.String,
	"address":fields.String,
	"total_subscribers_epf":fields.String,
	"total_subscribers_eps":fields.String,
	"total_subscribers_edli":fields.String,
	"total_wages_epf":fields.String,
	"total_wages_eps":fields.String,
	"total_wages_edli":fields.String,
	"administration_charges_ac_01":fields.String,
	"administration_charges_ac_02":fields.String,
	"administration_charges_ac_10":fields.String,
	"administration_charges_ac_21":fields.String,
	"administration_charges_ac_22":fields.String,
	"administration_charges_ac_total":fields.String,
	"employers_share_of_ac_01":fields.String,
	"employers_share_of_ac_02":fields.String,
	"employers_share_of_ac_10":fields.String,
	"employers_share_of_ac_21":fields.String,
	"employers_share_of_ac_22":fields.String,
	"employers_share_of_ac_total":fields.String,
	"employees_share_of_ac_01":fields.String,
	"employees_share_of_ac_02":fields.String,
	"employees_share_of_ac_10":fields.String,
	"employees_share_of_ac_21":fields.String,
	"employees_share_of_ac_22":fields.String,
	"employees_share_of_ac_total":fields.String,
	"ac_no_1_employer_share_rs_pmrpy_data":fields.String,
	"ac_no_1_employers_share_rs_pmgky_data":fields.String,
	"ac_no_1_employers_share_rs_pmgky_data":fields.String,
	"ac_no_10_Pension_fund_rs_pmrpy_data":fields.String,
	"ac_no_10_Pension_fund_rs_pmgky_data":fields.String,
	"ac_no_1_employee_share_rs_pmrpy_data":fields.String,
	"ac_no_1_employee_share_rs_pmgky_data":fields.String,
	"total_a_b_c_rs_pmrpy_data":fields.String,
	"total_a_b_c_rs_pmgky_data":fields.String,
	"grand_total":fields.String,
	"total_remittance_by_employer_rs":fields.String,
	"total_remittance_by_employer_rs_pmgky":fields.String,
	"total_amount_of_uploaded_ECR":fields.String,
	"due_for_the_wages_month_of_data":fields.String,
	"due_for_the_wages_year_of_data":fields.String
})

pf_payment_putmodel = api.model('ptax_payment_putmodel',{
	"trrn_data":fields.String,
	"challan_status_data":fields.String,
	"challan_generated_on_data":fields.String,
	"establishment_id_data":fields.String,
	"challan_type_data":fields.String,
	"wages_month_data":fields.String,
	"total_amount_rs_data":fields.String,
	"account_1_amount_rs_data":fields.String,
	"account_2_amount_rs_data":fields.String,
	"account_10_amount_rs_data":fields.String,
	"account_21_amount_rs_data":fields.String,
	"account_22_amount_rs_data":fields.String,
	"payment_confirmation_bank_data":fields.String,
	"crn_data":fields.String,
	"payment_date_data":fields.String,
	"payment_confirmation_date_data":fields.String,
	"total_pmrpy_benefit_data":fields.String
})

tds_challan_putmodel = api.model('tds_challan_putmodel',{
	"name_of_the_assessee_data":fields.String,
	"complete_address":fields.String,
	"tan_data":fields.String,
	"major_head_data":fields.String,
	"minor_head_data":fields.String,
	"nature_of_the_payment_data":fields.String,
	"basic_tax_data":fields.String,
	"surcharge_data":fields.String,
	"education_cess_data":fields.String,
	"penalty_data":fields.String,
	"oters_data":fields.String,
	"interest_data":fields.String,
	"fee_under_Sec_e_data":fields.String,
	"total_data":fields.String,
	"challan_no_data":fields.String,
	"bsr_code_data":fields.String,
	"date_of_receipt_data":fields.String,
	"challan_serial_no_data":fields.String,
	"assessment_year_data":fields.String,
	"bank_reference_data":fields.String,
	"drawn_on_data":fields.String,
	"rupees_in_words_data":fields.String,
	"cin_data":fields.String,
	"debit_acount_no_data":fields.String,
	"payment_realization_date_data":fields.String
})



upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
cors = CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ACCESS_KEY =  'AKIATWWALMDJAMSVRMK7'
SECRET_KEY = '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'


contributionHistoryFlag = "N"
firstTableFlag = "N"
secondTableFlag = "N"
readingFirstTable = "N"
readingSecondTable = "N"
secondTableDataIgnore = "Y"


# Generic Variables
fileLine = ""
lineNumber = 0
firstTableLineOffset = 0
secondTableLineOffset = 0
secondTableDataIgnore = "Y"

#----------------------Add-User---------------------#

@name_space.route("/AddUser")
class AddUser(Resource):
	@api.expect(user_postmodel)
	def post(self):
		connection = mysql_connection()
		cursor = connection.cursor()		
		details = request.get_json()

		user_name = details['user_name']
		phoneno = details['phoneno']
		password = details['password']

		insert_query = ("""INSERT INTO `user`(`user_name`,`phoneno`,`password`) 
								VALUES(%s,%s,%s)""")
		data = (user_name,phoneno,password)
		cursor.execute(insert_query,data)
		print(cursor._last_executed)
		user_id = cursor.lastrowid	

		details['user_id'] = user_id

		connection.commit()
		cursor.close()

		return ({"attributes": {
				    "status_desc": "user_details",
				    "status": "success"
				},
				"responseList":details}), status.HTTP_200_OK	

#----------------------Add-User---------------------#

#----------------------Login-User---------------------#

@name_space.route("/LoginUser")	
class LoginUser(Resource):
	@api.expect(user_login_postmodel)
	def post(self):		
		connection = mysql_connection()
		cursor = connection.cursor()

		details = request.get_json()

		get_query = ("""SELECT *
			FROM `user` WHERE `phoneno` = %s and `password` = %s""")
		getData = (details['phoneno'],details['password'])
		count_user = cursor.execute(get_query,getData)

		if count_user > 0:
			user_details = cursor.fetchone()
		else:
			user_details = {}

		return ({"attributes": {
				    "status_desc": "user_details",
				    "status": "success"
				},
				"responseList":user_details}), status.HTTP_200_OK

#----------------------Login-User---------------------#

@name_space.route("/UploadingTrack")
class UploadingTrack(Resource):
	@api.expect(UploadingTrack_postmodel)
	def post(self):
		connection = mysql_connection()
		cursor = connection.cursor()

		details = request.get_json()

		uploading_file_count = details['uploading_file_count']
		file_type = details['file_type']
		content_type = details['content_type']
		last_update_id = details['last_update_id']
		uploading_track_status = 1

		if details and "uploading_type" in details:
			uploading_type = details['uploading_type']
		else:
			uploading_type = "esic"	

		now = datetime.now()
		date_of_creation = now.strftime("%Y-%m-%d %H:%M:%S")

		insert_query = ("""INSERT INTO `uploading_track`(`uploading_file_count`,`file_type`,`content_type`,`status`,`uploading_type`,`last_update_id`,`last_update_ts`) 
								VALUES(%s,%s,%s,%s,%s,%s,%s)""")
		data = (uploading_file_count,file_type,content_type,uploading_track_status,uploading_type,last_update_id,date_of_creation)
		cursor.execute(insert_query,data)
		print(cursor._last_executed)
		request_no  = cursor.lastrowid	

		details['request_no'] = request_no

		connection.commit()
		cursor.close()


		return ({"attributes": {
				    "status_desc": "track_details",
				    "status": "success"
				},
				"responseList":details}), status.HTTP_200_OK


#----------------------Upload-To-S3-Bucket---------------------#

@name_space.route("/uploadToS3Bucket/<string:user_id>/<int:request_no>")
@name_space.expect(upload_parser)
class uploadToS3Bucket(Resource):
	def post(self,user_id,request_no):
		connection = mysql_connection()
		cursor = connection.cursor()

		bucket_name = "dms-project-bucket"
		s3 = boto3.client(
			"s3",
			aws_access_key_id=ACCESS_KEY,
			aws_secret_access_key=SECRET_KEY
			)
		bucket_resource = s3
		uploadedfile = request.files['file']
		print(uploadedfile)
		filename = ''
		userKey = user_id+'/'
		fpath = ''
		FileSize = None
		if uploadedfile:
			filename = secure_filename(uploadedfile.filename)
			keyname = userKey+filename
			uploadRes = bucket_resource.upload_fileobj(
				Bucket = bucket_name,
				Fileobj=uploadedfile,
				Key=keyname)
			print(uploadRes)
			# result = bucket_resource.list_objects(Bucket=bucket_name, Prefix=userKey)
			# absfilepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
			# # print(absfilepath)
			# uploadedfile.save(absfilepath)
			# 
			# uploadReq = (filename,absfilepath,keyname)
			# thread_a = Compute(uploadReq,'uploadToS3Bucket')
			# thread_a.start()

			file_type = filename.split('.')
			uploading_file_type = file_type[1]

			now = datetime.now()
			date_of_creation = now.strftime("%Y-%m-%d %H:%M:%S")

			s3_bucket_file_path = user_id+"/"+filename

			insert_query = ("""INSERT INTO `uploading_track_details`(`request_no`,`uploadig_file_name`,`uploading_file_type`,`uploading_into_s3_bucket`,`s3_bucket_file_path`,`last_update_id`,`last_update_ts`) 
								VALUES(%s,%s,%s,%s,%s,%s,%s)""")
			uploading_into_s3_bucket = 1
			data = (request_no,filename,uploading_file_type,uploading_into_s3_bucket,s3_bucket_file_path,user_id,date_of_creation)
			cursor.execute(insert_query,data)
			
			connection.commit()
			cursor.close()

			return {"attributes": {"status": "success"},
				"responseList": [{
				  "FileName": filename,
				  "FileSize": FileSize,
				  "FilePath": user_id+"/"+filename,
				  "request_no": request_no
				  }],
				"responseDataTO": {}
				}
		else:
			return {"attributes": {"status": "success"},
						"responseList": [],
						"responseDataTO": {}
					}

#----------------------Upload-To-S3-Bucket---------------------#

#----------------------Convert-Json-from-Uploading-File---------------------#

@name_space.route("/ConvetJsonFromUploadinFile")	
class ConvetJsonFromUploadinFile(Resource):
	@api.expect(convertjson_postmodel)
	def post(self):
		connection = mysql_connection()
		cursor = connection.cursor()

		details = request.get_json()

		s3BucketName = "dms-project-bucket"
		documentName = details['document_name']
		request_no = details['request_no']

		file_name = documentName.split('/')
		uploading_file_name = file_name[1]

		my_config = Config(
		    region_name = 'us-east-1'
		)
		

		textract = boto3.client('textract', config=my_config,aws_access_key_id=ACCESS_KEY,
			aws_secret_access_key=SECRET_KEY)

		print(textract)

		# Amazon Textract client


		# Call Amazon Textract
		response = textract.start_document_text_detection(
		    DocumentLocation={
		        'S3Object': {
		            'Bucket': s3BucketName,
		            'Name': documentName
		        }
		    },
		    NotificationChannel={
		        'SNSTopicArn': 'arn:aws:sns:us-east-1:732633173404:textract.fifo',
		        'RoleArn': 'arn:aws:iam::732633173404:role/@textract'
		    },
		    OutputConfig = { 
		      "S3Bucket": s3BucketName
		   }
		)
		print(response['JobId'])
		documnet_response = textract.get_document_text_detection(
			JobId=response['JobId'],
		    MaxResults=123
		)

		get_query = ("""SELECT *
			FROM `uploading_track_details` WHERE `request_no` = %s and `uploadig_file_name` = %s""")
		getData = (details['request_no'],uploading_file_name)
		count_track_details = cursor.execute(get_query,getData)

		if count_track_details > 0:
			converting_json_from_upoading_file = 1
			update_query = ("""UPDATE `uploading_track_details` SET `converting_json_from_upoading_file` = %s, `job_id` = %s
					WHERE `request_no` = %s and `uploadig_file_name` = %s""")
			update_data = (converting_json_from_upoading_file,response['JobId'],request_no,uploading_file_name)
			cursor.execute(update_query,update_data)

		key = "textract_output/"+response['JobId']+"/1"

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Convert-Json-from-Uploading-File",
								"status": "success"},
				"responseList": {"key":key,"documentName":documentName,"request_no":request_no,"JobId":response['JobId']}}), status.HTTP_200_OK

#----------------------Convert-Json-from-Uploading-File---------------------#


#----------------------Check-key-Is-Exsits--------------------#

@name_space.route("/checkKeyIsExsits")	
class checkKeyIsExsits(Resource):
	@api.expect(key_postmodel)
	def post(self):
		connection = mysql_connection()
		cursor = connection.cursor()

		details = request.get_json()

		job_id = details['job_id']

		key = "textract_output/"+str(job_id)+"/1"

		s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

		result = s3_client.list_objects_v2(Bucket='dms-project-bucket', Prefix=key)

		if 'Contents' in result:
			get_key = 1
			update_query = ("""UPDATE `uploading_track_details` SET `get_key` = %s
					WHERE `job_id` = %s """)
			update_data = (get_key,job_id)
			cursor.execute(update_query,update_data)

			connection.commit()
			cursor.close()
			details['get_key'] = 1

			return ({"attributes": {
				    "status_desc": "track_details",
				    "status": "success"
				},
				"responseList":details}), status.HTTP_200_OK

		else:		
			details['get_key'] = 0
			return ({"attributes": {
				    "status_desc": "track_details",
				    "status": "success"
				},
				"responseList":details}), status.HTTP_200_OK		


#----------------------Check-key-Is-Exsits--------------------#

#----------------------Create-Text-File---------------------#

@name_space.route("/CreateTextFile")	
class CreateTextFile(Resource):
	@api.expect(create_text_postmodel)
	def post(self):
		connection = mysql_connection()
		cursor = connection.cursor()

		details = request.get_json()

		request_no  = details['request_no']
		documentName = details['documentName']		

		file_name = documentName.split('/')
		uploading_file_name = file_name[1]

		uploading_file = uploading_file_name.split('.')

		key = details['key']
		job_id = details['job_id']

		get_job_status_query = ("""SELECT *
				FROM `uploading_track_details` WHERE `job_id` = %s""")
		get_job_status_data = (job_id)
		job_status_count = cursor.execute(get_job_status_query,get_job_status_data)

		job_status = cursor.fetchone()
		

		if job_status['get_key'] == 1:
			my_config = Config(
			    region_name = 'us-east-1'
			)

			client = boto3.client('s3',config=my_config,aws_access_key_id=ACCESS_KEY,
				aws_secret_access_key=SECRET_KEY)

			response = client.get_object(
			    Bucket='dms-project-bucket',
			    Key= key,
			)

			data = response['Body'].read()
			data = json.loads(data)

			for key,filedata in enumerate(data['Blocks']):
				if filedata['BlockType'] == 'LINE':
					f = open("./dms-project/"+uploading_file[0]+".txt", "a")
					#f = open(uploading_file[0]+".txt", "a")
					content = str(filedata['Text'].encode('utf-8'))
					split_main_content = content.split('\'')
					main_content = split_main_content[1]
					f.write(main_content)
					f.write("\n")
					f.close()

			get_query = ("""SELECT *
				FROM `uploading_track_details` WHERE `request_no` = %s and `uploadig_file_name` = %s""")
			getData = (details['request_no'],uploading_file_name)
			count_track_details = cursor.execute(get_query,getData)
			print(cursor._last_executed)

			if count_track_details > 0:
				create_text_file = 1
				update_query = ("""UPDATE `uploading_track_details` SET `create_text_file` = %s
						WHERE `request_no` = %s and `uploadig_file_name` = %s""")
				update_data = (create_text_file,request_no,uploading_file_name)
				cursor.execute(update_query,update_data)

				print(cursor._last_executed)

			connection.commit()
			cursor.close()

			text_file_path = "./dms-project/"+uploading_file[0]+".txt"
			#text_file_path = uploading_file[0]+".txt"

			return ({"attributes": {"status_desc": "create_text_file",
									"status": "success"},
					"responseList":{"text_file_path":text_file_path,"request_no":request_no,"documentName":documentName}}), status.HTTP_200_OK
		else:
			return ({"attributes": {"status_desc": "create_text_file",
											"status": "success"},
							"responseList":{"text_file_path":"","request_no":request_no,"documentName":documentName}}), status.HTTP_200_OK

#----------------------Create-Text-File---------------------#


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
		print(uploading_track_details)
		uploading_track_details_id = uploading_track_details['uploading_track_details_id']
		last_update_id = uploading_track_details['last_update_id']
		

		# Looping through the file line by line
		#line = inputFile.readline()
		# print(line)
		# Flag Variables

		is_disable = "" 
		ip_number = "" 
		ip_name = "" 
		no_of_days = ""
		total_wages = ""
		ip_contribution = ""
		reason = ""
		total_ip_contribution = ""
		employer_contribution = ""
		total_contribution = ""
		total_goverment_contribution = ""
		total_monthly_wagees = ""

		global lineNumber

		for fileLine in inputFile:
		    lineNumber = lineNumber+1

		    # Calling the function for Contribution History
		    if(contributionHistoryFlag == "N"):
		        contributionHistory(fileLine,uploading_track_details_id,last_update_id)
		    elif(firstTableFlag == "N"):
		        firstTableData(fileLine,uploading_track_details_id,last_update_id)
		    elif(secondTableFlag == "N"):
        		secondTableData(fileLine,uploading_track_details_id,last_update_id)

		return ({"attributes": {"status_desc": "Read_File_From_txt",
								"status": "success"},
				"responseList":details}), status.HTTP_200_OK


def firstTableData(fileLine,uploading_track_details_id,last_update_id):
    global firstTableLineOffset
    if("Total IP Contribution" in fileLine):
        print("starting First Table data" + str(lineNumber))
        global readingFirstTable
        readingFirstTable = "Y"
    global total_ip_contribution
    global employer_contribution
    global total_contribution
    global total_goverment_contribution
    global total_monthly_wagees

    connection = mysql_connection()
    cursor = connection.cursor()

    get_query = ("""SELECT *
			FROM `esic_basic_data` WHERE `uploading_track_details_id` = %s""")
    getData = (uploading_track_details_id)
    esi_basic_data_count = cursor.execute(get_query,getData)
    esi_basic_data = cursor.fetchone()
    esic_basic_data_id = esi_basic_data['esic_basic_data_id']

    if(readingFirstTable == "Y"):
        firstTableLineOffset = firstTableLineOffset+1
        if(firstTableLineOffset == 6):        	
        	total_ip_contribution = fileLine
        elif(firstTableLineOffset == 7):
        	employer_contribution = fileLine        	
        elif(firstTableLineOffset == 8):
        	total_contribution = fileLine
        elif(firstTableLineOffset == 9):
        	total_goverment_contribution = fileLine
        elif(firstTableLineOffset == 10):
            total_monthly_wagees = fileLine
            global firstTableFlag
            firstTableFlag = "Y"

            print(total_ip_contribution)
            print(employer_contribution)

            update_query = ("""UPDATE `esic_basic_data` SET `total_ip_contribution` = %s,`total_employee_contribution` = %s, 
        						`total_contribution` = %s, `total_goverment_contribution` = %s,`total_month_wages` = %s
													WHERE `esic_basic_data_id` = %s """)
            update_data = (total_ip_contribution,employer_contribution,total_contribution,total_goverment_contribution,total_monthly_wagees,esic_basic_data_id)
            cursor.execute(update_query,update_data)

            connection.commit()
            cursor.close()

            readingFirstTable = "N"


def secondTableData(fileLine,uploading_track_details_id,last_update_id):

    #    print(" In second table")
    global secondTableLineOffset
    global readingSecondTable
    global secondTableDataIgnore
    global secondTableFlag
#    print(str(secondTableLineOffset) + readingSecondTable)
    if("SNo." in fileLine):
        print("starting second Table data" + str(lineNumber))
        readingSecondTable = "Y"
    

    connection = mysql_connection()
    cursor = connection.cursor()

    get_query = ("""SELECT *
			FROM `esic_basic_data` WHERE `uploading_track_details_id` = %s""")
    getData = (uploading_track_details_id)
    esi_basic_data_count = cursor.execute(get_query,getData)
    esi_basic_data = cursor.fetchone()
    esic_basic_data_id = esi_basic_data['esic_basic_data_id']		

    global is_disable
    global ip_number
    global ip_name
    global no_of_days
    global total_wages
    global ip_contribution
    global reason

    if("Page of 1" in fileLine):
        secondTableFlag = "Y"

    if(readingSecondTable == "Y" and secondTableFlag == "N"):
     #       print(" in the Y if")
        secondTableLineOffset = secondTableLineOffset+1
        if(secondTableLineOffset == 11):
            secondTableLineOffset = 0
            secondTableDataIgnore = "N"            
        if(secondTableLineOffset == 2 and secondTableDataIgnore == "N"):
        	is_disable = fileLine
        	#print(is_disable)
        elif(secondTableLineOffset == 3 and secondTableDataIgnore == "N"):
        	ip_number = fileLine
        	#print(ip_number)
        elif(secondTableLineOffset == 4 and secondTableDataIgnore == "N"):
        	ip_name = fileLine  
        	#print(ip_name)
        elif(secondTableLineOffset == 5 and secondTableDataIgnore == "N"):
        	no_of_days = fileLine
        	#print(no_of_days)
        elif(secondTableLineOffset == 6 and secondTableDataIgnore == "N"):
        	total_wages = fileLine 
        	#print(total_wages)
        elif(secondTableLineOffset == 7 and secondTableDataIgnore == "N"):
        	ip_contribution = fileLine 
        	#print(ip_contribution)          

        elif(secondTableLineOffset == 8 and secondTableDataIgnore == "N"):
        	reason = fileLine
        	insert_query = ("""INSERT INTO `esic_table_data`(`esic_basic_data_id`,`is_disable`,`ip_number`,`ip_name`,`no_of_days`,`total_wages`,`ip_contribution`,`reason`,`last_update_id`) 
								VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
        	data = (esic_basic_data_id,is_disable,ip_number,ip_name,no_of_days,total_wages,ip_contribution,reason,last_update_id)
        	cursor.execute(insert_query,data)
        	

        	uploading_data_into_database = 1

        	update_query = ("""UPDATE `uploading_track_details` SET `uploading_data_into_database` = %s
						WHERE `uploading_track_details_id` = %s""")
        	update_data = (uploading_data_into_database,uploading_track_details_id)
        	cursor.execute(update_query,update_data)


        	print(cursor._last_executed)

        	connection.commit()
        	cursor.close()

        	secondTableLineOffset = 0       



def contributionHistory(fileLine,uploading_track_details_id,last_update_id):
    #    print("line Number" + str(lineNumber))
    if("Contribution History Of" in fileLine):
        print("in the Contribution history for line number" + str(lineNumber))
# Changing the flag so that the code only runs once
        global contributionHistoryFlag
        contributionHistoryFlag = "Y"
        connection = mysql_connection()
        cursor = connection.cursor()

        accountNumber = fileLine[24:38]
        month = fileLine[45:55]
        print("account Number" + str(accountNumber))
        print("month" + str(month))

        month = str(month)        

        insert_query = ("""INSERT INTO `esic_basic_data`(`history_no`,`challan_date`,`uploading_track_details_id`,`last_update_id`) 
								VALUES(%s,%s,%s,%s)""")
        data = (accountNumber,month,uploading_track_details_id,last_update_id)
        cursor.execute(insert_query,data)

        print(cursor._last_executed)

        connection.commit()
        cursor.close()




#----------------------Read-From-Text-File-And-Save-Into-Database--------------------#

#----------------------Uploading-Track-List--------------------#

@name_space.route("/UploadingTrackList/<int:user_id>/<string:start_date>/<string:end_date>/<string:content_type>/<string:uploading_type>")	
class UploadingTrackList(Resource):
	def get(self,user_id,start_date,end_date,content_type,uploading_type):
		connection = mysql_connection()
		cursor = connection.cursor()

		if start_date == 'NA' and end_date == 'NA' and content_type == 'NA':

			get_uploading_track_query = ("""SELECT ut.`request_no`,ut.`uploading_file_count`,ut.`file_type`,ut.`content_type`,ut.`status`,ut.`last_update_id`,DATE_ADD(last_update_ts, INTERVAL 330 MINUTE) as `last_update_ts` from `uploading_track` ut WHERE `last_update_id` = %s and `status` = 1 and `uploading_type` = %s""")
			get_uploading_track_data = (user_id,uploading_type)
			uploadin_track_count = cursor.execute(get_uploading_track_query,get_uploading_track_data)

			if uploadin_track_count > 0:
				uploading_track_data = cursor.fetchall()
				for key,data in enumerate(uploading_track_data):				
					last_update_ts = data['last_update_ts'].strftime("%d-%m-%Y %H:%M:%S")
					uploading_track_data[key]['last_update_ts'] = last_update_ts
			else:
				uploading_track_data = []
		else:
			if content_type == 'NA':
				get_uploading_track_query = ("""SELECT ut.`request_no`,ut.`uploading_file_count`,ut.`file_type`,ut.`content_type`,ut.`status`,ut.`last_update_id`,DATE_ADD(last_update_ts, INTERVAL 330 MINUTE) as `last_update_ts` from `uploading_track` ut WHERE `last_update_id` = %s and `status` = 1 
					and  date(ut.`last_update_ts`) >= %s and date(ut.`last_update_ts`) <= %s and `uploading_type` = %s""")
				get_uploading_track_data = (user_id,start_date,end_date,uploading_type)
				uploadin_track_count = cursor.execute(get_uploading_track_query,get_uploading_track_data)

				if uploadin_track_count > 0:
					uploading_track_data = cursor.fetchall()
					for key,data in enumerate(uploading_track_data):				
						last_update_ts = data['last_update_ts'].strftime("%d-%m-%Y %H:%M:%S")
						uploading_track_data[key]['last_update_ts'] = last_update_ts
				else:
					uploading_track_data = []
			elif start_date == 'NA' and end_date == 'NA':
				get_uploading_track_query = ("""SELECT ut.`request_no`,ut.`uploading_file_count`,ut.`file_type`,ut.`content_type`,ut.`status`,ut.`last_update_id`,DATE_ADD(last_update_ts, INTERVAL 330 MINUTE) as `last_update_ts` from `uploading_track` ut WHERE `last_update_id` = %s and `status` = 1 
					and  ut.`content_type` = %s and `uploading_type` = %s""")
				get_uploading_track_data = (user_id,content_type,uploading_type)
				uploadin_track_count = cursor.execute(get_uploading_track_query,get_uploading_track_data)

				if uploadin_track_count > 0:
					uploading_track_data = cursor.fetchall()
					for key,data in enumerate(uploading_track_data):				
						last_update_ts = data['last_update_ts'].strftime("%d-%m-%Y %H:%M:%S")
						uploading_track_data[key]['last_update_ts'] = last_update_ts
				else:
					uploading_track_data = []
			else:
				get_uploading_track_query = ("""SELECT ut.`request_no`,ut.`uploading_file_count`,ut.`file_type`,ut.`content_type`,ut.`status`,ut.`last_update_id`,DATE_ADD(last_update_ts, INTERVAL 330 MINUTE) as `last_update_ts` from `uploading_track` ut WHERE `last_update_id` = %s and `status` = 1 
					and  date(ut.`last_update_ts`) >= %s and date(ut.`last_update_ts`) <= %s and `content_type` = %s and `uploading_type` = %s""")
				get_uploading_track_data = (user_id,start_date,end_date,content_type,uploading_type)
				uploadin_track_count = cursor.execute(get_uploading_track_query,get_uploading_track_data)

				if uploadin_track_count > 0:
					uploading_track_data = cursor.fetchall()
					for key,data in enumerate(uploading_track_data):				
						last_update_ts = data['last_update_ts'].strftime("%d-%m-%Y %H:%M:%S")
						uploading_track_data[key]['last_update_ts'] = last_update_ts
				else:
					uploading_track_data = []

		return ({"attributes": {
			    		"status_desc": "uploading_track",
			    		"status": "success"
			    },
			    "responseList":uploading_track_data}), status.HTTP_200_OK	

#----------------------Uploading-Track-List--------------------#

#----------------------Uploading-Track-Details-List--------------------#

@name_space.route("/UploadingTrackDetailsList/<int:request_no>")	
class UploadingTrackDetailsList(Resource):
	def get(self,request_no):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_uploading_track_query = ("""SELECT * from `uploading_track` WHERE `request_no` = %s""")
		get_uploading_track_data = (request_no)
		uploading_track_count = cursor.execute(get_uploading_track_query,get_uploading_track_data)

		if uploading_track_count > 0:
			uploadin_track = cursor.fetchone()
			content_type = uploadin_track['content_type']
		else:
			content_type = 0

		get_uploading_track_details_query = ("""SELECT * from `uploading_track_details` WHERE `request_no` = %s""")
		get_uploading_track_details_data = (request_no)
		uploadin_track_details_count = cursor.execute(get_uploading_track_details_query,get_uploading_track_details_data)

		if uploadin_track_details_count > 0:
			uploading_track_details_data = cursor.fetchall()
			for key,data in enumerate(uploading_track_details_data):
				uploading_track_details_data[key]['last_update_ts'] = str(data['last_update_ts'])
		else:
			uploading_track_details_data = []

		return ({"attributes": {
			    		"status_desc": "uploading_track_details",
			    		"status": "success",
			    		"content_type":content_type
			    },
			    "responseList":uploading_track_details_data}), status.HTTP_200_OK	

#----------------------Uploading-Track-Details-List--------------------#

#----------------------Esic-Details--------------------#

@name_space.route("/esicDetails/<int:uploading_track_details_id>")	
class esicDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_esic_basic_details_query = ("""SELECT * from `esic_basic_data` WHERE `uploading_track_details_id` = %s""")
		get_esic_basic_details_data = (uploading_track_details_id)
		esic_basic_details_count = cursor.execute(get_esic_basic_details_query,get_esic_basic_details_data)

		if esic_basic_details_count > 0:
			esic_basic_details = cursor.fetchone()
			esic_basic_details['last_update_ts'] = str(esic_basic_details['last_update_ts'])
			get_esic_table_details_quey = ("""SELECT * from `esic_table_data` WHERE `esic_basic_data_id` = %s""")
			get_esic_table_details_data = (esic_basic_details['esic_basic_data_id'])
			get_esic_table_details_count = cursor.execute(get_esic_table_details_quey,get_esic_table_details_data)

			if get_esic_table_details_count > 0:
				esic_table_data = cursor.fetchall()
				for key,data in enumerate(esic_table_data):
					esic_table_data[key]['last_update_ts'] = str(esic_table_data[key]['last_update_ts'])
				esic_basic_details['esic_table_data'] = esic_table_data
			else:
				esic_basic_details['esic_table_data'] = []
		else:
			esic_basic_details = {}

		return ({"attributes": {
			    		"status_desc": "uploading_track_details",
			    		"status": "success"
			    },
			    "responseList":esic_basic_details}), status.HTTP_200_OK


#----------------------Esic-Details--------------------#

#----------------------Esic-Payment-Details--------------------#

@name_space.route("/esicPaymnetDetails/<int:uploading_track_details_id>")	
class esicPaymnetDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_esic_payment_details_query = ("""SELECT * from `esic_payment` WHERE `uploading_track_details_id` = %s""")
		get_esic_payment_details_data = (uploading_track_details_id)
		get_esic_payment_details_count = cursor.execute(get_esic_payment_details_query,get_esic_payment_details_data)

		if get_esic_payment_details_count > 0:
			esic_payment_details_data = cursor.fetchone()
			esic_payment_details_data['last_update_ts'] = str(esic_payment_details_data['last_update_ts'])
		else:
			esic_payment_details_data = {}

		return ({"attributes": {
			    		"status_desc": "esic_payment_details",
			    		"status": "success"
			    },
			    "responseList":esic_payment_details_data}), status.HTTP_200_OK
			    	
#----------------------Esic-Payment-Details--------------------#

#----------------------Esic-Table-Details--------------------#

@name_space.route("/esicTableDetails/<int:esic_table_data_id>")	
class esicTableDetails(Resource):
	def get(self,esic_table_data_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_esic_table_query = ("""SELECT * from `esic_table_data` WHERE `esic_table_data_id` = %s""")
		get_esic_table_data = (esic_table_data_id)
		get_esic_table_details_count = cursor.execute(get_esic_table_query,get_esic_table_data)

		if get_esic_table_details_count > 0:
			esic_table_details_data = cursor.fetchone()
			esic_table_details_data['last_update_ts'] = str(esic_table_details_data['last_update_ts'])
		else:
			esic_table_details_data = {}

		return ({"attributes": {
			    		"status_desc": "esic_table_details",
			    		"status": "success"
			    },
			    "responseList":esic_table_details_data}), status.HTTP_200_OK

#----------------------Esic-Table-Details--------------------#

#----------------------Ptax-Challan-Details--------------------#

@name_space.route("/ptaxChallanDetails/<int:uploading_track_details_id>")	
class ptaxChallanDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_p_tax_challan_details_query = ("""SELECT * from `p_tax_challan_data` WHERE `uploading_track_details_id` = %s""")
		get_p_tax_challan_details_data = (uploading_track_details_id)
		get_p_tax_challan_details_count = cursor.execute(get_p_tax_challan_details_query,get_p_tax_challan_details_data)

		if get_p_tax_challan_details_count > 0:
			p_tax_details_data = cursor.fetchone()
			p_tax_details_data['last_update_ts'] = str(p_tax_details_data['last_update_ts'])
		else:
			p_tax_details_data = {}

		return ({"attributes": {
			    		"status_desc": "ptax_esic_details",
			    		"status": "success"
			    },
			    "responseList":p_tax_details_data}), status.HTTP_200_OK
			    	
#----------------------Ptax-Challan-Details--------------------#

#----------------------Ptax-Payment-Details--------------------#

@name_space.route("/ptaxPaymentDetails/<int:uploading_track_details_id>")	
class ptaxPaymentDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_p_tax_payment_details_query = ("""SELECT * from `p_tax_payment_data` WHERE `uploading_track_details_id` = %s""")
		get_p_tax_payment_details_data = (uploading_track_details_id)
		get_p_tax_payment_details_count = cursor.execute(get_p_tax_payment_details_query,get_p_tax_payment_details_data)

		if get_p_tax_payment_details_count > 0:
			p_tax_payment_details_data = cursor.fetchone()
			p_tax_payment_details_data['last_update_ts'] = str(p_tax_payment_details_data['last_update_ts'])
		else:
			p_tax_payment_details_data = {}

		return ({"attributes": {
			    		"status_desc": "ptax_esic_details",
			    		"status": "success"
			    },
			    "responseList":p_tax_payment_details_data}), status.HTTP_200_OK
			    	
#----------------------Ptax-Payment-Details--------------------#

#----------------------PF-Challan-Details--------------------#

@name_space.route("/pfChallanDetails/<int:uploading_track_details_id>")	
class pfChallanDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_pf_challan_details_query = ("""SELECT * from `pf_challan_data` WHERE `uploading_track_details_id` = %s""")
		get_pf_challan_details_data = (uploading_track_details_id)
		get_pf_challan_details_count = cursor.execute(get_pf_challan_details_query,get_pf_challan_details_data)

		if get_pf_challan_details_count > 0:
			pf_challan_details_data = cursor.fetchone()
			pf_challan_details_data['last_update_ts'] = str(pf_challan_details_data['last_update_ts'])
		else:
			pf_challan_details_data = {}

		return ({"attributes": {
			    		"status_desc": "pf_challan_details",
			    		"status": "success"
			    },
			    "responseList":pf_challan_details_data}), status.HTTP_200_OK

#----------------------PF-Challan-Details--------------------#

#----------------------PF-Payment-Details--------------------#

@name_space.route("/pfPaymentDetails/<int:uploading_track_details_id>")	
class pfPaymentDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_pf_payment_details_query = ("""SELECT * from `pf_payment_data` WHERE `uploading_track_details_id` = %s""")
		get_pf_payment_details_data = (uploading_track_details_id)
		get_pf_payment_details_count = cursor.execute(get_pf_payment_details_query,get_pf_payment_details_data)

		if get_pf_payment_details_count > 0:
			pf_payment_details_data = cursor.fetchone()
			pf_payment_details_data['last_update_ts'] = str(pf_payment_details_data['last_update_ts'])
		else:
			pf_payment_details_data = {}

		return ({"attributes": {
			    		"status_desc": "pf_payment_details",
			    		"status": "success"
			    },
			    "responseList":pf_payment_details_data}), status.HTTP_200_OK

#----------------------PF-Payment-Details--------------------#

#----------------------TDS-Challan-Details--------------------#

@name_space.route("/tdsChallanDetails/<int:uploading_track_details_id>")	
class tdsChallanDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_tds_challan_details_query = ("""SELECT * from `tds_challan_data` WHERE `uploading_track_details_id` = %s""")
		get_tds_challan_details_data = (uploading_track_details_id)
		get_tds_challan_details_count = cursor.execute(get_tds_challan_details_query,get_tds_challan_details_data)

		if get_tds_challan_details_count > 0:
			tds_challan_details_data = cursor.fetchone()
			tds_challan_details_data['last_update_ts'] = str(tds_challan_details_data['last_update_ts'])
		else:
			tds_challan_details_data = {}

		return ({"attributes": {
			    		"status_desc": "tds_challan_details",
			    		"status": "success"
			    },
			    "responseList":tds_challan_details_data}), status.HTTP_200_OK

#----------------------TDS-Challan-Details--------------------#

#----------------------TDS-Payment-Details--------------------#

@name_space.route("/tdsPaymentDetails/<int:uploading_track_details_id>")	
class tdsPaymentDetails(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_tds_payment_details_query = ("""SELECT * from `tds_payment_data` WHERE `uploading_track_details_id` = %s""")
		get_tds_payment_details_data = (uploading_track_details_id)
		get_tds_payment_details_count = cursor.execute(get_tds_payment_details_query,get_tds_payment_details_data)

		if get_tds_payment_details_count > 0:
			tds_payment_details_data = cursor.fetchall()
			for key,data in enumerate(tds_payment_details_data):
				tds_payment_details_data[key]['last_update_ts'] = str(data['last_update_ts'])
		else:
			tds_payment_details_data = []

		get_tds_payment_deduction_details_query = ("""SELECT * from `tds_payment_deduction_details_data` WHERE `uploading_track_details_id` = %s""")
		get_tds_payment_deduction_details_data = (uploading_track_details_id)
		get_tds_payment_deduction_details_count = cursor.execute(get_tds_payment_deduction_details_query,get_tds_payment_deduction_details_data)

		if get_tds_payment_deduction_details_count > 0:
			tds_payment_deduction_details_data = cursor.fetchall()
			for key,data in enumerate(tds_payment_deduction_details_data):
				tds_payment_deduction_details_data[key]['last_update_ts'] = str(data['last_update_ts'])
		else:
			tds_payment_deduction_details_data = []

		
		return ({"attributes": {
			    		"status_desc": "pf_payment_details",
			    		"status": "success"
			    },
			    "responseList":{"tds_payment_details_data":tds_payment_details_data,"tds_payment_deduction_details_data":tds_payment_deduction_details_data}}), status.HTTP_200_OK

#----------------------TDS-Payment-Details--------------------#

#----------------------TDS-Payment-Details--------------------#

@name_space.route("/tdsPaymentDetailsBytdsPaymentdataid/<int:tds_payment_data_id>")	
class tdsPaymentDetailsBytdsPaymentdataid(Resource):
	def get(self,tds_payment_data_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_tds_payment_details_query = ("""SELECT * from `tds_payment_data` WHERE `tds_payment_data_id` = %s""")
		get_tds_payment_details_data = (tds_payment_data_id)
		get_tds_payment_details_count = cursor.execute(get_tds_payment_details_query,get_tds_payment_details_data)

		if get_tds_payment_details_count > 0:
			tds_payment_details_data = cursor.fetchone()
			tds_payment_details_data['last_update_ts'] = str(tds_payment_details_data['last_update_ts'] )
		else:
			tds_payment_details_data = {}

		return ({"attributes": {
			    		"status_desc": "tds_payment_details",
			    		"status": "success"
			    },
			    "responseList":tds_payment_details_data}), status.HTTP_200_OK

#----------------------Uploading-Track--------------------#

@name_space.route("/uploadingTrackByUploadingTrackDetailsId/<int:uploading_track_details_id>")	
class uploadingTrackByUploadingTrackDetailsId(Resource):
	def get(self,uploading_track_details_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		get_uploading_track_details_query = ("""SELECT * from `uploading_track_details` WHERE `uploading_track_details_id` = %s""")
		get_uploading_track_details_data = (uploading_track_details_id)
		get_uploading_track_details_count = cursor.execute(get_uploading_track_details_query,get_uploading_track_details_data)

		if get_uploading_track_details_count > 0:
			uploading_track_details_data = cursor.fetchone()
			uploading_track_data = {}
			uploading_track_data['uploadig_file_name'] = uploading_track_details_data['uploadig_file_name']

			get_uploading_track_query = ("""SELECT * from `uploading_track` WHERE `request_no` = %s""")
			get_uploading_track_data = (uploading_track_details_data['request_no'])
			get_uploading_track_data_count = cursor.execute(get_uploading_track_query,get_uploading_track_data)

			if get_uploading_track_data_count > 0:
				uploading_track = cursor.fetchone()
				uploading_track_data['request_no'] = uploading_track['request_no']
				uploading_track_data['uploading_file_count'] = uploading_track['uploading_file_count']
				uploading_track_data['file_type'] = uploading_track['file_type']
				uploading_track_data['content_type'] = uploading_track['content_type']
				uploading_track_data['status'] = uploading_track['status']
				uploading_track_data['last_update_ts'] = str(uploading_track['last_update_ts'])
			else:
				uploading_track_data = {}

		else:
			uploading_track_data = {}

		return ({"attributes": {
			    		"status_desc": "uploading_track_details",
			    		"status": "success"
			    },
			    "responseList":uploading_track_data}), status.HTTP_200_OK

#----------------------Uploading-Track--------------------#

#----------------------Update-Esic-Table-Data---------------------#

@name_space.route("/updateEsicTableData/<int:esic_table_data_id>")
class updateEsicTableData(Resource):
	@api.expect(esic_table_putmodel)
	def put(self, esic_table_data_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		if details and "is_disable" in details:
			is_disable = details['is_disable']
			update_query = ("""UPDATE `esic_table_data` SET `is_disable` = %s
				WHERE `esic_table_data_id` = %s """)
			update_data = (is_disable,esic_table_data_id)
			cursor.execute(update_query,update_data)

		if details and "ip_number" in details:
			ip_number = details['ip_number']
			update_query = ("""UPDATE `esic_table_data` SET `ip_number` = %s
				WHERE `esic_table_data_id` = %s """)
			update_data = (ip_number,esic_table_data_id)
			cursor.execute(update_query,update_data)

		if details and "ip_number" in details:
			ip_name = details['ip_name']
			update_query = ("""UPDATE `esic_table_data` SET `ip_name` = %s
				WHERE `esic_table_data_id` = %s """)
			update_data = (ip_name,esic_table_data_id)
			cursor.execute(update_query,update_data)

		if details and "no_of_days" in details:
			no_of_days = details['no_of_days']
			update_query = ("""UPDATE `esic_table_data` SET `no_of_days` = %s
				WHERE `esic_table_data_id` = %s """)
			update_data = (no_of_days,esic_table_data_id)
			cursor.execute(update_query,update_data)

		if details and "total_wages" in details:
			total_wages = details['total_wages']
			update_query = ("""UPDATE `esic_table_data` SET `total_wages` = %s
				WHERE `esic_table_data_id` = %s """)
			update_data = (total_wages,esic_table_data_id)
			cursor.execute(update_query,update_data)

		if details and "ip_contribution" in details:
			ip_contribution = details['ip_contribution']
			update_query = ("""UPDATE `esic_table_data` SET `ip_contribution` = %s
				WHERE `esic_table_data_id` = %s """)
			update_data = (ip_contribution,esic_table_data_id)
			cursor.execute(update_query,update_data)

		if details and "reason" in details:
			reason = details['reason']
			update_query = ("""UPDATE `esic_table_data` SET `reason` = %s
				WHERE `esic_table_data_id` = %s """)
			update_data = (reason,esic_table_data_id)
			cursor.execute(update_query,update_data)

		get_esic_table_query = ("""SELECT * from `esic_table_data` WHERE `esic_table_data_id` = %s""")
		get_esic_table_data = (esic_table_data_id)
		get_esic_table_details_count = cursor.execute(get_esic_table_query,get_esic_table_data)

		if get_esic_table_details_count > 0:
			esic_table_details_data = cursor.fetchone()
			esic_table_details_data['last_update_ts'] = str(esic_table_details_data['last_update_ts'])
		else:
			esic_table_details_data = {}

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update Esic Table Data",
								"status": "success"},
				"responseList": esic_table_details_data}), status.HTTP_200_OK

#----------------------Update-Esic-Table-Data---------------------#


#----------------------Update-Esic-Basic-Data---------------------#

@name_space.route("/updateEsicBasicData/<int:esic_basic_data_id>")
class updateEsicBasicData(Resource):
	@api.expect(esic_basic_putmodel)
	def put(self, esic_basic_data_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		if details and "history_no" in details:
			history_no = details['history_no']
			update_query = ("""UPDATE `esic_basic_data` SET `history_no` = %s
				WHERE `esic_basic_data_id` = %s """)
			update_data = (history_no,esic_basic_data_id)
			cursor.execute(update_query,update_data)

		if details and "challan_date" in details:
			challan_date = details['challan_date']
			update_query = ("""UPDATE `esic_basic_data` SET `challan_date` = %s
				WHERE `esic_basic_data_id` = %s """)
			update_data = (challan_date,esic_basic_data_id)
			cursor.execute(update_query,update_data)

		if details and "total_ip_contribution" in details:
			total_ip_contribution = details['total_ip_contribution']
			update_query = ("""UPDATE `esic_basic_data` SET `total_ip_contribution` = %s
				WHERE `esic_basic_data_id` = %s """)
			update_data = (total_ip_contribution,esic_basic_data_id)
			cursor.execute(update_query,update_data)

		if details and "total_employee_contribution" in details:
			total_employee_contribution = details['total_employee_contribution']
			update_query = ("""UPDATE `esic_basic_data` SET `total_employee_contribution` = %s
				WHERE `esic_basic_data_id` = %s """)
			update_data = (total_employee_contribution,esic_basic_data_id)
			cursor.execute(update_query,update_data)

		if details and "total_contribution" in details:
			total_contribution = details['total_contribution']
			update_query = ("""UPDATE `esic_basic_data` SET `total_contribution` = %s
				WHERE `esic_basic_data_id` = %s """)
			update_data = (total_contribution,esic_basic_data_id)
			cursor.execute(update_query,update_data)

		if details and "total_goverment_contribution" in details:
			total_goverment_contribution = details['total_goverment_contribution']
			update_query = ("""UPDATE `esic_basic_data` SET `total_goverment_contribution` = %s
				WHERE `esic_basic_data_id` = %s """)
			update_data = (total_goverment_contribution,esic_basic_data_id)
			cursor.execute(update_query,update_data)

		if details and "total_month_wages" in details:
			total_month_wages = details['total_month_wages']
			update_query = ("""UPDATE `esic_basic_data` SET `total_month_wages` = %s
				WHERE `esic_basic_data_id` = %s """)
			update_data = (total_month_wages,esic_basic_data_id)
			cursor.execute(update_query,update_data)

		get_esic_basic_query = ("""SELECT * from `esic_basic_data` WHERE `esic_basic_data_id` = %s""")
		get_esic_basic_data = (esic_basic_data_id)
		get_esic_basic_details_count = cursor.execute(get_esic_basic_query,get_esic_basic_data)

		if get_esic_basic_details_count > 0:
			esic_basic_details_data = cursor.fetchone()
			esic_basic_details_data['last_update_ts'] = str(esic_basic_details_data['last_update_ts'])
		else:
			esic_basic_details_data = {}

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update Esic Basic Data Successfully",
								"status": "success"},
				"responseList": esic_basic_details_data}), status.HTTP_200_OK

#----------------------Update-Esic-Basic-Data---------------------#

#----------------------Update-Esic-Basic-Data---------------------#

@name_space.route("/updateEsicPaymentData/<int:esic_payment_id>")
class updateEsicPaymentData(Resource):
	@api.expect(esic_payment_putmodel)
	def put(self, esic_payment_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		if details and "transaction_status" in details:
			transaction_status = details['transaction_status']
			update_query = ("""UPDATE `esic_payment` SET `transaction_status` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (transaction_status,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "employers_code_no" in details:
			employers_code_no = details['employers_code_no']
			update_query = ("""UPDATE `esic_payment` SET `employers_code_no` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (employers_code_no,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "employers_name" in details:
			employers_name = details['employers_name']
			update_query = ("""UPDATE `esic_payment` SET `employers_name` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (employers_name,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_period" in details:
			challan_period = details['challan_period']
			update_query = ("""UPDATE `esic_payment` SET `challan_period` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (challan_period,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_number" in details:
			challan_number = details['challan_number']
			update_query = ("""UPDATE `esic_payment` SET `challan_number` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (challan_number,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_created_date" in details:
			challan_created_date = details['challan_created_date']
			update_query = ("""UPDATE `esic_payment` SET `challan_created_date` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (challan_created_date,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_submited_date" in details:
			challan_submited_date = details['challan_submited_date']
			update_query = ("""UPDATE `esic_payment` SET `challan_submited_date` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (challan_submited_date,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "amount_paid" in details:
			amount_paid = details['amount_paid']
			update_query = ("""UPDATE `esic_payment` SET `amount_paid` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (amount_paid,esic_payment_id)
			cursor.execute(update_query,update_data)

		if details and "transaction_number" in details:
			transaction_number = details['transaction_number']
			update_query = ("""UPDATE `esic_payment` SET `transaction_number` = %s
				WHERE `esic_payment_id` = %s """)
			update_data = (transaction_number,esic_payment_id)
			cursor.execute(update_query,update_data)


		get_esic_payment_query = ("""SELECT * from `esic_payment` WHERE `esic_payment_id` = %s""")
		get_esic_payment_data = (esic_payment_id)
		get_esic_payment_details_count = cursor.execute(get_esic_payment_query,get_esic_payment_data)

		if get_esic_payment_details_count > 0:
			esic_paymengt_details_data = cursor.fetchone()
			esic_paymengt_details_data['last_update_ts'] = str(esic_paymengt_details_data['last_update_ts'])
		else:
			esic_paymengt_details_data = {}

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update Esic Payment Data Successfully",
								"status": "success"},
				"responseList": esic_paymengt_details_data}), status.HTTP_200_OK

#----------------------Add-Esic-Table-Data---------------------#

@name_space.route("/AddEsicTableData")
class AddEsicTableData(Resource):
	@api.expect(esic_table_postmodel)
	def post(self):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		esic_basic_data_id = details['esic_basic_data_id']
		is_disable = details['is_disable']
		ip_number = details['ip_number']
		ip_name = details['ip_name']
		no_of_days = details['no_of_days']
		total_wages = details['total_wages']
		ip_contribution = details['ip_contribution']
		reason = details['reason']
		user_id = details['user_id']

		insert_query = ("""INSERT INTO `esic_table_data`(`esic_basic_data_id`,`is_disable`,`ip_number`,`ip_name`,`no_of_days`,`total_wages`,`ip_contribution`,`reason`,`last_update_id`) 
				VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""")

		data = (esic_basic_data_id,is_disable,ip_number,ip_name,no_of_days,total_wages,ip_contribution,reason,user_id)
		cursor.execute(insert_query,data)

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Add Esic Table Data Successfully",
								"status": "success"},
				"responseList": details}), status.HTTP_200_OK

#----------------------Add-Esic-Table-Data---------------------#

#----------------------Delete-Esic-Table-Data--------------------#

@name_space.route("/deleteEsicTableData/<int:esic_table_data_id>/<int:esic_basic_data_id>")
class deleteEsicTableData(Resource):
	def delete(self, esic_table_data_id,esic_basic_data_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		delete_query = ("""DELETE FROM `esic_table_data` WHERE `esic_table_data_id` = %s""")
		delData = (esic_table_data_id)
		
		cursor.execute(delete_query,delData)		

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Delete Esic Table",
								"status": "success"},
				"responseList": {"esic_basic_data_id":esic_basic_data_id}}), status.HTTP_200_OK

#----------------------Delete-Esic-Table-Data--------------------#

#----------------------Delete-Uploading-Track-------------------#

@name_space.route("/deleteUploadingTrack/<int:request_no>")
class deleteUploadingTrack(Resource):
	def delete(self, request_no):
		connection = mysql_connection()
		cursor = connection.cursor()

		uploading_track_status = 0

		update_query = ("""UPDATE `uploading_track` SET `status` = %s WHERE `request_no` = %s""")
		update_data = (uploading_track_status,request_no)
		cursor.execute(update_query,update_data)

		connection.commit()
		cursor.close()

		return ({"attributes": {
				    "status_desc": "uploading_track_details",
				    "status": "success"
				},
				"responseList":"Deleted Successfuly"}), status.HTTP_200_OK

#----------------------Delete-Uploading-Track-------------------#

#----------------------Dms-Dashboard--------------------#

@name_space.route("/dmsDashboard/<int:user_id>")	
class dmsDashboard(Resource):
	def get(self,user_id):
		connection = mysql_connection()
		cursor = connection.cursor()

		dashboard_data = {}

		get_esic_challan_count_query = ("""SELECT count(*) as total_challan_count from `uploading_track` WHERE `content_type` = 'challan' and `uploading_type` = 'esic' and status = 1 and `last_update_id` = %s""")
		get_esic_challan_count_data = (user_id)
		esic_challan_count = cursor.execute(get_esic_challan_count_query,get_esic_challan_count_data)

		if esic_challan_count > 0:
			esic_challan = cursor.fetchone()
			dashboard_data['esic_challan_couunt'] = esic_challan['total_challan_count']
		else:
			dashboard_data['esic_challan_couunt'] = 0

		get_esic_payment_count_query = ("""SELECT count(*) as total_payment_count from `uploading_track` WHERE `content_type` = 'payment' and `uploading_type` = 'esic' and status = 1 and `last_update_id` = %s""")
		get_esic_payment_count_data = (user_id)
		esic_payment_count = cursor.execute(get_esic_payment_count_query,get_esic_payment_count_data)

		if esic_payment_count > 0:
			esic_payment = cursor.fetchone()
			dashboard_data['total_payment_count'] = esic_payment['total_payment_count']
		else:
			dashboard_data['total_payment_count'] = 0

		get_p_tax_challan_count_query = ("""SELECT count(*) as total_p_tax_challan_count from `uploading_track` WHERE `content_type` = 'challan' and `uploading_type` = 'p-tax' and status = 1 and `last_update_id` = %s""")
		get_p_tax_challan_count_data = (user_id)
		p_tax_challan_count = cursor.execute(get_p_tax_challan_count_query,get_p_tax_challan_count_data)

		if p_tax_challan_count > 0:
			p_tax_challan = cursor.fetchone()
			dashboard_data['p_tax_challan_count'] = p_tax_challan['total_p_tax_challan_count']
		else:
			dashboard_data['p_tax_challan_count'] = 0

		get_p_tax_payment_count_query = ("""SELECT count(*) as total_p_tax_payment_count from `uploading_track` WHERE `content_type` = 'payment' and `uploading_type` = 'p-tax' and status = 1 and `last_update_id` = %s""")
		get_p_tax_payment_count_data = (user_id)
		p_tax_payment_count = cursor.execute(get_p_tax_payment_count_query,get_p_tax_payment_count_data)

		if p_tax_payment_count > 0:
			p_tax_payment = cursor.fetchone()
			dashboard_data['p_tax_payment_count'] = p_tax_payment['total_p_tax_payment_count']
		else:
			dashboard_data['p_tax_payment_count'] = 0


		get_pf_challan_count_query = ("""SELECT count(*) as total_pf_challan_count from `uploading_track` WHERE `content_type` = 'challan' and `uploading_type` = 'pf' and status = 1 and `last_update_id` = %s""")
		get_pf_challan_count_data = (user_id)
		pf_challan_count = cursor.execute(get_pf_challan_count_query,get_pf_challan_count_data)

		if pf_challan_count > 0:
			pf_challan = cursor.fetchone()
			dashboard_data['pf_challan_count'] = pf_challan['total_pf_challan_count']
		else:
			dashboard_data['pf_challan_count'] = 0


		get_pf_payment_count_query = ("""SELECT count(*) as total_pf_payment_count from `uploading_track` WHERE `content_type` = 'payment' and `uploading_type` = 'pf' and status = 1 and `last_update_id` = %s""")
		get_pf_payment_count_data = (user_id)
		pf_payment_count = cursor.execute(get_pf_payment_count_query,get_pf_payment_count_data)

		if p_tax_payment_count > 0:
			pf_payment = cursor.fetchone()
			dashboard_data['pf_payment_count'] = pf_payment['total_pf_payment_count']
		else:
			dashboard_data['pf_payment_count'] = 0

		return ({"attributes": {"status_desc": "Dashboard Data",
								"status": "success"},
				"responseList": dashboard_data}), status.HTTP_200_OK



#----------------------Dms-Dashboard--------------------#

#----------------------Update-P-Tax-Challan-Data---------------------#

@name_space.route("/updatePtaxChallanData/<int:p_tax_challan_id>")
class updatePtaxChallanData(Resource):
	@api.expect(ptax_challan_putmodel)
	def put(self, p_tax_challan_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		if details and "grn" in details:
			grn = details['grn']
			update_query = ("""UPDATE `p_tax_challan_data` SET `grn` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (grn,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "payment_mode" in details:
			payment_mode = details['payment_mode']
			update_query = ("""UPDATE `p_tax_challan_data` SET `payment_mode` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (payment_mode,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "grn_date" in details:
			grn_date = details['grn_date']
			update_query = ("""UPDATE `p_tax_challan_data` SET `grn_date` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (grn_date,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "bank_gateway" in details:
			bank_gateway = details['bank_gateway']
			update_query = ("""UPDATE `p_tax_challan_data` SET `bank_gateway` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (bank_gateway,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "brn" in details:
			brn = details['brn']
			update_query = ("""UPDATE `p_tax_challan_data` SET `brn` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (brn,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "brn_date" in details:
			brn_date = details['brn_date']
			update_query = ("""UPDATE `p_tax_challan_data` SET `brn_date` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (brn_date,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "payment_status" in details:
			payment_status = details['payment_status']
			update_query = ("""UPDATE `p_tax_challan_data` SET `payment_status` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (payment_status,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "payment_ref_no" in details:
			payment_ref_no = details['payment_ref_no']
			update_query = ("""UPDATE `p_tax_challan_data` SET `payment_ref_no` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (payment_ref_no,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "depositors_name" in details:
			depositors_name = details['depositors_name']
			update_query = ("""UPDATE `p_tax_challan_data` SET `depositors_name` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (depositors_name,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "address" in details:
			address = details['address']
			update_query = ("""UPDATE `p_tax_challan_data` SET `address` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (address,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "mobile" in details:
			mobile = details['mobile']
			update_query = ("""UPDATE `p_tax_challan_data` SET `mobile` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (mobile,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "email" in details:
			email = details['email']
			update_query = ("""UPDATE `p_tax_challan_data` SET `email` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (email,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "depositor_status" in details:
			depositor_status = details['depositor_status']
			update_query = ("""UPDATE `p_tax_challan_data` SET `depositor_status` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (depositor_status,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "period_from" in details:
			period_from = details['period_from']
			update_query = ("""UPDATE `p_tax_challan_data` SET `period_from` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (period_from,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "period_to" in details:
			period_to = details['period_to']
			update_query = ("""UPDATE `p_tax_challan_data` SET `period_to` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (period_to,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "payment_id" in details:
			payment_id = details['payment_id']
			update_query = ("""UPDATE `p_tax_challan_data` SET `payment_id` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (payment_id,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "payment_ref_id" in details:
			payment_ref_id = details['payment_ref_id']
			update_query = ("""UPDATE `p_tax_challan_data` SET `payment_ref_id` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (payment_ref_id,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "sl.No" in details:
			slNo = details['slNo']
			update_query = ("""UPDATE `p_tax_challan_data` SET `sl.No` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (slNo,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "paymnet_id" in details:
			paymnet_id = details['paymnet_id']
			update_query = ("""UPDATE `p_tax_challan_data` SET `paymnet_id` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (paymnet_id,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "head_of_a/c_description" in details:
			head_of_a_c_description = details['head_of_a/c_description']
			update_query = ("""UPDATE `p_tax_challan_data` SET `head_of_a/c_description` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (head_of_a_c_description,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "head_of_ac" in details:
			head_of_ac = details['head_of_ac']
			update_query = ("""UPDATE `p_tax_challan_data` SET `head_of_ac` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (head_of_ac,p_tax_challan_id)
			cursor.execute(update_query,update_data)

		if details and "amount" in details:
			amount = details['amount']
			update_query = ("""UPDATE `p_tax_challan_data` SET `amount` = %s
				WHERE `p_tax_challan_id` = %s """)
			update_data = (amount,p_tax_challan_id)
			cursor.execute(update_query,update_data)
		
		

		get_p_tax_challan_query = ("""SELECT * from `p_tax_challan_data` WHERE `p_tax_challan_id` = %s""")
		get_p_tax_challan_data = (p_tax_challan_id)
		get_p_tax_challan_details_count = cursor.execute(get_p_tax_challan_query,get_p_tax_challan_data)

		if get_p_tax_challan_details_count > 0:
			p_tax_challan_details_data = cursor.fetchone()
			p_tax_challan_details_data['last_update_ts'] = str(p_tax_challan_details_data['last_update_ts'])
		else:
			p_tax_challan_details_data = {}

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update P tax Challan Data Successfully",
								"status": "success"},
				"responseList": p_tax_challan_details_data}), status.HTTP_200_OK

#----------------------Update-P-Tax-Challan-Data---------------------#

#----------------------Update-P-Tax-Payment-Data---------------------#

@name_space.route("/updatePtaxPaymentData/<int:p_tax_payment_id>")
class updatePtaxPaymentData(Resource):
	@api.expect(ptax_payment_putmodel)
	def put(self, p_tax_payment_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		if details and "name_of_the_depositor" in details:
			name_of_the_depositor = details['name_of_the_depositor']
			update_query = ("""UPDATE `p_tax_payment_data` SET `name_of_the_depositor` = %s
				WHERE `p_tax_pyment_data_id` = %s """)
			update_data = (name_of_the_depositor,p_tax_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_amount" in details:
			challan_amount = details['challan_amount']
			update_query = ("""UPDATE `p_tax_payment_data` SET `challan_amount` = %s
				WHERE `p_tax_pyment_data_id` = %s """)
			update_data = (challan_amount,p_tax_payment_id)
			cursor.execute(update_query,update_data)

		if details and "goverment_ref_no" in details:
			goverment_ref_no = details['goverment_ref_no']
			update_query = ("""UPDATE `p_tax_payment_data` SET `goverment_ref_no` = %s
				WHERE `p_tax_pyment_data_id` = %s """)
			update_data = (goverment_ref_no,p_tax_payment_id)
			cursor.execute(update_query,update_data)

		if details and "bank_ref_no" in details:
			bank_ref_no = details['bank_ref_no']
			update_query = ("""UPDATE `p_tax_payment_data` SET `bank_ref_no` = %s
				WHERE `p_tax_pyment_data_id` = %s """)
			update_data = (bank_ref_no,p_tax_payment_id)
			cursor.execute(update_query,update_data)

		if details and "transaction_date_time" in details:
			transaction_date_time = details['transaction_date_time']
			update_query = ("""UPDATE `p_tax_payment_data` SET `transaction_date_time` = %s
				WHERE `p_tax_pyment_data_id` = %s """)
			update_data = (transaction_date_time,p_tax_payment_id)
			cursor.execute(update_query,update_data)

		get_p_tax_payment_query = ("""SELECT * from `p_tax_payment_data` WHERE `p_tax_pyment_data_id` = %s""")
		get_p_tax_payment_data = (p_tax_payment_id)
		get_p_tax_payment_details_count = cursor.execute(get_p_tax_payment_query,get_p_tax_payment_data)

		if get_p_tax_payment_details_count > 0:
			p_tax_payment_details_data = cursor.fetchone()
			p_tax_payment_details_data['last_update_ts'] = str(p_tax_payment_details_data['last_update_ts'])
		else:
			p_tax_payment_details_data = {}

		print(p_tax_payment_details_data)

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update P tax Payment Data Successfully",
								"status": "success"},
				"responseList": p_tax_payment_details_data}), status.HTTP_200_OK

#----------------------Update-P-Tax-Payment-Data---------------------#

#----------------------Update-PF-Challan-Data---------------------#

@name_space.route("/updatePfChallanData/<int:pf_challan_id>")
class updatePfChallanData(Resource):
	@api.expect(pf_challan_putmodel)
	def put(self, pf_challan_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		print(details)

		if details and "trn" in details:
			trn = details['trn']
			update_query = ("""UPDATE `pf_challan_data` SET `trn` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (trn,pf_challan_id)
			cursor.execute(update_query,update_data)	

		if details and "establishment_code" in details:
			establishment_code = details['establishment_code']
			update_query = ("""UPDATE `pf_challan_data` SET `establishment_code` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (establishment_code,pf_challan_id)
			cursor.execute(update_query,update_data)	

		if details and "establishment_name" in details:
			establishment_name = details['establishment_name']
			update_query = ("""UPDATE `pf_challan_data` SET `establishment_name` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (establishment_name,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "address" in details:
			address = details['address']
			update_query = ("""UPDATE `pf_challan_data` SET `address` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (address,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_subscribers_epf" in details:
			total_subscribers_epf = details['total_subscribers_epf']
			update_query = ("""UPDATE `pf_challan_data` SET `total_subscribers_epf` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_subscribers_epf,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_subscribers_eps" in details:
			total_subscribers_eps = details['total_subscribers_eps']
			update_query = ("""UPDATE `pf_challan_data` SET `total_subscribers_eps` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_subscribers_eps,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_subscribers_edli" in details:
			total_subscribers_edli = details['total_subscribers_edli']
			update_query = ("""UPDATE `pf_challan_data` SET `total_subscribers_edli` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_subscribers_edli,pf_challan_id)
			cursor.execute(update_query,update_data)


		if details and "total_wages_epf" in details:
			total_wages_epf = details['total_wages_epf']
			update_query = ("""UPDATE `pf_challan_data` SET `total_wages_epf` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_wages_epf,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_wages_eps" in details:
			total_wages_eps = details['total_wages_eps']
			update_query = ("""UPDATE `pf_challan_data` SET `total_wages_eps` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_wages_eps,pf_challan_id)
			cursor.execute(update_query,update_data)


		if details and "total_wages_edli" in details:
			total_wages_edli = details['total_wages_edli']
			update_query = ("""UPDATE `pf_challan_data` SET `total_wages_edli` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_wages_edli,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "administration_charges_ac_01" in details:
			administration_charges_ac_01 = details['administration_charges_ac_01']
			update_query = ("""UPDATE `pf_challan_data` SET `administration_charges_ac_01` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (administration_charges_ac_01,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "administration_charges_ac_02" in details:
			administration_charges_ac_02 = details['administration_charges_ac_02']
			update_query = ("""UPDATE `pf_challan_data` SET `administration_charges_ac_02` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (administration_charges_ac_02,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "administration_charges_ac_10" in details:
			administration_charges_ac_10 = details['administration_charges_ac_10']
			update_query = ("""UPDATE `pf_challan_data` SET `administration_charges_ac_10` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (administration_charges_ac_10,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "administration_charges_ac_21" in details:
			administration_charges_ac_21 = details['administration_charges_ac_21']
			update_query = ("""UPDATE `pf_challan_data` SET `administration_charges_ac_21` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (administration_charges_ac_21,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "administration_charges_ac_22" in details:
			administration_charges_ac_22 = details['administration_charges_ac_22']
			update_query = ("""UPDATE `pf_challan_data` SET `administration_charges_ac_22` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (administration_charges_ac_22,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "administration_charges_ac_total" in details:
			administration_charges_ac_total = details['administration_charges_ac_total']
			update_query = ("""UPDATE `pf_challan_data` SET `administration_charges_ac_total` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (administration_charges_ac_total,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "administration_charges_ac_total" in details:
			administration_charges_ac_total = details['administration_charges_ac_total']
			update_query = ("""UPDATE `pf_challan_data` SET `administration_charges_ac_total` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (administration_charges_ac_total,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employers_share_of_ac_01" in details:
			employers_share_of_ac_01 = details['employers_share_of_ac_01']
			update_query = ("""UPDATE `pf_challan_data` SET `employers_share_of_ac_01` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employers_share_of_ac_01,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employers_share_of_ac_02" in details:
			employers_share_of_ac_02 = details['employers_share_of_ac_02']
			update_query = ("""UPDATE `pf_challan_data` SET `employers_share_of_ac_02` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employers_share_of_ac_02,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employers_share_of_ac_10" in details:
			employers_share_of_ac_10 = details['employers_share_of_ac_10']
			update_query = ("""UPDATE `pf_challan_data` SET `employers_share_of_ac_10` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employers_share_of_ac_10,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employers_share_of_ac_21" in details:
			employers_share_of_ac_21 = details['employers_share_of_ac_21']
			update_query = ("""UPDATE `pf_challan_data` SET `employers_share_of_ac_21` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employers_share_of_ac_21,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employers_share_of_ac_22" in details:
			employers_share_of_ac_22 = details['employers_share_of_ac_22']
			update_query = ("""UPDATE `pf_challan_data` SET `employers_share_of_ac_22` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employers_share_of_ac_22,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employers_share_of_ac_total" in details:
			employers_share_of_ac_total = details['employers_share_of_ac_total']
			update_query = ("""UPDATE `pf_challan_data` SET `employers_share_of_ac_total` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employers_share_of_ac_total,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employees_share_of_ac_01" in details:
			employees_share_of_ac_01 = details['employees_share_of_ac_01']
			update_query = ("""UPDATE `pf_challan_data` SET `employees_share_of_ac_01` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employees_share_of_ac_01,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employees_share_of_ac_02" in details:
			employees_share_of_ac_02 = details['employees_share_of_ac_02']
			update_query = ("""UPDATE `pf_challan_data` SET `employees_share_of_ac_02` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employees_share_of_ac_02,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employees_share_of_ac_10" in details:
			employees_share_of_ac_10 = details['employees_share_of_ac_10']
			update_query = ("""UPDATE `pf_challan_data` SET `employees_share_of_ac_10` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employees_share_of_ac_10,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employees_share_of_ac_21" in details:
			employees_share_of_ac_21 = details['employees_share_of_ac_21']
			update_query = ("""UPDATE `pf_challan_data` SET `employees_share_of_ac_21` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employees_share_of_ac_21,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employees_share_of_ac_22" in details:
			employees_share_of_ac_22 = details['employees_share_of_ac_22']
			update_query = ("""UPDATE `pf_challan_data` SET `employees_share_of_ac_22` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employees_share_of_ac_22,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "employees_share_of_ac_total" in details:
			employees_share_of_ac_total = details['employees_share_of_ac_total']
			update_query = ("""UPDATE `pf_challan_data` SET `employees_share_of_ac_total` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (employees_share_of_ac_total,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "ac_no_1_employer_share_rs_pmrpy_data" in details:
			ac_no_1_employer_share_rs_pmrpy_data = details['ac_no_1_employer_share_rs_pmrpy_data']
			update_query = ("""UPDATE `pf_challan_data` SET `ac_no_1_employer_share_rs_pmrpy_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (ac_no_1_employer_share_rs_pmrpy_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "ac_no_1_employers_share_rs_pmgky_data" in details:
			ac_no_1_employers_share_rs_pmgky_data = details['ac_no_1_employers_share_rs_pmgky_data']
			update_query = ("""UPDATE `pf_challan_data` SET `ac_no_1_employers_share_rs_pmgky_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (ac_no_1_employers_share_rs_pmgky_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "ac_no_10_Pension_fund_rs_pmrpy_data" in details:
			ac_no_10_Pension_fund_rs_pmrpy_data = details['ac_no_10_Pension_fund_rs_pmrpy_data']
			update_query = ("""UPDATE `pf_challan_data` SET `ac_no_10_Pension_fund_rs_pmrpy_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (ac_no_10_Pension_fund_rs_pmrpy_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "ac_no_10_Pension_fund_rs_pmgky_data" in details:
			ac_no_10_Pension_fund_rs_pmgky_data = details['ac_no_10_Pension_fund_rs_pmgky_data']
			update_query = ("""UPDATE `pf_challan_data` SET `ac_no_10_Pension_fund_rs_pmgky_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (ac_no_10_Pension_fund_rs_pmgky_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "ac_no_1_employee_share_rs_pmrpy_data" in details:
			ac_no_1_employee_share_rs_pmrpy_data = details['ac_no_1_employee_share_rs_pmrpy_data']
			update_query = ("""UPDATE `pf_challan_data` SET `ac_no_1_employee_share_rs_pmrpy_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (ac_no_1_employee_share_rs_pmrpy_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "ac_no_1_employee_share_rs_pmgky_data" in details:
			ac_no_1_employee_share_rs_pmgky_data = details['ac_no_1_employee_share_rs_pmgky_data']
			update_query = ("""UPDATE `pf_challan_data` SET `ac_no_1_employee_share_rs_pmgky_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (ac_no_1_employee_share_rs_pmgky_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_a_b_c_rs_pmrpy_data" in details:
			total_a_b_c_rs_pmrpy_data = details['total_a_b_c_rs_pmrpy_data']
			update_query = ("""UPDATE `pf_challan_data` SET `total_a_b_c_rs_pmrpy_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_a_b_c_rs_pmrpy_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_a_b_c_rs_pmgky_data" in details:
			total_a_b_c_rs_pmgky_data = details['total_a_b_c_rs_pmgky_data']
			update_query = ("""UPDATE `pf_challan_data` SET `total_a_b_c_rs_pmgky_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_a_b_c_rs_pmgky_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "grand_total" in details:
			grand_total = details['grand_total']
			update_query = ("""UPDATE `pf_challan_data` SET `grand_total` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (grand_total,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_remittance_by_employer_rs" in details:
			total_remittance_by_employer_rs = details['total_remittance_by_employer_rs']
			update_query = ("""UPDATE `pf_challan_data` SET `total_remittance_by_employer_rs` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_remittance_by_employer_rs,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_remittance_by_employer_rs_pmgky" in details:
			total_remittance_by_employer_rs_pmgky = details['total_remittance_by_employer_rs_pmgky']
			update_query = ("""UPDATE `pf_challan_data` SET `total_remittance_by_employer_rs_pmgky` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_remittance_by_employer_rs_pmgky,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_amount_of_uploaded_ECR" in details:
			total_amount_of_uploaded_ECR = details['total_amount_of_uploaded_ECR']
			update_query = ("""UPDATE `pf_challan_data` SET `total_amount_of_uploaded_ECR` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (total_amount_of_uploaded_ECR,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "due_for_the_wages_month_of_data" in details:
			due_for_the_wages_month_of_data = details['due_for_the_wages_month_of_data']
			update_query = ("""UPDATE `pf_challan_data` SET `due_for_the_wages_month_of_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (due_for_the_wages_month_of_data,pf_challan_id)
			cursor.execute(update_query,update_data)

		if details and "due_for_the_wages_year_of_data" in details:
			due_for_the_wages_year_of_data = details['due_for_the_wages_year_of_data']
			update_query = ("""UPDATE `pf_challan_data` SET `due_for_the_wages_year_of_data` = %s
				WHERE `pf_challan_id` = %s """)
			update_data = (due_for_the_wages_year_of_data,pf_challan_id)
			cursor.execute(update_query,update_data)



		get_pf_challan_query = ("""SELECT * from `pf_challan_data` WHERE `pf_challan_id` = %s""")
		get_pf_challan_data = (pf_challan_id)
		get_pf_challan_details_count = cursor.execute(get_pf_challan_query,get_pf_challan_data)

		if get_pf_challan_details_count > 0:
			pf_challan_details_data = cursor.fetchone()
			pf_challan_details_data['last_update_ts'] = str(pf_challan_details_data['last_update_ts'])
		else:
			pf_challan_details_data = {}

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update PF Challan Data Successfully",
								"status": "success"},
				"responseList": pf_challan_details_data}), status.HTTP_200_OK

#----------------------Update-PF-Challan-Data---------------------#

#----------------------Update-PF-Payment-Data---------------------#

@name_space.route("/updatePfPaymentData/<int:pf_payment_id>")
class updatePfPaymentData(Resource):
	@api.expect(pf_payment_putmodel)
	def put(self, pf_payment_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		print(details)

		if details and "trrn_data" in details:
			trrn_data = details['trrn_data']
			update_query = ("""UPDATE `pf_payment_data` SET `trrn_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (trrn_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_status_data" in details:
			challan_status_data = details['challan_status_data']
			update_query = ("""UPDATE `pf_payment_data` SET `challan_status_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (challan_status_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_generated_on_data" in details:
			challan_generated_on_data = details['challan_generated_on_data']
			update_query = ("""UPDATE `pf_payment_data` SET `challan_generated_on_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (challan_generated_on_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "establishment_id_data" in details:
			establishment_id_data = details['establishment_id_data']
			update_query = ("""UPDATE `pf_payment_data` SET `establishment_id_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (establishment_id_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "challan_type_data" in details:
			challan_type_data = details['challan_type_data']
			update_query = ("""UPDATE `pf_payment_data` SET `challan_type_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (challan_type_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "wages_month_data" in details:
			wages_month_data = details['wages_month_data']
			update_query = ("""UPDATE `pf_payment_data` SET `wages_month_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (wages_month_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "total_amount_rs_data" in details:
			total_amount_rs_data = details['total_amount_rs_data']
			update_query = ("""UPDATE `pf_payment_data` SET `total_amount_rs_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (total_amount_rs_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "account_1_amount_rs_data" in details:
			account_1_amount_rs_data = details['account_1_amount_rs_data']
			update_query = ("""UPDATE `pf_payment_data` SET `account_1_amount_rs_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (account_1_amount_rs_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "account_2_amount_rs_data" in details:
			account_2_amount_rs_data = details['account_2_amount_rs_data']
			update_query = ("""UPDATE `pf_payment_data` SET `account_2_amount_rs_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (account_2_amount_rs_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "account_10_amount_rs_data" in details:
			account_10_amount_rs_data = details['account_10_amount_rs_data']
			update_query = ("""UPDATE `pf_payment_data` SET `account_10_amount_rs_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (account_10_amount_rs_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "account_21_amount_rs_data" in details:
			account_21_amount_rs_data = details['account_21_amount_rs_data']
			update_query = ("""UPDATE `pf_payment_data` SET `account_21_amount_rs_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (account_21_amount_rs_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "account_22_amount_rs_data" in details:
			account_22_amount_rs_data = details['account_22_amount_rs_data']
			update_query = ("""UPDATE `pf_payment_data` SET `account_22_amount_rs_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (account_22_amount_rs_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "payment_confirmation_bank_data" in details:
			payment_confirmation_bank_data = details['payment_confirmation_bank_data']
			update_query = ("""UPDATE `pf_payment_data` SET `payment_confirmation_bank_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (payment_confirmation_bank_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "crn_data" in details:
			crn_data = details['crn_data']
			update_query = ("""UPDATE `pf_payment_data` SET `crn_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (crn_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "payment_date_data" in details:
			payment_date_data = details['payment_date_data']
			update_query = ("""UPDATE `pf_payment_data` SET `payment_date_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (payment_date_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "payment_confirmation_date_data" in details:
			payment_confirmation_date_data = details['payment_confirmation_date_data']
			update_query = ("""UPDATE `pf_payment_data` SET `payment_confirmation_date_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (payment_confirmation_date_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		if details and "total_pmrpy_benefit_data" in details:
			total_pmrpy_benefit_data = details['total_pmrpy_benefit_data']
			update_query = ("""UPDATE `pf_payment_data` SET `total_pmrpy_benefit_data` = %s
				WHERE `pf_payment_id` = %s """)
			update_data = (total_pmrpy_benefit_data,pf_payment_id)
			cursor.execute(update_query,update_data)

		get_pf_payment_query = ("""SELECT * from `pf_payment_data` WHERE `pf_payment_id` = %s""")
		get_pf_payment_data = (pf_payment_id)
		get_pf_payment_details_count = cursor.execute(get_pf_payment_query,get_pf_payment_data)

		if get_pf_payment_details_count > 0:
			pf_payment_details_data = cursor.fetchone()
			pf_payment_details_data['last_update_ts'] = str(pf_payment_details_data['last_update_ts'])
		else:
			pf_payment_details_data = {}

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update PF Payment Data Successfully",
								"status": "success"},
				"responseList": pf_payment_details_data}), status.HTTP_200_OK

#----------------------Update-PF-Payment-Data---------------------#

#----------------------Update-TDS-Challan-Data---------------------#

@name_space.route("/updateTdsChallanData/<int:tds_challan_id>")
class updateTdsChallanData(Resource):
	@api.expect(tds_challan_putmodel)
	def put(self, tds_challan_id):
		connection = mysql_connection()
		cursor = connection.cursor()
		details = request.get_json()

		if details and "name_of_the_assessee_data" in details:
			name_of_the_assessee_data = details['name_of_the_assessee_data']
			update_query = ("""UPDATE `tds_challan_data` SET `name_of_the_assessee_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (name_of_the_assessee_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "complete_address" in details:
			complete_address = details['complete_address']
			update_query = ("""UPDATE `tds_challan_data` SET `complete_address` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (complete_address,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "tan_data" in details:
			tan_data = details['tan_data']
			update_query = ("""UPDATE `tds_challan_data` SET `tan_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (tan_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "major_head_data" in details:
			major_head_data = details['major_head_data']
			update_query = ("""UPDATE `tds_challan_data` SET `major_head_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (major_head_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "nature_of_the_payment_data" in details:
			nature_of_the_payment_data = details['nature_of_the_payment_data']
			update_query = ("""UPDATE `tds_challan_data` SET `nature_of_the_payment_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (nature_of_the_payment_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "basic_tax_data" in details:
			basic_tax_data = details['basic_tax_data']
			update_query = ("""UPDATE `tds_challan_data` SET `basic_tax_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (basic_tax_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "surcharge_data" in details:
			surcharge_data = details['surcharge_data']
			update_query = ("""UPDATE `tds_challan_data` SET `surcharge_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (surcharge_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "education_cess_data" in details:
			education_cess_data = details['education_cess_data']
			update_query = ("""UPDATE `tds_challan_data` SET `education_cess_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (education_cess_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "penalty_data" in details:
			penalty_data = details['penalty_data']
			update_query = ("""UPDATE `tds_challan_data` SET `penalty_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (penalty_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "oters_data" in details:
			oters_data = details['oters_data']
			update_query = ("""UPDATE `tds_challan_data` SET `oters_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (oters_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "interest_data" in details:
			interest_data = details['interest_data']
			update_query = ("""UPDATE `tds_challan_data` SET `interest_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (interest_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "fee_under_Sec_e_data" in details:
			fee_under_Sec_e_data = details['fee_under_Sec_e_data']
			update_query = ("""UPDATE `tds_challan_data` SET `fee_under_Sec_e_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (fee_under_Sec_e_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "total_data" in details:
			total_data = details['total_data']
			update_query = ("""UPDATE `tds_challan_data` SET `total_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (total_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "challan_no_data" in details:
			challan_no_data = details['challan_no_data']
			update_query = ("""UPDATE `tds_challan_data` SET `challan_no_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (challan_no_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "bsr_code_data" in details:
			bsr_code_data = details['bsr_code_data']
			update_query = ("""UPDATE `tds_challan_data` SET `bsr_code_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (bsr_code_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "date_of_receipt_data" in details:
			date_of_receipt_data = details['date_of_receipt_data']
			update_query = ("""UPDATE `tds_challan_data` SET `date_of_receipt_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (date_of_receipt_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "challan_serial_no_data" in details:
			challan_serial_no_data = details['challan_serial_no_data']
			update_query = ("""UPDATE `tds_challan_data` SET `challan_serial_no_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (challan_serial_no_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "assessment_year_data" in details:
			assessment_year_data = details['assessment_year_data']
			update_query = ("""UPDATE `tds_challan_data` SET `assessment_year_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (assessment_year_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "bank_reference_data" in details:
			bank_reference_data = details['bank_reference_data']
			update_query = ("""UPDATE `tds_challan_data` SET `bank_reference_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (bank_reference_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "drawn_on_data" in details:
			drawn_on_data = details['drawn_on_data']
			update_query = ("""UPDATE `tds_challan_data` SET `drawn_on_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (drawn_on_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "rupees_in_words_data" in details:
			rupees_in_words_data = details['rupees_in_words_data']
			update_query = ("""UPDATE `tds_challan_data` SET `rupees_in_words_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (rupees_in_words_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "cin_data" in details:
			cin_data = details['cin_data']
			update_query = ("""UPDATE `tds_challan_data` SET `cin_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (cin_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "debit_acount_no_data" in details:
			debit_acount_no_data = details['debit_acount_no_data']
			update_query = ("""UPDATE `tds_challan_data` SET `debit_acount_no_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (debit_acount_no_data,tds_challan_id)
			cursor.execute(update_query,update_data)

		if details and "payment_realization_date_data" in details:
			payment_realization_date_data = details['payment_realization_date_data']
			update_query = ("""UPDATE `tds_challan_data` SET `payment_realization_date_data` = %s
				WHERE `tds_challan_id` = %s """)
			update_data = (payment_realization_date_data,tds_challan_id)
			cursor.execute(update_query,update_data)



		get_tds_challan_query = ("""SELECT * from `tds_challan_data` WHERE `tds_challan_id` = %s""")
		get_tds_challan_data = (tds_challan_id)
		get_tds_challan_details_count = cursor.execute(get_tds_challan_query,get_tds_challan_data)

		if get_tds_challan_details_count > 0:
			tds_challan_details_data = cursor.fetchone()
			tds_challan_details_data['last_update_ts'] = str(tds_challan_details_data['last_update_ts'])
		else:
			tds_challan_details_data = {}

		connection.commit()
		cursor.close()

		return ({"attributes": {"status_desc": "Update TDS Challan Data Successfully",
								"status": "success"},
				"responseList": tds_challan_details_data}), status.HTTP_200_OK



#----------------------Update-TDS-Challan-Data---------------------#








