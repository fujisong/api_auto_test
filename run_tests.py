# coding:utf-8
import time, sys
import gl
sys.path.append('.\\dcxyinterface')
sys.path.append('.\\db_fixture')
from HTMLTestRunner import HTMLTestRunner
from unittest import defaultTestLoader
from db_fixture import test_data
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText

# 指定测试用例为当前文件夹下的 interface 目录
test_dir = './dcxyinterface'
testsuit = defaultTestLoader.discover(test_dir, pattern='*_test.py')

def send_Mail(file_new):
    f = open(file_new, 'rb')
    # 读取测试报告正文
    mail_body = f.read()
    f.close()
    try:
        smtp = smtplib.SMTP(gl.Smtp_Server, 25)
        sender = gl.Smtp_Sender
        password = gl.Smtp_Sender_Password
        receiver = gl.Smtp_Receiver
        smtp.login(sender,password)
        msg = MIMEMultipart()
        # 编写html类型的邮件正文，MIMEtext()用于定义邮件正文
        # 发送正文
        text = MIMEText(mail_body, 'html', 'utf-8')
        # 定义邮件正文标题
        text['Subject'] = Header('dc学院接口自动化测试报告', 'utf-8')
        msg.attach(text)
        # 发送附件
        # Header()用于定义邮件主题，主题加上时间，是为了防止主题重复，主题重复，发送太过频繁，邮件会发送不出去。
        msg['Subject'] = Header('dc学院接口自动化测试报告' + now, 'utf-8')
        msg_file = MIMEText(mail_body, 'html', 'utf-8')
        msg_file['Content-Type'] = 'application/octet-stream'
        msg_file["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        msg.attach(msg_file)
        # 定义发件人，如果不写，发件人为空
        msg['From'] = sender
        # 定义收件人，如果不写，收件人为空
        msg['To'] = ",".join(receiver)
        tmp = smtp.sendmail(sender, receiver, msg.as_string())
        print (tmp)
        smtp.quit()
        return True
    except smtplib.SMTPException as e:
        print(str(e))
        return False


if __name__ == "__main__":
#    test_data.init_data() # 初始化接口测试数据

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/' + now + u'_dc学院_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='DC学院接口自动化测试报告',
                            description='运行环境：MySQL(PyMySQL), Requests, unittest ')
    runner.run(testsuit)
    fp.close()
    mail = send_Mail(filename)
    print (mail)
    if mail:
        print(u"邮件发送成功！")
    else:
        print(u"邮件发送失败！")