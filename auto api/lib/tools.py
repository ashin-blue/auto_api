import os

import requests
import time
import xlrd
from xlutils import copy
from conf.setting import DATA_PATH
def readCase(case_path):
	case_list = [] #存放所有的测试用例，给后面运行的时候使用
	book = xlrd.open_workbook(case_path)
	sheet = book.sheet_by_index(0)
	for line in range(1,sheet.nrows):
		case = []
		line_case = sheet.row_values(line)#row_values是excel里面每一行的所有数据
		project = line_case[0]
		model = line_case[1]
		case_id = line_case[2]
		detail = line_case[3]
		url = line_case[4]
		method = line_case[5]
		req_data = line_case[6]
		hope = line_case[7]
		tester = line_case[11]
		case = [project,model,case_id,detail,url,method,req_data,hope,tester]
		case_list.append(case)
	return case_list

def strToDict(data):
	#username=niuhy,passwd=123456
	dic  = {}
	data_list = data.split(',')
	if not data_list[0]:
		return dic
	# ['username=niuhy','passwod=123456']
	for k in data_list:
		#username=niuhy
		k_list = k.split('=')
		#['usenrmae','niuhy']
		dic_k = k_list[0]
		dic_v = k_list[1]
		dic[dic_k]=dic_v
	return dic

def my_request(method,url,data):
	new_data = strToDict(data)
	try:
		if method.upper()=='GET':
			r = requests.get(url,new_data)
		else:
			r = requests.post(url,new_data)

	except Exception as e:
		return '出错了，错误是%s'%e
	return r.text

def check_res(response,hope):
	new_response = response.replace('": "','=').replace('": ','=')
	for check in hope.split(','):
		if check not in new_response:
			return '失败'
	return '通过'

def write_excel(src_case_path,res_list):
	src_book = xlrd.open_workbook(src_case_path)
	new_book = copy.copy(src_book)
	sheet = new_book.get_sheet(0)
	line = 1
	for res in res_list:
		req  = res.get('request')
		response  = res.get('response')
		status  = res.get('status')
		sheet.write(line,8,req)
		sheet.write(line,9,response)
		sheet.write(line,10,status)
		line+=1
	file_name = time.strftime('%Y%m%d%H%M%S')+os.path.basename(src_case_path)
	abs_path = os.path.join(DATA_PATH,file_name).replace('xlsx','xls')
	new_book.save(abs_path)

if __name__ =='__main__':
	# res = readCase(r'C:\Users\bjniuhanyang\Desktop\测试用例.xlsx')
	# print(res)
	# dic = strToDict('username=niuhy,passwd=123456')
	# print(dic)
	# r = my_request('get','http://lanxia.lxsb.com','a=1')
	# print(r)
	res = """
	{
    "error_code": 0,
    "login_info": {
        "login_time": "20171216171928",
        "sign": "d8f3044197d21f18bf782b0f0b7e9a8b",
        "userId": 8
    }
}
	"""
	# r = check_res(res,'error_code=0,userId=8')
	# print(r)
	res_list =[ [
		'http://api.nnzhp.cn/user?username=xxx&passwd=111','{}',True
	]
	]
	excel_path=r'C:\Users\bjniuhanyang\Desktop\测试用例.xlsx'
	write_excel(excel_path,res_list)
	# 总共运行了N条测试用例，通过xx条，失败xx。
