import os
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(BASE_PATH,'report') #存放报告的目录
DATA_PATH = os.path.join(BASE_PATH,'data')#存放执行完之后excel的目录
CASE_PATH = os.path.join(BASE_PATH,'cases')#放case的目录

EMAIL_INFO = {
	'username':'18301096410@163.com',#发件箱
	'password':'sj1992',#邮箱授权码
	'recv':['511402865@qq.com','174596537@qq.com'],#收件人
	'email_host':'smtp.163.com',#邮箱host
	'port':25,#端口号
	'ssl':False#是否为ssl
}#邮箱信息

EMAIL_CONTENT_FORMAT='''
各位好！
	本次测试结果如下：
	{}
'''

HOST_INFO = {
	'dev':'http://dev.nnzhp.cn',
	'test':'http://test.nnzhp.cn',
	'pre':'http://api.nnzhp.cn'
}
#对应的环境信息