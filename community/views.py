from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q

# Create your views here.
# class ArticleListView(ListView):
#     model = Article
#     paginate_by = 10
#     template_name = 'community/article_list.html'
#     context_object_name = 'article_list'

#     def get_queryset(self):
#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#         article_list = Article.objects.order_by('-id') 
        
#         if search_keyword :
#             if len(search_keyword) > 1 :
#                 if search_type == 'all':
#                     search_article_list = article_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (user__user_id__icontains=search_keyword))
#                 elif search_type == 'title_content':
#                     search_article_list = article_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
#                 elif search_type == 'title':
#                     search_article_list = article_list.filter(title__icontains=search_keyword)    
#                 elif search_type == 'content':
#                     search_article_list = article_list.filter(content__icontains=search_keyword)    
#                 elif search_type == 'writer':
#                     search_article_list = article_list.filter(user__user_id__icontains=search_keyword)

#                 return search_article_list
#             else:
#                 messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
#         return article_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)

#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1

#         start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index

#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range

#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#         article_fixed = Article.objects.filter(top_fixed=True).order_by('-created_at')

#         if len(search_keyword) > 1 :
#             context['q'] = search_keyword
#         context['type'] = search_type
#         context['article_fixed'] = article_fixed

#         return context

@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    
    context = {
        'articles': articles,
    }
    return render(request, 'community/index.html', context)



@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('community:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)


@require_safe
def detail(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm()
        comments = article.comment_set.all()
        context = {
            'article': article,
            'comment_form': comment_form,
            'comments': comments,
        }
        return render(request, 'community/detail.html', context)
    return redirect('accounts:login')

# @require_safe
# def detail(request, pk):
#     if request.user.is_authenticated:
#         article = get_object_or_404(Article, pk=pk)
#         session_cookie = request.user
#         print(session_cookie)
#         cookie_name = f'article_hits:{session_cookie}'
#         context = {
#             'article': article,
#         }
#         response = render(request, 'community/_card.html', context)

#         if request.COOKIES.get(cookie_name) is not None:
#             cookies = request.COOKIES.get(cookie_name)
#             cookies_list = cookies.split('|')
#             if str(pk) not in cookies_list:
#                 response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
#                 article.hits += 1
#                 article.save()
#                 return response
#         else:
#             response.set_cookie(cookie_name, pk, expires=None)
#             article.hits += 1
#             article.save()
#             return response
#         return render(request, 'community/_card.html', context)
#     return redirect('accounts:login')


# @login_required
@require_POST
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.is_authenticated:
        if request.user == article.user: 
            article.delete()
            messages.success(request, "삭제되었습니다.")
            return redirect('community:index')
    else:
        messages.error(request, "본인 게시글이 아닙니다.")
        return redirect('community:detail', article.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                messages.success(request, "수정되었습니다.")
                return redirect('community:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        messages.error(request, "본인 게시글이 아닙니다.")
        return redirect('community:detail', article.pk)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'community/update.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
        return redirect('community:detail', article.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', article_pk)