from gglobal.badges.utils import MetaBadge
from gglobal.crm.models import ExecutantProfile
from gglobal.badges.utils import register as register_badge


class VerificationUser(MetaBadge):
    id = "verification_user"
    model = ExecutantProfile
    one_time_only = True

    title = "Верифицированный пользователь"
    description = "Пройдена проверка личных данных"
    level = "1"

    progress_start = 0
    progress_finish = 2
    
    def get_user(self, instance):
    	return instance.user

    def get_progress(self, user):
    	has_number_passport = 1 if user.executantprofile.number_passport else 0
    	has_serial_passport = 1 if user.executantprofile.serial_passport else 0
    	return has_number_passport + has_serial_passport
    
    def check_number_passport(self, instance):
        return instance.user.executantprofile.number_passport

    def check_serial_passport(self, instance):
        return instance.user.executantprofile.serial_passport

register_badge(VerificationUser)
