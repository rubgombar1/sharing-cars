from django.core.urlresolvers import resolve
from common.models import User

VIEWS_NAMES = {'announcements': ['create-announcement', 'announcement-all', 'announcement-user',
                               'details-announcement', 'edit-announcement', 'stop-announcement-create',
                               'stop-announcement-edit'],
             'routes': ['create-route', 'all-routes', 'user-routes', 'recommendations-routes',
                        'details-route', 'edit-route', 'stop-route-create', 'stop-route-edit'],
             'messages': ['messages-send',  'messages-delete', 'messages-reply', 'messages-mark-not-see',
                          'messages-details', 'messages-see'],
             'applies': ['apply-announcement-user-received', 'apply-announcement-user-performed',
                         'create-apply-announcement', 'remove-apply-announcement', 'resolve-apply-announcement',
                         'apply-route-user-received', 'apply-route-user-performed', 'remove-apply-route',
                         'create-apply-route', 'resolve-apply-route'],
             'contact': ['contact']
             }


def check_menu(request):
    view_name = resolve(request.path_info).url_name
    for key in VIEWS_NAMES:
        if view_name in VIEWS_NAMES[key]:
            return {'active': key}
    return {}


def user_more_evaluated(request):
    return {'user_more_evaluated': User.objects.all()[:9]}