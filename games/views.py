
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def paginate(paginator, page):
    try:
        objects = paginator.page(page)
        return(objects)
    except EmptyPage:
        objects = paginator.page(1)
        return(objects)


def paginate_count(paginator):
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
            ).order_by(self.request.POST.get('order', 'name')).select_related('studio')
        return objects
    

    def get(self, request, *args, **kwargs):
        page = 1
        objects = self.model.objects.order_by('name').select_related('studio')
        paginator = Paginator(objects, self.max_objects)
        end_page = paginate_count(paginator)

        return render(
            request=request,
            template_name="games/list.html",
            context={
                'games': paginate(paginator, page), 
                'paginate_range': paginate_pages_range(page, 2, end_page),
                'end_page': end_page,
                'page': 1,
                'filter_form': GameSortForm(),
                },
            )


    def post(self, request, *args, **kwargs):
        if GameSortForm(request.POST).is_valid():
            try:
                page = int(request.GET.get('page', 1))
            except ValueError:
                page = 1

            if GameSortForm(request.POST).is_valid():
                objects = self.get_queryset()
                paginator = Paginator(objects, self.max_objects)
                end_page = paginate_count(paginator)
                filter_variables = ''
                if request.POST.get('order') is not None:
                    filter_variables += f'order={request.POST.get("order")}&'
                for studio in request.POST.getlist('studio'):
                    filter_variables += f'studio={studio}&'
                if request.POST.get('name') is not None:
                    filter_variables += f'name={request.POST.get("name")}&'
            else:
                objects = self.model.objects.all().select_related('studio')
                paginator = Paginator(objects, self.max_objects)
                end_page = paginate_count(paginator)
                filter_variables = ''

            if 1 > page or page > end_page:
                page = 1

            html = render_to_string(
                    request=request,
                    template_name="games/list-template.html",
                    context={
                        'games': paginate(paginator, page), 
                        'paginate_range': paginate_pages_range(page, 2, end_page),
                        'end_page': end_page,
                        'page': page,
                        },
                    )
            return JsonResponse({'html': html}, status=200)
        else:
            page = 1
            objects = self.model.objects.order_by('name').select_related('studio')
            paginator = Paginator(objects, self.max_objects)
            end_page = paginate_count(paginator)

            html = render_to_string(
                request=request,
                template_name="games/list.html",
                context={
                    'games': paginate(paginator, page), 
                    'paginate_range': paginate_pages_range(page, 2, end_page),
                    'end_page': end_page,
                    'page': 1,
                    'filter_form': GameSortForm(request.POST),
                    },
                )
            return JsonResponse({'html_error': html}, status=203)
        

class GamesDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = 'games/detail.html'
    context_object_name = 'game'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm()
        game = self.object
        context['comments'] = Comment.objects.filter(game=game).order_by('-date').select_related('user', 'game')
        context['user_grade'] = game.get_grade_by_user(self.request.user)
        context['grade_form'] = GradeForm()
        try:
            favorite = FavoriteItem.objects.get(user=self.request.user, game=game)
            context['is_favorite'] = True
        except FavoriteItem.DoesNotExist:
            context['is_favorite'] = False
        return context


def get_comments(request, game, form):
    html = ''
    comments = Comment.objects.filter(game=game).order_by('-date').select_related('user', 'game')
    for comment_flex in comments:
        html += render_to_string(request=request, template_name='games/comment.html', context={'comment': comment_flex, 'comment_form': form})
    return html


class CommentCreateView(LoginRequiredMixin, View):
    model = Comment
    form_class = CommentCreateForm

    def post(self, request, *args, **kwargs):
        if self.form_class(request.POST).is_valid():
            game = Game.objects.get(pk = kwargs['pk'])
            user = request.user
            comment = self.model.objects.create(game=game, user=user, text=request.POST.get('text', ''))
            return JsonResponse({'html': get_comments(request, game, self.form_class())}, status=200)
        else:
            game = Game.objects.get(pk=kwargs['pk'])
            html = render_to_string(
                request=request, 
                template_name='games/comment.html', 
                context={
                    'comment_form': CommentCreateForm(request.POST),
                    'comments': Comment.objects.filter(game=game).order_by('date'),
                    'game': game,
                    })
            return JsonResponse({'html_error': html}, status=203)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Comment
    form_class = CommentCreateForm


    def get(self, request, *args, **kwargs):
        try:
            comment = self.model.objects.get(pk=self.kwargs['pk'])
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Object does not exist'}, status=203)

        game = comment.game
        comment.delete()
        return JsonResponse({'html': get_comments(request, game, self.form_class())}, status=200)


    def test_func(self):
        comment_user = self.model.objects.get(pk=self.kwargs['pk']).user
        user = self.request.user
        return comment_user == user


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Comment
    form_class = CommentCreateForm


    def post(self, request, *args, **kwargs):
        try:
            comment = self.model.objects.get(pk=self.kwargs['pk'])
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Object does not exist'}, status=203)

        game = comment.game

        if self.form_class(request.POST).is_valid():
            comment.text = request.POST.get('text', 'ERROR')
            comment.save()
            return JsonResponse({'html': get_comments(request, game, self.form_class())}, status=200)
        else:
            html = render_to_string(
                request=request, 
                template_name='games/comment.html', 
                context={
                    'comment_form': CommentCreateForm(request.POST),
                    'comments': Comment.objects.filter(game=game).order_by('date'),
                    'game': game,
                    })
            return JsonResponse({'html_error': html}, status=203)


    def test_func(self):
        comment_user = self.model.objects.get(pk=self.kwargs['pk']).user
        user = self.request.user
        return comment_user == user


class GradeView(LoginRequiredMixin, View):
    form_class = GradeForm

    def post(self, request, *args, **kwargs):
        if self.form_class(request.POST).is_valid():
            try:
                game = Game.objects.get(pk=kwargs['pk'])
            except Game.DoesNotExist:
                return JsonResponse({'error': 'Game does not exist'}, status=203)

            grade = Grade.objects.get_or_create(user=request.user, game=game)[0]
            grade.number = request.POST.get('number', 1)
            grade.save()
            html = render_to_string(
                request=request, 
                template_name='games/game.html', 
                context={
                    'game':game, 
                    'detail':True, 
                    'user_grade': game.get_grade_by_user(self.request.user), 
                    'grade_form': GradeForm()})
            return JsonResponse({'html': html}, status=200)
        else:
            return JsonResponse({'form_error': 'Number is not valid'}, status=203)


class FavoriteItemsListView(LoginRequiredMixin, ListView):
    template_name = 'games/favorites.html'
    model = FavoriteItem
    context_object_name = 'favorite_items'


    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user).select_related('game')
    

class FavoriteItemView(LoginRequiredMixin, View):
    model = FavoriteItem


    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            game = Game.objects.get(pk = kwargs['pk'])
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game does not exist'}, status=203)

        try:
            favorite = self.model.objects.get(user=user, game=game)
            favorite.delete()
            return JsonResponse({'success': 'Delete'}, status=200)
        except self.model.DoesNotExist:
            favorite = self.model.objects.create(user=user, game=game)
            return JsonResponse({'success': 'Create'}, status=200)
