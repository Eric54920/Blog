# Blog

一个基于 Django 6 的个人博客系统，包含前台内容展示与后台内容管理。文章支持 Markdown 编辑和 HTML 预览，评论支持回复，相册通过资源 URL 管理图片和视频。

项目前身已经过依赖升级与初始化流程整理，当前使用 Django 6.1、Python 3.12+，并已提供 Docker Compose 部署方式。

## 功能

前台：

- 首页文章列表、分类筛选、标题/摘要/内容搜索
- 文章详情、目录、代码高亮
- 按年份归档
- 相册专题、图片与视频浏览
- 关于页面

后台：

- 管理员登录、退出、修改密码
- 文章创建、编辑、隐藏、删除、批量删除
- 评论查看、回复、删除、批量删除
- 相册专题与图片/视频管理
- 个人信息维护

## 技术栈

- Django 6.1
- Python 3.12+
- SQLite 或 MySQL 8
- Bootstrap 4
- editor.md
- Gunicorn
- WhiteNoise
- Docker Compose

## 快速开始

### 环境要求

- Python 3.12 或更高版本
- 可选：Docker 与 Docker Compose
- 可选：MySQL 8

### 手动初始化

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py init_admin
python manage.py runserver
```

访问地址：

- 前台首页：http://127.0.0.1:8000/
- 后台登录：http://127.0.0.1:8000/login/

默认使用 SQLite，数据库文件为 `db.sqlite3`。

### 使用 Makefile

```bash
make bootstrap
make init-admin
make run
```

`make bootstrap` 会创建 `.venv`，并在没有 `.env` 时从 `.env.example` 复制一份。

## 创建管理员

项目使用自定义 `web.User`，没有直接复用 Django 默认后台：

```bash
python manage.py init_admin
```

常用参数：

```bash
python manage.py init_admin --username admin --nickname 站长
python manage.py init_admin --username admin --password 你的密码 --force
```

- 未提供密码时命令会交互式要求输入
- `--force` 会重置已存在用户的密码
- 非交互环境必须显式提供 `--password`

## Docker 部署

复制环境变量文件并启动：

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec web python manage.py init_admin
```

容器启动时自动执行：

```text
python manage.py migrate
python manage.py collectstatic
```

若 `.env` 设置了 `ADMIN_PASSWORD`，容器首次启动会创建 `ADMIN_USERNAME` 对应的管理员账号。正式部署后建议清空该变量。

常用命令：

```bash
docker compose ps
docker compose logs -f web
docker compose exec web python manage.py init_admin
docker compose down
```

MySQL 数据保存在 Docker named volume `mysql_data` 中。

## 配置

项目只保留 `.env` 一种配置入口。复制 [.env.example](.env.example) 为 `.env` 后修改即可：

```bash
cp .env.example .env
```

常用环境变量：

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `DJANGO_DEBUG` | `true` | 开发调试模式；生产环境设为 `false` |
| `DJANGO_SECRET_KEY` | 兼容旧项目的默认密钥 | 生产环境必须替换为随机密钥 |
| `DJANGO_ALLOWED_HOSTS` | `*` | 允许访问的域名，逗号分隔 |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | 空 | HTTPS 代理场景下的可信来源 |
| `DB_ENGINE` | SQLite | 本地默认 SQLite |
| `DB_NAME` | `db.sqlite3` | SQLite 文件名或 MySQL 数据库名 |
| `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` | - | MySQL 连接参数 |
| `MYSQL_DATABASE` / `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_ROOT_PASSWORD` | `blog` | Docker MySQL 初始化参数 |
| `SITE_NAME` / `SITE_AUTHOR` / `SITE_SIGNATURE` | - | 站点基本信息 |
| `SITE_LOGO` / `SITE_AVATAR` | `images/avatar.png` | 站点 Logo 和头像 |
| `ALBUM_DESCRIPTION` | 分享点滴，记录美好 | 相册页描述 |
| `ALBUM_HEADIMG` | `images/bg.jpg` | 相册背景图 |
| `SITE_SOCIAL` | 空 | 可选 JSON 社交链接 |
| `SITE_VERIFICATION` | 空 | 可选 JSON 站点验证 |

`SITE_SOCIAL` 示例：

```bash
SITE_SOCIAL={"GITHUB":{"icon":"fa-github","url":"https://github.com/your-name"}}
```

`SITE_VERIFICATION` 示例：

```bash
SITE_VERIFICATION={"google":"your-google-verification","baidu":"your-baidu-verification"}
```

静态路径可以写成 `images/avatar.png`，模板会自动转换为 `/static/images/avatar.png`；也可以填写完整的 HTTP URL。

## 目录结构

```text
Blog/
├── Blog/                     # Django 项目配置
│   └── settings.py           # 从 .env 读取配置
├── web/                      # 博客业务应用
│   ├── forms/
│   ├── management/commands/
│   ├── migrations/
│   ├── middlewares/
│   ├── static/
│   ├── templates/
│   ├── templatetags/
│   ├── urls.py
│   ├── utils/
│   └── views/
├── compose.yaml
├── Dockerfile
├── docker-entrypoint.sh
├── requirements.txt
└── Makefile
```

## 日常开发

运行 Django 检查：

```bash
python manage.py check
```

运行测试：

```bash
python manage.py test web
```

修改模型后生成迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

收集静态文件：

```bash
python manage.py collectstatic --noinput
```

## 生产环境检查

- `DJANGO_DEBUG=false`
- `DJANGO_SECRET_KEY` 使用独立随机值
- `DJANGO_ALLOWED_HOSTS` 只包含实际域名
- `CSRF_TRUSTED_ORIGINS` 与 HTTPS 域名保持一致
- 使用 Gunicorn，不要运行 `manage.py runserver`
- 在反向代理层启用 HTTPS
- 定期备份 MySQL 数据

## 升级说明

当前依赖锁定在 [requirements.txt](requirements.txt)，Django 为 6.1.1。

从旧版本升级：

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
```

历史版本如果仍有 `local_settings.py`，需要迁移到 `.env` 后删除。密码哈希依赖 `DJANGO_SECRET_KEY`，若修改过密钥，需要重新执行 `python manage.py init_admin --force` 更新管理员密码。
