from django.shortcuts import render, redirect
from django.db.models import Q
from sistema_sga.core.models import Profile
from sistema_sga.artigos.models import Article

# Create your views here.


def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')
        try:
            search_type = request.GET.get('type')
            if search_type not in ['articles', 'users']:
                search_type = 'articles'
        except Exception:
            search_type = 'articles'

        count = {}
        results = {}

        results['articles'] = Article.objects.filter(
            Q(title__icontains=querystring) |
            Q(content__icontains=querystring))
        results['users'] = Profile.objects.filter(
            Q(username__icontains=querystring) | Q(
                first_name__icontains=querystring) |
            Q(last_name__icontains=querystring))

        count['articles'] = results['articles'].count()
        count['users'] = results['users'].count()

        context = {
            'hide_search': True,
            'querystring': querystring,
            'active': search_type,
            'count': count,
            'results': results[search_type]
        }

        return render(request, 'search/results.html', context)
    else:
        return render(request, 'search/search.html', {'hide_search': True})
