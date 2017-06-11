from gglobal.crm.bot_views import StartCommandView, UnknownCommandView, \
									HelpCommandView

from telegrambot.handlers import command, unknown_command
from telegrambot.bot_views.decorators import login_required

urlpatterns = [command('start', StartCommandView.as_command_view()),
               command('help', HelpCommandView.as_command_view()),
			   unknown_command(UnknownCommandView.as_command_view())]