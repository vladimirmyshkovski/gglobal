from gglobal.badges.utils import MetaBadge
from gglobal.badges.utils import register as register_badge
from gglobal.users.models import User


class AuthorizationUser(MetaBadge):
    id = "authorization_user"
    model = User
    one_time_only = True

    title = "Авторизованный пользователь"
    description = "Заполнены имя и фамилия"
    level = "1"

    progress_start = 0
    progress_finish = 2
    
    def get_user(self, instance):
        return instance

    def get_progress(self, user):
        has_first_name = 1 if user.first_name else 0
        has_last_name = 1 if user.first_name else 0
        return has_first_name + has_last_name
    
    def check_first_name(self, instance):
        return instance.first_name

    def check_last_name(self, instance):
        return instance.last_name
                
                
register_badge(AuthorizationUser)
