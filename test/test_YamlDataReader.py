# -*- coding: utf-8 -*-
import os

import pytest

from src.Types import DataType
from src.YamlDataReader import YamlDataReader


class TestYamlDataReader:

    @pytest.fixture()
    def yaml_text(self) -> str:
        return (
            "- Иванов Константин Дмитриевич:\n"
            "    математика: 91\n"
            "    химия: 100\n"
            "- Петров Петр Семенович:\n"
            "    русский язык: 87\n"
            "    литература: 78\n"
        )

    @pytest.fixture()
    def expected_data(self) -> DataType:
        return {
            "Иванов Константин Дмитриевич": [
                ("математика", 91), ("химия", 100)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87), ("литература", 78)
            ]
        }

    @pytest.fixture()
    def make_file(self, tmpdir):
        def creator(content: str, name: str = "my_data.yaml") -> str:
            path = tmpdir.mkdir("yamldir").join(name)
            path.write_text(content, encoding='utf-8')
            return str(path)
        return creator

    def test_init_yaml_data_reader(self) -> None:
        assert YamlDataReader().students == {}

    def test_read(self, make_file, yaml_text: str,
                  expected_data: DataType) -> None:
        students = YamlDataReader().read(make_file(yaml_text))
        assert students == expected_data

    def test_read_string_scores(self, make_file) -> None:
        text = "- Иванов Иван Иванович:\n    математика: '91'\n"
        students = YamlDataReader().read(make_file(text))
        assert students == {"Иванов Иван Иванович": [("математика", 91)]}

    def test_read_same_as_sample_file(self, make_file,
                                      expected_data: DataType) -> None:
        text = (
            "- Иванов Константин Дмитриевич:\n"
            "    математика: 91\n"
            "    химия: 100\n"
            "- Петров Петр Семенович:\n"
            "    русский язык: 87\n"
            "    литература: 78\n"
        )
        assert YamlDataReader().read(make_file(text)) == expected_data

    def test_read_several_students_one_subject(self, make_file) -> None:
        text = ("- Абрамов П. С.:\n    химия: 61\n"
                "- Петров П. П.:\n    химия: 78\n")
        students = YamlDataReader().read(make_file(text))
        assert students == {
            "Абрамов П. С.": [("химия", 61)],
            "Петров П. П.": [("химия", 78)]
        }

    def test_read_restores_previous_state(self, make_file, yaml_text: str,
                                          expected_data: DataType) -> None:
        reader = YamlDataReader()
        reader.students = {"Устаревшая запись": [("математика", 50)]}
        assert reader.read(make_file(yaml_text)) == expected_data

    def test_read_nonexistent_file(self, tmpdir) -> None:
        with pytest.raises(FileNotFoundError):
            YamlDataReader().read(os.path.join(str(tmpdir), "none.yaml"))

    def test_read_empty_file(self, make_file) -> None:
        with pytest.raises(TypeError):
            YamlDataReader().read(make_file("", "empty.yaml"))
