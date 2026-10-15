# -*- coding: utf-8 -*-
import argparse
import sys

from CalcQuartile import CalcQuartile
from CalcRating import CalcRating
from CalcRating import RatingType
from DataReader import DataReader
from TextDataReader import TextDataReader
from YamlDataReader import YamlDataReader


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def get_reader(path: str) -> DataReader:
    if path.lower().endswith((".yaml", ".yml")):
        return YamlDataReader()
    return TextDataReader()


def print_second_quartile(rating: RatingType) -> None:
    calc_quartile = CalcQuartile(rating)
    students = calc_quartile.calc_students_in_second_quartile()
    print("Second quartile bounds: ",
          calc_quartile.lower_bound, calc_quartile.upper_bound)
    if students:
        print("Students in second quartile: ", students)
    else:
        print("There are no students in second quartile")


def main():
    path = get_path_from_arguments(sys.argv[1:])

    students = get_reader(path).read(path)
    print("Students: ", students)

    rating = CalcRating(students).calc()
    print("Rating: ", rating)

    print_second_quartile(rating)


if __name__ == "__main__":
    main()
