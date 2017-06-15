from django.core.urlresolvers import reverse

def appeal_river_button(obj, proceeding):
    return """
        <input
            type="button"
            style="margin: 2px;"
            value="%s"
            onclick="location.href=\'%s\'"
            />

    """% (proceeding.meta.transition,
          reverse('crm:proceed_appeal', kwargs={'appeal_id': obj.pk, 'next_state_id': proceeding.meta.transition.destination_state.pk })
          )

def appeal_river_field_button(obj, proceeding):
    return """
        <input
            type="button"
            style="margin: 2px;"
            value="%s"
            onclick="location.href=\'%s\'"
            />

    """% (proceeding.meta.transition,
          reverse('crm:proceed_appeal_single', kwargs={'appeal_id': obj.pk, 'next_state_id': proceeding.meta.transition.destination_state.pk })
          )
    
def assignment_river_button(obj, proceeding):
    return """
        <input
            type="button"
            style="margin: 2px;"
            value="%s"
            onclick="location.href=\'%s\'"
            />

    """% (proceeding.meta.transition,
          reverse('crm:proceed_assignment', kwargs={'assignment_id': obj.pk, 'next_state_id': proceeding.meta.transition.destination_state.pk })
          )

def assignment_river_field_button(obj, proceeding):
    return """
        <input
            type="button"
            style="margin: 2px;"
            value="%s"
            onclick="location.href=\'%s\'"
            />

    """% (proceeding.meta.transition,
          reverse('crm:proceed_assignment_single', kwargs={'assignment_id': obj.pk, 'next_state_id': proceeding.meta.transition.destination_state.pk })
          )


def assignment_passing_button(obj, user_id):
    return """
        <input
            type="button"
            style="margin: 2px;"
            value="Отказаться"
            onclick="location.href=\'%s\'"
            />

    """% (
        reverse('crm:passing_assign', kwargs={'assignment_id': obj.pk, 'user_id': user_id })
        )

def telegram_auth_button(obj, user_id):
    return """
        <input
            type="button"
            style="margin: 2px;"
            value="Авторизоваться через Telegram"
            onclick="location.href=\'%s\'"
            />

    """% (
        reverse('crm:telegram_auth', kwargs={'user_id': user_id })
        )