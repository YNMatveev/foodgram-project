import operator
from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Q
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from recipes.forms import RecipeForm
from recipes.models import Favorite, Recipe, Subscribe

User = get_user_model()

ITEMS_PER_PAGE = 6


class ListViewWithFilter(generic.ListView):

    def _get_conditions(self, tags):

        if not tags:
            return Q(tags=None)

        conditions = [
            Q(tags__icontains=value) for key, value in self.TAGS.items()
            if key in tags
        ]

        return reduce(operator.or_, conditions)

    def _update_filter(self):
        change_tag = self.request.GET.get('change_filter')
        self.tags_filter = self._get_filter()

        if change_tag:
            if change_tag in self.tags_filter:
                self.tags_filter.remove(change_tag)
            else:
                self.tags_filter.append(change_tag)

        self.request.session['filter'] = self.tags_filter

        return self.tags_filter

    def _get_filter(self):
        return self.request.session.get('filter', default=self.DEFAULT_FILTER)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.tags_filter
        return context

    TAGS = {tag.name.lower(): tag.value for tag in Recipe.Tag}
    DEFAULT_FILTER = list(TAGS.keys())
    RECIPES_PER_PAGE = ITEMS_PER_PAGE

    paginate_by = RECIPES_PER_PAGE
    template_name = 'index.html'
    context_object_name = 'recipes'


class RecipeListView(ListViewWithFilter):
    def get_queryset(self):
        self.tags_filter = self._update_filter()
        self.condition = self._get_conditions(self.tags_filter)
        queryset = Recipe.objects.filter(self.condition).annotate(
            is_favorite=Exists(Favorite.objects.filter(
                chooser_id=self.request.user.id,
                recipe_id=OuterRef('pk'))
            )
        )
        return queryset


class ProfileListView(ListViewWithFilter):

    def get_queryset(self):
        self.tags_filter = self._update_filter()
        self.condition = self._get_conditions(self.tags_filter)
        self.author = get_object_or_404(User, username=self.kwargs['username'])
        self.author.is_subscribe = Subscribe.objects.filter(
            subscriber_id=self.request.user.id,
            author_id=self.author).exists()

        queryset = self.author.recipes.filter(self.condition).annotate(
            is_favorite=Exists(Favorite.objects.filter(
                chooser_id=self.request.user.id,
                recipe_id=OuterRef('pk'))
            )
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class FavoriteListView(LoginRequiredMixin, ListViewWithFilter):

    def get_queryset(self):
        self.tags_filter = self._update_filter()
        self.condition = self._get_conditions(self.tags_filter)
        queryset = Recipe.objects.filter(
            self.condition,
            favorites__chooser__id=self.request.user.id).annotate(
                is_favorite=Exists(Favorite.objects.filter(
                    chooser_id=self.request.user.id,
                    recipe_id=OuterRef('pk'))
                )
        )
        return queryset


class RecipeDetailView(generic.DetailView):

    template_name = 'recipe_details.html'

    def get_queryset(self):
        queryset = Recipe.objects.annotate(
            is_favorite=Exists(Favorite.objects.filter(
                chooser_id=self.request.user.id,
                recipe_id=OuterRef('pk'))
            )
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        is_subscribe = Subscribe.objects.filter(
            subscriber_id=self.request.user.id,
            author=recipe.author).exists()
        context['is_subscribe'] = is_subscribe
        return context


class SubscribeListView(LoginRequiredMixin, generic.ListView):
    paginate_by = ITEMS_PER_PAGE
    template_name = 'subscribes.html'
    context_object_name = 'authors'

    def get_queryset(self):
        return User.objects.filter(
            subscribers__subscriber__id=self.request.user.id).annotate(
                is_subscribe=Exists(Subscribe.objects.filter(
                    subscriber=self.request.user,
                    author_id=OuterRef('pk'))
                )
        )


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


class RecipeEditView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    success_delete_url = reverse_lazy('recipes:index')

    post_url_name = 'new_recipe'
    update_url_name = 'update_recipe'
    delete_url_name = 'delete_recipe'

    delete_template_name = 'recipe_confirm_delete.html'
    form_template_name = 'recipe_form.html'

    def get_url_name(self):
        return self.request.resolver_match.url_name

    def get_template_name(self):
        if self.get_url_name() == self.delete_url_name:
            return self.delete_template_name
        return self.form_template_name

    def get_object(self, queryset=None):
        self.template_name = self.get_template_name()

        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def form_valid(self, form):
        if self.get_url_name() == self.post_url_name:
            form.instance.author_id = self.request.user.id
            return super().form_valid(form)

        if self.request.user.is_owner(form.instance):
            return super().form_valid(form)
        form.add_error(None, ValidationError(
            {"???????????? ?????????? ?????????? ?????????????????????????? ????????????"}))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_url_name() == self.update_url_name:
            context['update'] = True
        return context

    def post(self, request, *args, **kwargs):
        if self.get_url_name() == self.delete_url_name:
            return self.delete(request, *args, **kwargs)
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.is_owner(self.object):
            return HttpResponseRedirect(self.object.get_absolute_url())
        self.object.delete()
        return HttpResponseRedirect(self.success_delete_url)
