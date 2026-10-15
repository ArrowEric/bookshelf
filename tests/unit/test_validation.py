import pytest
from bookshelf import services
from bookshelf.models import BookCreate
from pydantic import ValidationError


@pytest.mark.parametrize(
    "isbn,expected",
    [
        pytest.param("9780132350884", True, id="valid-13-digit"),
        pytest.param("0132350882", True, id="valid-10-digit"),
        pytest.param("978-0-13-235088-4", True, id="valid-hyphenated"),
        pytest.param("123", False, id="too-short"),
        pytest.param("97801323508841", False, id="too-long"),
        pytest.param("", False, id="empty"),
        pytest.param("978013235088X", False, id="non-numeric"),
        pytest.param("0000000000", True, id="all-zeros"),
    ],
)
def test_validate_isbn(isbn: str, expected: bool):
    assert services.validate_isbn(isbn) == expected


@pytest.mark.parametrize(
    "year,should_raise",
    [
        (1970, False),
        (2020, False),
        (1800, False),
        (2099, True),
        (3000, True),
    ],
)
def test_year_validation(year: int, should_raise: bool):
    if should_raise:
        with pytest.raises(ValidationError):
            BookCreate(
                title="X",
                author="Y",
                isbn="9780135957059",
                year=year,
            )
    else:
        book = BookCreate(
            title="X",
            author="Y",
            isbn="9780135957059",
            year=year,
        )
        assert book.year == year
