from django.urls import path
from .views import UserView, LoginView

urlpatterns = [
    path('user/', UserView.as_view(), name="user"),
    path('user/<int:user_id>/', UserView.as_view(), name="user_details"),
    path('login/', LoginView.as_view(), name="login")
]

# Using Restframework Generics: ListAPIView, RetrieveAPIView
# from .views import UserListView, UserDetailView

# urlpatterns = [
#     path('user/', UserListView.as_view(), name="user"),
#     path('user/<int:id>', UserDetailView.as_view(), name="user_details")
# ]