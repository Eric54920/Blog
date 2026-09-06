import getpass
import sys

from django.core.management.base import BaseCommand, CommandError

from web.models import User
from web.utils.encrypt import sha256


class Command(BaseCommand):
    help = "Create the initial blog administrator or reset an existing one."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--nickname", default="")
        parser.add_argument("--email", default="")
        parser.add_argument("--password", default="")
        parser.add_argument("--force", action="store_true", help="Reset the password when the user already exists.")
        parser.add_argument("--no-input", action="store_true", dest="no_input")

    def handle(self, *args, **options):
        username = options["username"]
        nickname = options["nickname"]
        email = options["email"]
        password = options["password"]
        force = options["force"]

        user = User.objects.filter(username=username).first()
        if user and not force:
            self.stdout.write(self.style.WARNING(f"用户 {username} 已存在，跳过创建。使用 --force 可重置密码。"))
            return

        if not password:
            if options["no_input"] or not sys.stdin.isatty():
                raise CommandError("非交互环境必须通过 --password 提供密码。")
            password = getpass.getpass("请输入后台密码（至少 8 位）: ")
            confirmed = getpass.getpass("请再次输入后台密码: ")
            if password != confirmed:
                raise CommandError("两次输入的密码不一致。")

        if len(password) < 8:
            raise CommandError("后台密码至少需要 8 位。")

        if user:
            user.nic_name = nickname or user.nic_name
            if email:
                user.email = email
            user.password = sha256(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"用户 {username} 的密码已更新。"))
        else:
            User.objects.create(
                username=username,
                nic_name=nickname or "站长",
                email=email or None,
                password=sha256(password),
            )
            self.stdout.write(self.style.SUCCESS(f"管理员 {username} 创建成功。"))
