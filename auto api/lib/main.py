import time

from lib import tools
from lib import report
from lib import sendmail
from conf.setting import EMAIL_INFO,EMAIL_CONTENT_FORMAT

class Main():

	def __init__(self,case_path,host):
		self.case_path = case_path
		self.host = host

	def __run(self):
		start_time = time.time() #用例运行的开始时间
		self.all_res_list = [ ] #存放所有用例的返回结果
		self.pass_count = 0 #记录用例通过的次数
		case_list = tools.readCase(self.case_path)
		for case in case_list:
			res_dic = {}#存的每条用例的结果
			project = case[0]
			model = case[1]
			case_id = case[2]#用例id
			detail = case[3]#用例描述
			req_url = self.host+case[4]#请求url
			method = case[5]#请求方式
			req_data = case[6]#请求数据
			hope = case[7]#预期结果
			tester = case[8]#预期结果
			response = tools.my_request(method,req_url,req_data)
			req_param = req_url+'?'+req_data.replace(',','&')#请求报文
			case_status = tools.check_res(response,hope)#用例执行结果
			if case_status=='通过':
				self.pass_count+=1
			res_dic={
				"case_id": case_id,
				"project": project,
				"model": model,
				"detail": detail,
				"url": req_url,
				"tester": tester,
				"status": case_status,
				"request": req_param,
				"response": response
			}
			self.all_res_list.append(res_dic)
		end_time = time.time()#结束时间
		self.run_time = end_time - start_time #开始时间减去结束时间就是运行的时间

	def __result(self):
		tools.write_excel(self.case_path,self.all_res_list)#反写excel
		all_case_num = len(self.all_res_list)#总共用例条数
		fail_count = all_case_num-self.pass_count
		all = {
			"all": all_case_num,  # 总共多少条用例
			"ok": self.pass_count,  # 通过的
			"fail":fail_count ,  # 失败
			"run_time": '%.2f'%self.run_time,  # 运行了多久
			"case_res": self.all_res_list,
			"date": time.strftime('%Y/%m/%d %H:%M:%S')  # 什么时候执行的
		}
		my_report = report.HtmlReport(all)
		my_report.report()#生成html测试报告
		report_file_name = my_report.file_name #生成报告的文件名
		title = '%s接口测试报告'%time.strftime('%Y/%m/%d %H:%M:%S')
		content = EMAIL_CONTENT_FORMAT.format(
			'本次共执行%s条用例，通过%s条，失败%s条。详情见附件测试报告。'%(all_case_num,
			self.pass_count,fail_count) )
		mail_man = sendmail.SendMail(
			username=EMAIL_INFO.get('username'),
			passwd=EMAIL_INFO.get('password'),
			recv=EMAIL_INFO.get('recv'),
			email_host=EMAIL_INFO.get('email_host'),
			port=EMAIL_INFO.get('port'),
			ssl=EMAIL_INFO.get('ssl'),
			title=title,
			content=content,
			file=report_file_name
		)
		mail_man.send_mail()

	def main(self):
		self.__run()
		self.__result()
if __name__ == '__main__':
	pass