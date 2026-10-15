# -*- coding: utf-8 -*-
import yaml

from DataReader import DataReader
from Types import DataType


class YamlDataReader(DataReader):

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            documents = yaml.safe_load(file)

        self.students = {}
        for entry in documents:
            for student, subjects in entry.items():
                self.students[student] = [
                    (subj, int(score))
                    for subj, score in subjects.items()
                ]
        return self.students
