import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('Hello' == 'World') is False

def test_type():
    assert type('this' is str)
    assert type('bla' is not int)

def test_greater_and_less_than():
    assert 3 > 2
    assert 3 < 5

def test_list():
    nim_list = [1, 2, 3]
    any_list = [False, False]
    assert 1 in nim_list
    assert 5 not in nim_list
    assert all(nim_list)
    assert not any(any_list)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'CS', 3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == 'John', 'First name should be John'
    assert default_employee.last_name == 'Doe', 'Last name should be Doe'
    assert default_employee.major == 'CS'
    assert default_employee.years == 3