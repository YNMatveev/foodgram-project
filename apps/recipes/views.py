import operator
from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Q
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from recipes.forms import RecipeForm
from recipes.models import Favorite, Recipe, Subscribe

# Create your views here.
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
        tags_filter = self._get_filter()

        if change_tag:
            if change_tag in tags_filter:
                tags_filter.remove(change_tag)
            else:
                tags_filter.append(change_tag)

        self.request.session['filter'] = tags_filter

        return tags_filter

    def _get_filter(self):
        return self.request.session.get('filter', default=self.DEFAULT_FILTER)

    def get_queryset(self):

        self.tags_filter = self._update_filter()
        self.condition = self._get_conditions(self.tags_filter)

        return None

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
        super().get_queryset()
        queryset = Recipe.objects.filter(self.condition).annotate(
            is_favorite=Exists(Favorite.objects.filter(
                chooser_id=self.request.user.id,
                recipe_id=OuterRef('pk'))
            )
        )
        return queryset


class ProfileListView(ListViewWithFilter):

    def get_queryset(self):
        super().get_queryset()
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
        super().get_queryset()
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
                    subscriber_id=self.request.user.id,
                    author_id=OuterRef('pk'))
                )
        )


class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'

    def form_valid(self, form):
        if form.instance.author_id == self.request.user.id:
            return super().form_valid(form)
        form.add_error(None, ValidationError(
            {"author": "Только автор может редактировать рецепт"}))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


class RecipeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:index')
    template_name = 'recipe_confirm_delete.html'

    def get_object(self, queryset=None):
        recipe = super(RecipeDeleteView, self).get_object()
        if not recipe.author == self.request.user:
            ValidationError('Только автор может удалить рецепт')
        return recipe
