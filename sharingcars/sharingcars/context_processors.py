from django.core.urlresolvers import resolve
from sharingcars import colaborative_recommendations
from common.models import User, Comment
from routes.models import CommentRoute
from announcements.models import CommentAnnouncement

VIEWS_NAMES = {'announcements': ['create-announcement', 'announcement-all', 'announcement-user',
                               'details-announcement', 'edit-announcement', 'stop-announcement-create',
                               'stop-announcement-edit', 'recommendations-announcements'],
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
    if not request.user.is_anonymous() and request.user.username != 'admin':
        prefs = {}
        comments = Comment.objects.all()
        comments_routes = CommentRoute.objects.all()
        comments_announcements = CommentAnnouncement.objects.all()
        prefs = evaluations_of_comments(prefs, comments)
        prefs = evaluations_of_comments(prefs, comments_routes)
        prefs = evaluations_of_comments(prefs, comments_announcements)
        for key in prefs:
            for key_1 in prefs[key]:
                prefs[key][key_1] = round(sum(prefs[key][key_1]) / float(len(prefs[key][key_1])), 1)
        top_matches = colaborative_recommendations.topMatches(prefs, request.user.username, 9)
        users = []
        for match in top_matches:
            users.append(User.objects.get(user_account__username=match[1]))
        return {'user_more_evaluated': users}
    else:
        return {'user_more_evaluated': User.objects.all()[:9]}


def evaluations_of_comments(prefs, comments):
    for comment in comments:
        if hasattr(comment, 'referrer'):
            if prefs.get(comment.referrer.user_account.username, None):
                if prefs[comment.referrer.user_account.username].get(comment.evaluated.user_account.username, None):
                    prefs[comment.referrer.user_account.username][comment.evaluated.user_account.username].append(comment.rating)
                else:
                    prefs[comment.referrer.user_account.username][comment.evaluated.user_account.username] = [comment.rating, ]
            else:
                prefs[comment.referrer.user_account.username] = {comment.evaluated.user_account.username: [comment.rating, ]}
        else:
            if hasattr(comment, 'route'):
                username = comment.route.user.user_account.username
            else:
                username = comment.announcement.user.user_account.username
            if prefs.get(comment.user.user_account.username, None):
                if prefs[comment.user.user_account.username].get(username, None):
                    prefs[comment.user.user_account.username][username].append(comment.rating)
                else:
                    prefs[comment.user.user_account.username][username] = [comment.rating, ]
            else:
                prefs[comment.user.user_account.username] = {username: [comment.rating, ]}
    return prefs