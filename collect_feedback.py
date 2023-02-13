import datetime
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from user.models import Feedback
from utils.postmail import send_mail
from zoneinfo import ZoneInfo


class Command(BaseCommand):
    help = '收集汇总每日用户反馈'

    # 接收参数
    def add_arguments(self, parser):
        # 需要初始化的配置名称
        # parser.add_argument('config_codes', type=str, help='配置名称', nargs='*')
        pass

    def handle(self, *args, **options):
        # config_codes = options['config_codes']  # 拿到参数的值
        today0 = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
        # 起止时间24小时制
        time = 4
        start = today0 - timedelta(hours=(24 - time))
        fd_qs = Feedback.objects.filter(created_at__range=(start, today0))
        for fd in fd_qs:
            pass
        # 将fd数据插入到为html表格
        html = '<table border="1" cellspacing="0" cellpadding="0" width="100%">'
        html += '<tr><td>用户名称</td><td>用户邮箱</td><td>内容</td><td>创建时间</td></tr>'
        for fd in fd_qs:
            # 时间转换为北京时间
            created_at = fd.created_at.astimezone(ZoneInfo('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
            html += f'<tr><td>{fd.name}</td><td>{fd.email}</td><td>{fd.content}</td><td>{created_at}</td></tr>'
        html += '</table>'
        # 发送邮件
        send_mail(settings.EMAIL_HOST, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.EMAIL_PORT,['1289120437@qq.com'], html)

# settings.EMAIL_HOST           # 设置服务器
# settings.EMAIL_HOST_USER      # 用户名
# settings.EMAIL_HOST_PASSWORD  # 口令
# settings.EMAIL_PORT           # SMTP端口号
