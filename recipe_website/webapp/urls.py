from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    RecipeListView,
    UserRecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    RecipeByCategoryView,
    AboutView
)
from . import views

urlpatterns = [
    path('', RecipeListView.as_view(), name='webapp-home'),
    path('user/<str:username>', UserRecipeListView.as_view(), name='user-recipes'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipes/category/<int:category_id>/', RecipeByCategoryView.as_view(), name='recipes-by-category'),
    path('about/', AboutView.as_view(), name='webapp-about'),
]

# включаем возможность обработки картинок в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
