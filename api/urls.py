from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import knowledge_area, user, entry, image, definition, question

entry_urls = [
    path('entry/', entry.EntryView, name='entry-list'),
    path('entry/<int:pk>', entry.SingleEntryView, name='entry-detail'),
]

image_urls = [
    path('image/', image.ImageView, name='entry-image-list'),
    path('image/<int:pk>', image.ImageView, name='entry-image-detail'),
    path('image/<int:pk>/blob_file', image.get_image_blob_file.as_view(), name='entry-image-blob-file'),
]

definition_urls = [
    path('definition/', definition.DefinitionView, name='definition-list'),
    path('definition/<int:pk>', definition.SingleDefinitionView, name='definition-detail'),
]

question_urls = [
    path('question/', question.DefinitionView, name='question-list'),
    path('question/<int:pk>', question.SingleDefinitionView, name='question-detail'),
]

knowledge_area_urls = [
    path('knowledge_area', knowledge_area.KnowledgeAreaView, name='knowledge-area-list'),
    path('knowledge_area/<int:pk>', knowledge_area.SingleKnowledgeAreaView, name='knowledge-area-detail'),
]

user_urls = [
    path('hello-world', user.hello_world),
    path('users', user.UserView.as_view()),
    path('users/turn-admin', user.turn_admin_view),
]

urlpatterns = (
        [
            path('token', TokenObtainPairView.as_view()),
            path('token/refresh', TokenRefreshView.as_view()),
        ]
        + user_urls
        + entry_urls
        + image_urls
        + knowledge_area_urls
        + definition_urls
)
