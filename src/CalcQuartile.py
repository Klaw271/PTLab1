# -*- coding: utf-8 -*-
from statistics import quantiles

from CalcRating import RatingType

Epsilon = 1e-9


class CalcQuartile:
    # Вторая квартиль — интервал [Q1, Q2] распределения рейтингов.

    def __init__(self, rating: RatingType) -> None:
        self.rating: RatingType = rating
        self.lower_bound: float = 0.0
        self.upper_bound: float = 0.0
        self.students: list[str] = []

    def calc_quartile_bounds(self) -> tuple[float, float]:
        scores = sorted(self.rating.values())
        if len(scores) < 2:
            self.lower_bound = scores[0]
            self.upper_bound = scores[0]
        else:
            q1, q2, _ = quantiles(scores, n=4, method="inclusive")
            self.lower_bound = q1
            self.upper_bound = q2
        return self.lower_bound, self.upper_bound

    def calc_students_in_second_quartile(self) -> list[str]:
        self.calc_quartile_bounds()
        self.students = []
        for student, score in self.rating.items():
            low = self.lower_bound - Epsilon
            high = self.upper_bound + Epsilon
            if low <= score <= high:
                self.students.append(student)
        return self.students
