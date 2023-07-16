from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('book', views.add),
    path('book/create', views.addingBook),
    path('book/<int:book_id>', views.viewBook),
    path('review/create', views.addingReview),
    path('review/remove/<int:review_id>', views.removeReview),
]