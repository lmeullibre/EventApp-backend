
from database.models import Event
from  api.events.logic import add_event
import json
import pytest

def test_model_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """

    new_event = Event("event1", "Description","1996-11-14T18:21:35.433Z", "1996-11-14T18:21:35.433Z", 12345, "1996-11-14T18:21:35.433Z", "1996-11-14T18:21:35.433Z", "barcelona",1)
    assert new_event.name == "event1"
    assert new_event.description == "Description"
    assert new_event.funding_start_date == "1996-11-14T18:21:35.433Z"
    assert new_event.funding_end_date == "1996-11-14T18:21:35.433Z"
    assert new_event.goal == 12345
    assert new_event.event_start_date == "1996-11-14T18:21:35.433Z"
    assert new_event.event_end_date == "1996-11-14T18:21:35.433Z"
    assert new_event.location == "barcelona"
    assert new_event.user_creator == 1

def test_add_event_exception1():

    """
    GIVEN a JSON File with the event funding starting in the past
    WHEN trying to create an event
    THEN the system raises an exception which is catched
    """

    x = {
        "name":"Joan",
        "description":"123",
        "funding_start_date":"2010-11-14T18:21:35.433Z",
        "funding_end_date":"2030-11-14T18:21:35.433Z",
        "goal":"1234",
        "event_start_date":"2040-11-14T18:21:35.433Z",
        "telephone":"612123123",
        "event_end_date":"2050-11-14T18:21:35.433Z",
        "location":"barcelona",
        "user_creator":1
    }
    y = json.dumps(x)
    z = json.loads(y)
    with pytest.raises(Exception) as e:
        assert add_event(z)
    assert str(e.value) == "The event funding date can not start in the past"


def test_add_event_exception2():

    """
    GIVEN a JSON File with the event funding ending at the past
    WHEN trying to create an event
    THEN the system raises an exception which is catched
    """

    x = {
        "name":"Joan",
        "description":"description",
        "funding_start_date":"2030-11-14T18:21:35.433Z",
        "funding_end_date":"2015-11-14T18:21:35.433Z",
        "goal":"1234",
        "event_start_date":"2040-11-14T18:21:35.433Z",
        "telephone":"612123123",
        "event_end_date":"2050-11-14T18:21:35.433Z",
        "location":"barcelona",
        "user_creator":1
    }
    y = json.dumps(x)
    z = json.loads(y)
    with pytest.raises(Exception) as e:
        assert add_event(z)
    assert str(e.value) == "The event funding date can not end in the past"

def test_add_event_exception3():

    """
    GIVEN a JSON File with the start funding date being after end funding date
    WHEN trying to create an event
    THEN the system raises an exception which is catched
    """

    x = {
        "name":"Joan",
        "description":"description",
        "funding_start_date":"2030-11-14T18:21:35.433Z",
        "funding_end_date":"2021-11-14T18:21:35.433Z",
        "goal":40,
        "event_start_date":"2040-11-14T18:21:35.433Z",
        "telephone":"612123123",
        "event_end_date":"2050-11-14T18:21:35.433Z",
        "location":"barcelona",
        "user_creator":1
    }
    y = json.dumps(x)
    z = json.loads(y)
    with pytest.raises(Exception) as e:
        assert add_event(z)
    assert str(e.value) == "Start funding date  is after end funding date"

def test_add_event_exception4():

    """
    GIVEN a JSON File with the event starting in the past
    WHEN trying to create an event
    THEN the system raises an exception which is catched
    """

    x = {
        "name":"Joan",
        "description":"description",
        "funding_start_date":"2022-11-14T18:21:35.433Z",
        "funding_end_date":"2023-11-14T18:21:35.433Z",
        "goal":40,
        "event_start_date":"2010-11-14T18:21:35.433Z",
        "telephone":"612123123",
        "event_end_date":"2050-11-14T18:21:35.433Z",
        "location":"barcelona",
        "user_creator":1
    }
    y = json.dumps(x)
    z = json.loads(y)
    with pytest.raises(Exception) as e:
        assert add_event(z)
    assert str(e.value) == "The event can not start in the past"


def test_add_event_exception5():

    """
    GIVEN a JSON File with the event ending in the past
    WHEN trying to create an event
    THEN the system raises an exception which is catched
    """

    x = {
        "name":"Joan",
        "description":"description",
        "funding_start_date":"2022-11-14T18:21:35.433Z",
        "funding_end_date":"2023-11-14T18:21:35.433Z",
        "goal":40,
        "event_start_date":"2025-11-14T18:21:35.433Z",
        "telephone":"612123123",
        "event_end_date":"2010-11-14T18:21:35.433Z",
        "location":"barcelona",
        "user_creator":1
    }
    y = json.dumps(x)
    z = json.loads(y)
    with pytest.raises(Exception) as e:
        assert add_event(z)
    assert str(e.value) == "The event can not end in the past"

def test_add_event_exception6():

    """
    GIVEN a JSON File with the event starting date being after the ending date
    WHEN trying to create an event
    THEN the system raises an exception which is catched
    """

    x = {
        "name":"Joan",
        "description":"description",
        "funding_start_date":"2022-11-14T18:21:35.433Z",
        "funding_end_date":"2023-11-14T18:21:35.433Z",
        "goal":40,
        "event_start_date":"2025-11-14T18:21:35.433Z",
        "telephone":"612123123",
        "event_end_date":"2024-11-14T18:21:35.433Z",
        "location":"barcelona",
        "user_creator":1
    }
    y = json.dumps(x)
    z = json.loads(y)
    with pytest.raises(Exception) as e:
        assert add_event(z)
    assert str(e.value) == "Start date is after end date"

