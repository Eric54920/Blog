from django.urls import path, include
from .views import web, admin

urlpatterns = [
    path('', web.home),
    path('article/<int:id>', web.article_detail, name="article_detail"),
    path('article/<int:id>/comment/', web.article_comment, name="comment"),
    path('archives/', web.archives),
    path('album/', web.album),
    path('album/<int:id>', web.album_detail, name="album"),
    path('about/', web.about),

    path('login/', admin.login, name="login"),
    path('admin/logout/', admin.logout, name="logout"),

    path('admin/', include([
        path('dashboard/', admin.dashboard, name="dashboard"),

        path('article/', admin.article, name="article"),
        path('article_edit/', admin.article_edit),
        path('article_hide/<int:id>', admin.article_hide, name="article_hide"),
        path('article_delete/<int:id>', admin.article_delete, name="article_delete"),

        path('comment/', admin.comment, name="comment"),
        path('comment/delete/', admin.comment_delete, name="comment_delete"),
        path('comment/reply/', admin.comment_reply, name="comment_reply"),

        path('album/', admin.album),
        path('album_edit/', admin.album_edit, name="album_edit"),
        path('picture_upload/', admin.picture_upload, name="picture_upload"),
        path('album/upload/<int:id>', admin.album_upload, name="album_upload"),
        path('album_hide/<int:id>', admin.album_hide, name="album_hide"),
        path('album_delete/<int:id>', admin.album_delete, name="album_delete"),
        path('picture_hide/<int:id>', admin.picture_hide, name="picture_hide"),
        path('picture_delete/<int:id>', admin.picture_delete, name="picture_delete"),

        path('about/', admin.settings),
        path('change_password/', admin.change_password, name="change_password")
    ])),
]