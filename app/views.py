from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from .forms import PostCreateFormSet
from .models import Post


def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。::

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def index(request):
    post_list = Post.objects.order_by('-date')
    page_obj = paginate_queryset(request, post_list, 3)
    formset = PostCreateFormSet(request.POST or None, queryset=page_obj.object_list)

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return redirect('app:index')

    context = {
        'formset': formset,
        'page_obj': page_obj,
    }

    return render(request, 'app/post_formset.html', context)
