import sys,os
BASE_PATH = os.path.dirname(
	os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0,BASE_PATH)
from lib.main import Main
from conf.setting import CASE_PATH,HOST_INFO
import threading

def single_run(sit):
	'''
	单线程运行
	:return:
	'''
	if sit in HOST_INFO:
		host = HOST_INFO.get(sit)
	else:
		print('请输入正确的环境名称，环境有：'
			  'dev:开发环境'
			  'test:测试环境'
			  'pre:预生产环境'
			  )
		return
	for case_file in os.listdir(CASE_PATH):
		if case_file.endswith('.xls') or case_file.endswith('.xlsx'):
			abs_case_file = os.path.join(CASE_PATH,case_file)
			my_test = Main(abs_case_file,host)
			my_test.main()

def multi_run(sit):
	if sit in HOST_INFO:
		host = HOST_INFO.get(sit)
	else:
		print('请输入正确的环境名称，环境有：\n'
			  'dev:开发环境\n'
			  'test:测试环境\n'
			  'pre:预生产环境'
			  )
		return
	for case_file in os.listdir(CASE_PATH):
		if case_file.endswith('.xls') or case_file.endswith('.xlsx'):
			abs_case_file = os.path.join(CASE_PATH,case_file)
			my_test = Main(abs_case_file,host)
			t = threading.Thread(target=my_test.main)
			t.start()

multi_run('test')