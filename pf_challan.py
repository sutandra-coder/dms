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

pf_challan = Blueprint('pf_challan_api', __name__)
api = Api(pf_challan,  title='Dms API',description='DMS API')
name_space = api.namespace('pfChallan',description='Dms Section')

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
		establishment_code_key = 0
		establishment_code_and_name_data = ''
		establishment_code = ''
		establishment_name = ''
		address_key = 0
		address_data = ''
		due_for_the_wages_month_of_key = 0
		due_for_the_wages_month_of_data = ''

		due_for_the_wages_year_of_key = 0
		due_for_the_wages_year_of_data = ''

		total_subscribers_epf_key = 0
		total_subscribrs_epf_data = ''
		total_subscribrs_eps_key = 0
		total_subscribrs_eps_data = ''
		total_subscribrs_edli_key = 0
		total_subscribrs_edli_data = ''

		total_wages_epf_key = 0
		total_wages_epf_data = ''
		total_wages_eps_key = 0
		total_wages_eps_data = ''
		total_wages_edli_key = 0
		total_wages_edli_data = ''

		admininstarion_charges_ac_01_key = 0
		administration_charges_ac_01_data = ''
		admininstarion_charges_ac_02_key = 0
		admininstarion_charges_ac_02_data = ''
		admininstarion_charges_ac_10_key = 0
		admininstarion_charges_ac_10_data = ''
		admininstarion_charges_ac_21_key = 0
		admininstarion_charges_ac_21_data = ''
		admininstarion_charges_ac_22_key = 0
		admininstarion_charges_ac_22_data = ''
		admininstarion_charges_total_key = 0
		admininstarion_charges_total_data = ''

		employers_share_Of_ac_01_key = 0
		employers_share_Of_ac_01_data =''
		employers_share_Of_ac_02_key = 0
		employers_share_Of_ac_02_data = ''
		employers_share_Of_ac_10_key = 0
		employers_share_Of_ac_10_data = ''
		employers_share_Of_ac_21_key = 0
		employers_share_Of_ac_21_data = ''
		employers_share_Of_ac_22_key = 0
		employers_share_Of_ac_22_data = ''
		employers_share_Of_ac_total_key = 0
		employers_share_Of_ac_total_data = ''

		employees_share_of_ac_01_key = 0
		employees_share_of_ac_01_data = ''
		employees_share_of_ac_02_key = 0
		employees_share_of_ac_02_data = ''
		employees_share_of_ac_10_key = 0
		employees_share_of_ac_10_data = ''
		employees_share_of_ac_21_key = 0
		employees_share_of_ac_21_data = ''
		employees_share_of_ac_22_key = 0
		employees_share_of_ac_22_data = ''
		employees_share_of_ac_22_key = 0
		employees_share_of_ac_22_data = ''
		employees_share_of_ac_total_key = 0
		employees_share_of_ac_total_data = ''

		grand_total_key = 0
		grand_total_data = ''

		ac_no_1_employer_share_rs_pmrpy_key = 0
		ac_no_1_employer_share_rs_pmrpy_data = ''
		ac_no_1_employers_share_rs_pmgky_key = 0
		ac_no_1_employers_share_rs_pmgky_data = ''

		ac_no_10_Pension_fund_rs_key = 0
		ac_no_10_Pension_fund_rs_data = ''
		ac_no_10_Pension_fund_rs_pmgky_key = 0
		ac_no_10_Pension_fund_rs_pmgky_data = ''

		ac_no_1_employee_share_rs_key = 0
		ac_no_1_employee_share_rs_data = ''
		ac_no_1_employee_share_rs_pmgky_key = 0
		ac_no_1_employee_share_rs_pmgky_data = ''

		total_A_B_C_Rs_key = 0
		total_A_B_C_Rs_data = ''
		total_A_B_C_Rs_pmgky_key = 0
		total_A_B_C_Rs_pmgky_data = ''

		total_remittance_by_employer_rs_key = 0
		total_remittance_by_employer_rs_data = ''

		total_amount_of_uploaded_ecr_d_E_key = 0
		total_amount_of_uploaded_ecr_d_E_data = ''
 

		for key,data in enumerate(inputFile):
			if "TRRN" in data:
				trrn_key = key
			if "Establishment Code & Name" in data:
				establishment_code_key = key

			if "Dues for the wage month of" in data:
				due_for_the_wages_month_of_key = key+1
				due_for_the_wages_year_of_key = key+2

			if "Address" in data:
				address_key = key

			if "Total Subscribers :" in data:
				total_subscribers_epf_key = key+1
				total_subscribrs_eps_key = key+2
				total_subscribrs_edli_key = key+3

			if "Total Wages :" in data:
				total_wages_epf_key = key+1
				total_wages_eps_key = key+2
				total_wages_edli_key = key+3

			if "Administration Charges" in data:				
				admininstarion_charges_ac_01_key = key+1
				admininstarion_charges_ac_02_key = key+2
				admininstarion_charges_ac_10_key = key+3
				admininstarion_charges_ac_21_key = key+4
				admininstarion_charges_ac_22_key = key+5
				admininstarion_charges_total_key = key+6			
				employers_share_Of_ac_01_key = key+9
				employers_share_Of_ac_02_key= key+10
				employers_share_Of_ac_10_key = key+11
				employers_share_Of_ac_21_key = key+12
				employers_share_Of_ac_22_key = key+13
				employers_share_Of_ac_total_key = key+14
				employees_share_of_ac_01_key = key+17
				employees_share_of_ac_02_key = key+18
				employees_share_of_ac_10_key = key+19
				employees_share_of_ac_21_key = key+20
				employees_share_of_ac_22_key = key+21
				employees_share_of_ac_total_key = key+22



			if "Grand Total :" in data:
				grand_total_key = key+1

			if "A/C no 1 (Employer share) ( Rs.)" in data:
				ac_no_1_employer_share_rs_pmrpy_key = key+1
				ac_no_1_employers_share_rs_pmgky_key = key+2

			if "A/C no 10 (Pension fund) ( Rs.)" in data:
				ac_no_10_Pension_fund_rs_key = key+1
				ac_no_10_Pension_fund_rs_pmgky_key = key+2

			if "A/C no 1 (Employee share) ( Rs.)" in data:
				ac_no_1_employee_share_rs_key = key+1
				ac_no_1_employee_share_rs_pmgky_key = key+2

			if "Total (A + B + C) ( Rs." in data:
				total_A_B_C_Rs_key = key+1
				total_A_B_C_Rs_pmgky_key = key+2

			if "Total remittance by Employer (Rs.)" in data:
				total_remittance_by_employer_rs_key = key+1

			if "Total amount of uploaded ECR (D + E)" in data:
				total_amount_of_uploaded_ecr_d_E_key = key+1


			if trrn_key == key:
				trrn_data = data
			if establishment_code_key == key:
				establishment_code_and_name_data = data
			if address_key == key:
				address_data = data

			if due_for_the_wages_month_of_key == key:
				due_for_the_wages_month_of_data = data

			if due_for_the_wages_year_of_key == key:
				due_for_the_wages_year_of_data = data

			if total_subscribers_epf_key == key:
				total_subscribers_epf_data = data
			if total_subscribrs_eps_key == key:
				total_subscribrs_eps_data = data
			if total_subscribrs_edli_key == key:
				total_subscribrs_edli_data = data

			if total_wages_epf_key == key:
				total_wages_epf_data = data
			if total_wages_eps_key == key:
				total_wages_eps_data = data
			if total_wages_edli_key == key:
				total_wages_edli_data = data

			if admininstarion_charges_ac_01_key == key:
				administration_charges_ac_01_data = data
			if admininstarion_charges_ac_02_key == key:
				admininstarion_charges_ac_02_data = data
			if admininstarion_charges_ac_10_key == key:
				admininstarion_charges_ac_10_data = data
			if admininstarion_charges_ac_21_key == key:
				admininstarion_charges_ac_21_data = data
			if admininstarion_charges_ac_22_key == key:
				admininstarion_charges_ac_22_data = data
			if admininstarion_charges_total_key == key:
				admininstarion_charges_total_data = data

			if employers_share_Of_ac_01_key == key:
				employers_share_Of_ac_01_data = data	
			if employers_share_Of_ac_02_key == key:
				employers_share_Of_ac_02_data = data	
			if employers_share_Of_ac_10_key == key:
				employers_share_Of_ac_10_data = data
			if 	employers_share_Of_ac_21_key == key:
				employers_share_Of_ac_21_data = data
			if employers_share_Of_ac_22_key == key:
				employers_share_Of_ac_22_data = data
			if employers_share_Of_ac_total_key == key:
				employers_share_Of_ac_total_data = data

			if employees_share_of_ac_01_key == key:
				employees_share_of_ac_01_data = data
			if employees_share_of_ac_02_key == key:
				employees_share_of_ac_02_data = data
			if employees_share_of_ac_10_key == key:
				employees_share_of_ac_10_data = data
			if employees_share_of_ac_21_key == key:
				employees_share_of_ac_21_data = data
			if employees_share_of_ac_22_key == key:
				employees_share_of_ac_22_data = data
			if employees_share_of_ac_total_key == key:
				employees_share_of_ac_total_data = data

			if grand_total_key == key:
				grand_total_data = data

			if ac_no_1_employer_share_rs_pmrpy_key == key:
				ac_no_1_employer_share_rs_pmrpy_data = data
			if ac_no_1_employers_share_rs_pmgky_key == key:
				ac_no_1_employers_share_rs_pmgky_data = data

			if ac_no_10_Pension_fund_rs_key == key:
				ac_no_10_Pension_fund_rs_data = data
			if ac_no_10_Pension_fund_rs_pmgky_key == key:
				ac_no_10_Pension_fund_rs_pmgky_data = data

			if ac_no_1_employee_share_rs_key == key:
				ac_no_1_employee_share_rs_data = data
			if ac_no_1_employee_share_rs_pmgky_key == key:
				ac_no_1_employee_share_rs_pmgky_data = data


			if total_A_B_C_Rs_key == key:
				total_A_B_C_Rs_data = data
			if total_A_B_C_Rs_pmgky_key == key:
				total_A_B_C_Rs_pmgky_data = data

			if total_remittance_by_employer_rs_key == key:
				total_remittance_by_employer_rs_data = data

			if total_amount_of_uploaded_ecr_d_E_key == key:
				total_amount_of_uploaded_ecr_d_E_data = data


		trrn_string = trrn_data.split(' ')
		trrn_data = trrn_string[1]
		establishment_code_and_name_data_string = establishment_code_and_name_data.split(' ')			
		establishment_code = establishment_code_and_name_data_string[4]
		establishment_name = establishment_code_and_name_data_string[5]+" "+establishment_code_and_name_data_string[6]+" "+establishment_code_and_name_data_string[7]+" "+establishment_code_and_name_data_string[8]+" "+establishment_code_and_name_data_string[9]

		address_data_string = address_data.split(':')
		address_data = address_data_string[1]

		print(due_for_the_wages_month_of_data)
		print(due_for_the_wages_year_of_data)
		
		print(total_subscribers_epf_data)
		print(total_subscribrs_eps_data)
		print(total_subscribrs_edli_data)
		print(total_wages_epf_data)
		print(total_wages_eps_data)
		print(total_wages_edli_data)
		print(administration_charges_ac_01_data)
		print(admininstarion_charges_ac_02_data)
		print(admininstarion_charges_ac_10_data)
		print(admininstarion_charges_ac_21_data)
		print(admininstarion_charges_ac_22_data)
		print(admininstarion_charges_total_data)
		print(employers_share_Of_ac_01_data)
		print(employers_share_Of_ac_02_data)
		print(employers_share_Of_ac_10_data)
		print(employers_share_Of_ac_21_data)
		print(employers_share_Of_ac_22_data)
		print(employers_share_Of_ac_total_data)
		print(employees_share_of_ac_01_data)
		print(employees_share_of_ac_02_data)
		print(employees_share_of_ac_10_data)
		print(employees_share_of_ac_21_data)
		print(employees_share_of_ac_22_data)
		print(employees_share_of_ac_total_data)
		print(grand_total_data)
		print(ac_no_1_employer_share_rs_pmrpy_data)
		print(ac_no_1_employers_share_rs_pmgky_data)
		print(ac_no_10_Pension_fund_rs_data)
		print(ac_no_10_Pension_fund_rs_pmgky_data)
		print(ac_no_1_employee_share_rs_data)
		print(ac_no_1_employee_share_rs_pmgky_data)
		print(total_A_B_C_Rs_data)
		print(total_A_B_C_Rs_pmgky_data)
		print(total_remittance_by_employer_rs_data)
		print(total_amount_of_uploaded_ecr_d_E_data)

		insert_query = ("""INSERT INTO `pf_challan_data` (`trn`, `establishment_code`, 
			`establishment_name`, `address`, `total_subscribers_epf`, `total_subscribers_eps`, `total_subscribers_edli`, 
			`total_wages_epf`, `total_wages_eps`, `administration_charges_ac_01`, `administration_charges_ac_02`, 
			`administration_charges_ac_10`, `administration_charges_ac_21`, `administration_charges_ac_22`, 
			`administration_charges_ac_total`, `employers_share_of_ac_01`, `employers_share_of_ac_02`, 
			`employers_share_of_ac_10`, `employers_share_of_ac_21`, `employers_share_of_ac_22`, 
			`total_wages_edli`, `employers_share_of_ac_total`, `employees_share_of_ac_01`, 
			`employees_share_of_ac_02`,`employees_share_of_ac_10`, `employees_share_of_ac_21`, `employees_share_of_ac_22`, 
			`employees_share_of_ac_total`, `ac_no_1_employer_share_rs_pmrpy_data`, 
			`ac_no_1_employers_share_rs_pmgky_data`, `ac_no_10_Pension_fund_rs_pmrpy_data`, 
			`ac_no_10_Pension_fund_rs_pmgky_data`, `ac_no_1_employee_share_rs_pmrpy_data`, 
			`ac_no_1_employee_share_rs_pmgky_data`, `total_a_b_c_rs_pmrpy_data`, `total_a_b_c_rs_pmgky_data`, 
			`grand_total`, `total_remittance_by_employer_rs`, `total_amount_of_uploaded_ECR`, 
			`due_for_the_wages_month_of_data`, `due_for_the_wages_year_of_data`, `uploading_track_details_id`, 
			`last_update_id`) 
			VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
			%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
		data = (trrn_data,establishment_code,establishment_name,address_data,total_subscribers_epf_data,
			total_subscribrs_eps_data,total_subscribrs_edli_data,total_wages_epf_data,total_wages_eps_data,
			administration_charges_ac_01_data,admininstarion_charges_ac_02_data,admininstarion_charges_ac_10_data,
			admininstarion_charges_ac_21_data,admininstarion_charges_ac_22_data,admininstarion_charges_total_data,
			employers_share_Of_ac_01_data,employers_share_Of_ac_02_data,employers_share_Of_ac_10_data,employers_share_Of_ac_21_data,
			admininstarion_charges_ac_22_data,total_wages_edli_data,employers_share_Of_ac_total_data,employees_share_of_ac_01_data,
			employees_share_of_ac_02_data,employees_share_of_ac_10_data,employees_share_of_ac_21_data,employees_share_of_ac_22_data,
			employees_share_of_ac_total_data,ac_no_1_employer_share_rs_pmrpy_data,ac_no_1_employers_share_rs_pmgky_data,
			ac_no_10_Pension_fund_rs_data,ac_no_10_Pension_fund_rs_pmgky_data,ac_no_1_employee_share_rs_data,ac_no_1_employee_share_rs_pmgky_data,
			total_A_B_C_Rs_data,total_A_B_C_Rs_pmgky_data,grand_total_data,total_remittance_by_employer_rs_data,total_amount_of_uploaded_ecr_d_E_data,
			due_for_the_wages_month_of_data,due_for_the_wages_year_of_data,
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

		