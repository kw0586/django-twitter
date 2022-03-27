from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now


class Tweet(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text = 'who posts this tweet',
    )

    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')

    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) #只有创建的时候会更细数值
    # updated_at = models.DateTimeField(auto_now=True) #每次更改的时候都会更新数值

    @property
    def hours_to_now(self):
        # datetime.now 不带时区信息，需要增加上 utc 的时区信息
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        # 这里是你执行 print(tweet instance) 的时候会显示的内容
        return f'{self.created_at} {self.user}: {self.content}'