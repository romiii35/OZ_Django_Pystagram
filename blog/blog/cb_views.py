from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CommentForm
from blog.models import Blog, Comment
from django.db.models import Q
from django.urls import reverse




# url에 적어도 되지만. 너무 길어질거 같아, 임의로 파일을 만들고.. 여기에 만들어 둘 생각 이다.

class BlogListView(ListView):
    # model = Blog ==>이렇게 가져 오면, Blog.objects.all()==>모든걸 가져온다... 가 생긴다.
    # 아니면 'model = Blog'를 사용하고. class 아래에 'ordering = ('-created_at')'넣어줘도 괜찮다.
    queryset = Blog.objects.all().order_by('-created_at')
    template_name = 'blog_list.html'
    paginate_by = 10
    # ordering = ('-created_at')


    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset

class BlogDetailView(DetailView):
    model = Blog
    queryset = Blog.objects.all().prefetch_related('comment_set', 'comment_set__author')
    template_name = 'blog_detail.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     return queryset.filter(id__lte=50)
    #
    # def get_object(self, queryset=None):
    #     object = super().get_object()
    #     object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #
    #     return object
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, *args, **kwargs):
        comment_form = CommentForm(self.request.POST)

        if not comment_form.is_valid():
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            context['comment_form'] = comment_form
            return self.render_to_response(context)

        if not self.request.user.is_authenticated:
            raise Http404


        comment = comment_form.save(commit=False)
        # comment.blog = self.get_object()
        comment.blog_id = self.kwargs['pk']
        comment.author = self.request.user
        comment.save()

        return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'pk': self.kwargs['pk']}))


class BlogCreateView(LoginRequiredMixin, CreateView):
        model = Blog
        template_name = 'blog_form.html'
        fields = ('category', 'title', 'content')
        # success_url = reverse_lazy('cb_blog_list')
        # success_url = reverse_lazy('cb_blog_detail', kwargs={'pk': object.pk})
        # 변경 가는한것을 넣어 줄때에는 'success_url'을 넣는것이 아닌, 함수에 'def get_success_url'이라는 함수를 만들어준다.


        def form_valid(self, form):
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())

        # def get_success_url(self):
        #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['sub_title'] = '작성'
            context['btn_name'] = '생성'
            return context

        #     test_dict = {
        #         'a': 1,
        #         'b': 2,
        #         'c': 3
        #     }
        #
        #     self.test(a=test_dict['a'], b=test_dict['b'], c=test_dict['c'])
        #     self.test(**test_dict)
        #
        #     test_list = [1, 2, 3]
        #     self.test(test_list[0], test_list[1], test_list[2])
        #     self.test(*test_list)
        #
        # def test(self, a, b, c):
        #     return


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ('category', 'title', 'content')

    def get_queryset(self):
        queryset = super().get_queryset()
        if  self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context


    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #         raise Http404
    #     return self.object

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(author=self.request.user)
        return queryset
    #   update 부분이랑 똑같은 의미를 가진다.
    #   코드가 길어지면(조건이 많아지면) 'if not'을 쓰는 것을 추천한다. 코드가 깔끔해진다.('if'안에 'if'안에.. 하고 많이 안들어 갈수 있다.)
    def get_success_url(self):
        return reverse_lazy('blog:list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404


    def form_valid(self, form):
        blog = self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = blog
        self.object.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': blog.pk}))

    def get_blog(self):
        pk = self.kwargs['blog_pk']
        blog = get_object_or_404(Blog, pk=pk)
        return blog

