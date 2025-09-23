from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from blog.utils.models import TimestampedModel

User = get_user_model()

# 제목
# 본문
# 작성자 => 패스(추후 업데이트)
# 작성일자
# 수정일자
# 카테고리

class Blog(TimestampedModel):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )

    category = models.CharField('카테고리', max_length=20, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # author_id = models.IntegerField()
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제가 불가능함 (유저를 삭제하려고 할때, 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL => NULL값을 넣습니다. => 유저 삭제시 블로그의 author가 null이 됨


    def __str__(self):
            return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    #위 함수 안넣으면, 'cb/33/update'로 바로 들어갈시, 에러 발생한다.

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

# category update
#  Blog.objects.filter(category='').update(category='free')

class Comment(TimestampedModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at', '-id']
    # blog
    # 댓글내용
    # 작성자
    # 작성일자
    # 수정일자
