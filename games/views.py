
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *
from django.db.models import Q
from django.template.loader import render_to_string


def paginate(max_objects, objects, page):
    paginator = Paginator(objects, max_objects)

    try:
        objects = paginator.page(page)
        return(objects)
    except EmptyPage:
        objects = paginator.page(1)
        return(objects)


def paginate_count(max_objects, objects):
    paginator = Paginator(objects, max_objects)
    return paginator.num_pages


def paginate_pages_range(page, around_page, num_pages):
    min_page = 0
    max_page = 0

    if page - around_page > 0:
            min_page = page - around_page
    else:
        for i in reversed(range(0, around_page)):
            if page - i > 0:
                min_page = page - i
                break

    if page + around_page < num_pages + 1: 
            max_page = page + around_page
    else:
        for i in reversed(range(0, around_page)):
            if page + i < num_pages + 1:
                max_page = page + i
                break
    return range(min_page, max_page + 1)

        
class GamesListView(View):
    model = Game
    template_name = 'games/list.html'
    max_objects = 6


    def get_studios(self):
        studios = []
        for studio in Studio.objects.all():
            studios.append(studio.pk)
        return studios


    def get_queryset(self):
        objects = self.model.objects.filter(
            studio__in=self.request.POST.getlist('studio', self.get_studios()),
            name__icontains=self.request.POST.get('name', ''),
            ).order_by(self.request.POST.get('order', 'name'))
        return objects
    

    def get(self, request, *args, **kwargs):
        page = 1
        objects = self.model.objects.all()
        end_page = paginate_count(self.max_objects, objects)

        return render(
            request=request,
            template_name="games/list.html",
            context={
                'games': paginate(self.max_objects, objects, page), 
                'paginate_range': paginate_pages_range(page, 2, end_page),
                'end_page': end_page,
                'page': 1,
                'filter_form': GameSortForm(),
                },
            )


    def post(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        if GameSortForm(request.POST).is_valid(): 
            objects = self.get_queryset()
            end_page = paginate_count(self.max_objects, objects)
            filter_variables = ''
            if request.POST.get('order') is not None:
                filter_variables += f'order={request.POST.get("order")}&'
            for studio in request.POST.getlist('studio'):
                filter_variables += f'studio={studio}&'
            if request.POST.get('name') is not None:
                filter_variables += f'name={request.POST.get("name")}&'
        else:
            objects = self.model.objects.all()
            end_page = paginate_count(self.max_objects, objects)
            filter_variables = ''

        if 1 > page or page > end_page:
            page = 1

        html = render_to_string(
                request=request,
                template_name="games/list.html",
                context={
                    'games': paginate(self.max_objects, objects, page), 
                    'paginate_range': paginate_pages_range(page, 2, end_page),
                    'end_page': end_page,
                    'page': page,
                    'filter_form': GameSortForm(request.POST),
                    'filter_variables': filter_variables,
                    },
                )
        return JsonResponse({'html': html}, status=200)
        

class GamesDetailView(DetailView):
    model = Game
    template_name = 'games/detail.html'
    context_object_name = 'game'