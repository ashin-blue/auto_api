import os
import time
from conf.setting import REPORT_PATH
class HtmlReport(object):
    __style_html = '''
    <style type="text/css">
    				body {
    					font:normal 68% verdana,arial,helvetica;
    					color:#000000;
    				}
    				table tr td, table tr th {
    					font-size: 68%;
    				}
    				table.details tr th{
    				    color: #ffffff;
    					font-weight: bold;
    					text-align:center;
    					background:#2674a6;
    				}
    				table.details tr td{
    					background:#eeeee0;
    				}
    				h1 {
    					margin: 0px 0px 5px; font: 165% verdana,arial,helvetica
    				}
    				h2 {
    					margin-top: 1em; margin-bottom: 0.5em; font: bold 125% verdana,arial,helvetica
    				}
    				h3 {
    					margin-bottom: 0.5em; font: bold 115% verdana,arial,helvetica
    				}
    				.Failure {
    					font-weight:bold; color:red;
    				}


    				img
    				{
    				  border-width: 0px;
    				}

    				.expand_link
    				{
    				   position=absolute;
    				   right: 0px;
    				   width: 27px;
    				   top: 1px;
    				   height: 27px;
    				}

    				.page_details
    				{
    				   display: none;
    				}

                                    .page_details_expanded
                                    {
                                        display: block;
                                        display/* hide this definition from  IE5/6 */: table-row;
                                    }


    			</style>
    <script language="JavaScript">
    		function show(details_id)
    			   {
    			      var close = 'page_details';
    			      var show = 'page_details_expanded';
    			      if (document.getElementById(details_id).className==close){
    			          document.getElementById(details_id).className = show;
    				  }
    				  else {
    			          document.getElementById(details_id).className = close;
    				  }

    			   }

    			</script>
    '''
    __report_html = '''
    <!DOCTYPE html>
    <html>
    <head>
    <META http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>接口测试报告</title>
    {style}
    </head>
    <body>
    <h1>接口测试报告</h1>
    <table width="100%">
    <tr>
    <td align="left">测试时间: {date}</td>
    </tr>
    </table>
    <hr size="1">
    	<h2>测试概况</h2>
    <table width="95%" cellspacing="2" cellpadding="5" border="0" class="details" align="center">
    <tr valign="top">
    <th>用例总数</th><th>通过数量</th><th>失败数量</th><th>运行时间</th>
    </tr>
    <tr valign="top" class="">
    <td align="center">{all}</td><td align="center">{ok}</td><td align="center">{fail}</td><td align="center">{run_time} s</td>
    </tr>
    </table>
    <hr align="center" width="95%" size="1">
    <h2>接口详细</h2>
    <table width="95%" cellspacing="2" cellpadding="5" border="0" class="details" align="center">
    <tr valign="top">
    <th>所属项目</th><th>模块</th><th>用例描述</th><th>URL</th><th>测试人员</th><th>用例状态</th><th></th>
    </tr>{case_res}</table>
    <hr align="center" width="95%" size="1">
    </body>
    </html>

    '''
    __case_html = '''
    <tr valign="top" class="">
    <td>{project}</td><td align="center">{model}</td><td align="center">{detail}</td><td align="center">{url}</td><td align="center">{tester}</td><td align="center">{status}</td><td align="center"><a href="#" onclick="show('page_details_{case_id}');">查看接口详细</a></td>
    </tr>
    <tr class="page_details" id="page_details_{case_id}">
    <td bgcolor="#FF0000" colspan="8">
    <div align="center">
    <b>请求/返回 "{project}"</b>
    <table width="95%" cellspacing="1" cellpadding="1" border="0" bgcolor="#2674A6" bordercolor="#000000">
    <tr>
    <th>请求报文</th><th>返回报文</th>
    </tr>
    <tr>
    <td align="center" style="width :300px;word-break: break-all;"><span>{request}</span></td><td align="center" style="width :300px;word-break: break-all;" ><span>{response}</span></td>

    </tr>
    </table>
    </div>
    </td>
    </tr>

    '''
    def __init__(self,report_dic):
        '''

        :param report_dic:生成报告需要用的字典
        {
            "all": 5,#运行用例数量
            "ok": 4,#通过数量
            "fail": 1,#失败数量
            "run_time": 100,#运行时间，单位s
            "case_res": [{}],#每条用例的执行结果，
            case_res:
            {
                    "case_id":"001",#用例id
                    "project":"易品",#所属项目
                    "model":"登录",#模块
                    "detail":"正常登录",#用例标题
                    "url":"http://10.165.124.28:8080/q", #请求url
                    "tester":"牛牛", #测试人员
                    "status":"通过",#测试结果
                    "request":"a=1&b=2",#请求报文
                "response":"{'code':200,'msg':'操作成功'}"#返回报文
            }
        }
        '''
        self.report_dic = report_dic
    def report(self):
        res_list_html = ''
        res_list = self.report_dic.get('case_res')
        for res in res_list:
            res_list_html+=self.__case_html.format(**res)
        self.report_dic['case_res']=res_list_html
        self.report_dic['style'] = self.__style_html
        self.report_dic['date'] = time.strftime('%Y/%m/%d %H:%M:%S')
        self.__write_file()
        return self.file_name
    def __write_file(self):
        self.file_name = os.path.join(REPORT_PATH,'{date}_TestReport.html'.format(date=time.strftime('%Y%m%d%H%M%S')))
        with open(self.file_name,'w',encoding='utf-8') as fw:
            fw.write(self.__report_html.format(**self.report_dic))


if __name__ == '__main__':


    res_list = [
    {
            "case_id":"1",
            "project":"易品",
            "model":"登录",
            "detail":"正常登录",
            "url":"http://10.165.124.28:8080/q",
            "tester":"牛牛",
            "status":"通过",
            "request":"a=1&b=2",
        "response":"{'code':200,'msg':'操作成功'}"
        }, {
            "case_id":"2",
            "project":"易品",
            "model":"登录",
            "detail":"正常登录",
            "url":"http://10.165.124.28:8080/q11111",
            "tester":"牛牛111",
            "status":"通过",
            "request":"a=1&b=2",
        "response":"{'code':200,'msg':'操作成功'}"
        },

    ]

    all = {
        "all":2,#总共多少条用例
        "ok":1,#通过的
        "fail":1,#失败
        "run_time":100,#运行了多久
        "case_res":res_list,
        "date": time.strftime('%Y/%m/%d %H:%M:%S')#什么时候执行的
    }

    a = HtmlReport(all)
    a.report()