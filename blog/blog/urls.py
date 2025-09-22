from django.urls import path

from blog import cb_views

app_name = 'blog'

urlpatterns = [
    # CBV blog(class base view)
    path('', cb_views.BlogListView.as_view(), name='list'),
    path('<int:pk>/', cb_views.BlogDetailView.as_view(), name='detail'),
    path('create/', cb_views.BlogCreateView.as_view(), name='create'),
    path('<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='update'),

    path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='delete'),

]

# (% url 'blog_list' %}
# (% url 'blog;list' %} ==> include 후에는 'template/base, detail, list' 파일 안, url 부분들을 클론으로 다 바꿔주기
# cb_view 제일아래 'blog'detail'부분// models 안에 아래부분 'blog_detail'뷰뷴, views 안, member/login  아래부분, 바꿔주기