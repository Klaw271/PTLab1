# -*- coding: utf-8 -*-
import pytest

from src.CalcQuartile import CalcQuartile
from src.CalcRating import RatingType


class TestCalcQuartile:

    @pytest.fixture()
    def odd_rating(self) -> RatingType:
        return {
            "Иванов Иван Иванович": 82.0,
            "Петров Петр Петрович": 83.66666666666667,
            "Абрамов Петр Сергеевич": 85.66666666666667
        }

    @pytest.fixture()
    def even_rating(self) -> RatingType:
        return {
            "Студент А": 70.0,
            "Студент Б": 80.0,
            "Студент В": 90.0,
            "Студент Г": 100.0
        }

    def test_init_calc_quartile(self, odd_rating: RatingType) -> None:
        calc_quartile = CalcQuartile(odd_rating)
        assert odd_rating == calc_quartile.rating
        assert calc_quartile.students == []
        assert calc_quartile.lower_bound == 0.0

    def test_calc_bounds_three_students(self, odd_rating: RatingType) -> None:
        low, high = CalcQuartile(odd_rating).calc_quartile_bounds()
        assert pytest.approx(low, abs=1e-6) == 82.83333333333334
        assert pytest.approx(high, abs=1e-6) == 83.66666666666667

    def test_calc_bounds_four_students(self, even_rating: RatingType) -> None:
        assert CalcQuartile(even_rating).calc_quartile_bounds() == (77.5, 85.0)

    def test_calc_bounds_single_student(self) -> None:
        assert CalcQuartile({"Один Студент": 77.5}).calc_quartile_bounds() \
            == (77.5, 77.5)

    def test_calc_bounds_empty_rating(self) -> None:
        with pytest.raises(IndexError):
            CalcQuartile({}).calc_quartile_bounds()

    def test_students_three_students(self, odd_rating: RatingType) -> None:
        students = CalcQuartile(odd_rating).calc_students_in_second_quartile()
        assert students == ["Петров Петр Петрович"]

    def test_students_four_students(self, even_rating: RatingType) -> None:
        students = CalcQuartile(even_rating).calc_students_in_second_quartile()
        assert students == ["Студент Б"]

    def test_students_five_students_two_in_quartile(self) -> None:
        rating = {"А": 60.0, "Б": 70.0, "В": 80.0, "Г": 90.0, "Д": 100.0}
        assert CalcQuartile(rating).calc_students_in_second_quartile() == \
            ["Б", "В"]

    def test_students_all_equal(self) -> None:
        rating = {"А": 90.0, "Б": 90.0, "В": 90.0}
        students = CalcQuartile(rating).calc_students_in_second_quartile()
        assert students == ["А", "Б", "В"]

    def test_students_single(self) -> None:
        calc_quartile = CalcQuartile({"Один Студент": 77.5})
        assert calc_quartile.calc_students_in_second_quartile() == \
            ["Один Студент"]

    def test_students_none_in_quartile(self) -> None:
        calc_quartile = CalcQuartile({"А": 70.0, "Б": 90.0})
        assert calc_quartile.calc_students_in_second_quartile() == []
        assert calc_quartile.lower_bound == 75.0

    def test_fields_updated_after_calc(self, odd_rating: RatingType) -> None:
        calc_quartile = CalcQuartile(odd_rating)
        calc_quartile.calc_students_in_second_quartile()
        assert calc_quartile.students == ["Петров Петр Петрович"]
        assert pytest.approx(calc_quartile.upper_bound,
                             abs=1e-6) == 83.66666666666667
