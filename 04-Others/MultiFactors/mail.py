import smtplib
from email.mime.text import MIMEText
msg_from='313407040@qq.com'                                 #发送方邮箱
passwd='kgxvnbvdetuabgeb'                                   #填入发送方邮箱的授权码
msg_to='zhengow@qq.com'                                  #收件人邮箱
                            
subject="python邮件测试"                                     #主题     
content="111"     
msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to
for i in range(1):
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('success')
    except Exception as e:
        print(e)
    finally:
        s.quit()