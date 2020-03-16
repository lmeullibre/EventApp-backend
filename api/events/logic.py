from database import db
from database.models import Event, Tag, Report, User, Funded, VotedTest
from datetime import datetime
import pytz

utc = pytz.UTC


def add_event(data, user_creator):
    name = data.get('name')
    description = data.get('description')
    funding_start_date = datetime.strptime(data.get('funding_start_date'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=utc)
    funding_end_date = datetime.strptime(data.get('funding_end_date'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=utc)
    goal = data.get('goal')
    event_start_date = datetime.strptime(data.get('event_start_date'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=utc)
    event_end_date = datetime.strptime(data.get('event_end_date'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=utc)
    location = data.get('location')
    latitude = data.get('lat')
    if latitude is None:
        latitude = 0.000
    longitude = data.get('long')
    if longitude is None:
        longitude = 0.00
    tags = data.get('tags')
    photo = data.get('photo')

    if (funding_start_date < utc.localize(datetime.now())):
        raise Exception("The event funding date can not start in the past")
    if (funding_end_date < utc.localize(datetime.now())):
        raise Exception("The event funding date can not end in the past")
    if (funding_start_date > funding_end_date):
        raise Exception("Start funding date  is after end funding date")
    if (event_start_date < utc.localize(datetime.now())):
        raise Exception("The event can not start in the past")
    if (event_end_date < utc.localize(datetime.now())):
        raise Exception("The event can not end in the past")
    if (event_start_date > event_end_date):
        raise Exception("Start date is after end date")

    new_event = Event(name, description, funding_start_date, funding_end_date, goal, event_start_date, event_end_date,
                      location, user_creator, latitude, longitude, photo)

    for tag in tags:
        new_tag = Tag(tag)
        new_event.tags.append(new_tag)

    db.session.add(new_event)
    db.session.commit()

    return new_event.id


def update_event(id, data):
    event = Event.query.get(id)
    event.description = data.get('description')
    event.location = data.get('location')
    event.photo = data.get('photo')

    funding_end_date = datetime.strptime(data.get('funding_end_date'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=utc)
    event_start_date = datetime.strptime(data.get('event_start_date'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=utc)
    event_end_date = datetime.strptime(data.get('event_end_date'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=utc)

    event.lat = data.get('lat')
    event.long = data.get('long')

    if (event_start_date > event_end_date):
        raise Exception("Start date is after end date")

    event.event_end_date = event_end_date
    event.event_start_date = event_start_date
    event.funding_end_date = funding_end_date

    db.session.add(event)
    db.session.commit()


def delete_event(id):
    event = Event.query.get(id)
    db.session.delete(event)
    db.session.commit()
    return event


def add_report(data, user_id):
    event_id = data.get('event_id')
    content = data.get('content')

    new_report = Report(user_id, event_id, content)

    db.session.add(new_report)
    db.session.commit()

    return new_report.id


def delete_report(id):
    report = Report.query.get(id)
    db.session.delete(report)
    db.session.commit()
    return report


def watch_event(id, data, user_id):
    event = Event.query.get(id)
    user = User.query.get(user_id)

    if user in event.watchers:
        event.watchers.remove(user)
    else:
        event.watchers.append(user)

    db.session.commit()


def fund_event(id, data, user_id):
    event = Event.query.get(id)
    user = User.query.get(user_id)

    test = Funded(fund_amount=data.get('fund_amount'))

    test.backed = user
    test.backers = event

    event.backers.append(test)
    db.session.commit()


def vote_event(id, data, user_id):

    event = Event.query.get(id)
    user = User.query.get(user_id)

    test = VotedTest(stars=data.get('stars'))

    test.voted = user
    test.votes = event

    event.votes.append(test)
    db.session.commit()


def get_info_events(events):

    if type(events) != list:
        user = User.query.filter(User.id == events.user_creator).one()
        events.__dict__['user_creator_name'] = user.name
        return events

    result = []
    for event in events:
        user = User.query.filter(User.id == event.user_creator).one()
        event.__dict__['user_creator_name'] = user.name
        result.append(event)

    return result
