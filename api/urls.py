from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import knowledge_area, user, entry, image, definition, question, entry_access_history

entry_urls = [
    path('entry', entry.EntryView.as_view(), name='entry-list'),
    path('entry/<int:pk>', entry.SingleEntryView.as_view(), name='entry-detail'),
    path('entry/<int:pk>/validate', entry.validate, name='entry-validation')
]

entry_history_urls = [
    path('history', entry_access_history.EntryAccessHistoryView.as_view(), name='entry-history'),
    path('history/most_accessed', entry_access_history.get_most_accessed_entries, name='entry-history-most-accessed'),
]

image_urls = [
    path('image', image.ImageView.as_view(), name='entry-image-list'),
    path('image/<int:pk>', image.SingleImageView.as_view(), name='entry-image-detail'),
    path('image/<int:pk>/blob_file', image.get_image_blob_file, name='entry-image-blob-file'),
]

definition_urls = [
    path('definition', definition.DefinitionView.as_view(), name='definition-list'),
    path('definition/<int:pk>', definition.SingleDefinitionView.as_view(), name='definition-detail'),
]

question_urls = [
    path('question', question.QuestionView.as_view(), name='question-list'),
    path('question/<int:pk>', question.SingleQuestionView.as_view(), name='question-detail'),
]

knowledge_area_urls = [
    path('knowledge_area', knowledge_area.KnowledgeAreaView.as_view(), name='knowledge-area-list'),
    path('knowledge_area/<int:pk>', knowledge_area.SingleKnowledgeAreaView.as_view(), name='knowledge-area-detail'),
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
        + entry_history_urls
        + question_urls
        + image_urls
        + knowledge_area_urls
        + definition_urls
)
