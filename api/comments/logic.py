from database import db
from database.models import Comment, User


def add_comment(data, user_id):
    event_id = data.get('event_id')
    text = data.get('text')
    if not text:
        raise Exception("You can't post an empty comment")
    new_comment = Comment(user_id, event_id, text)
    db.session.add(new_comment)
    db.session.commit()
    return new_comment


def delete_comment(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return comment


def get_info_comments(comments):

    if type(comments) != list:
        user = User.query.filter(User.id == comments.user_id).one()
        comments.__dict__['user_name'] = user.name
        comments.__dict__['user_photo'] = user.photo
        return comments

    result = []
    for comment in comments:
        user = User.query.filter(User.id == comment.user_id).one()
        comment.__dict__['user_name'] = user.name
        comment.__dict__['user_photo'] = user.photo
        result.append(comment)

    return result
