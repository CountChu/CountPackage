#
# FILENAME.
#       cnt_ft.py - Count File Table Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides functions of file table, refactored as a class.
#
# NOTICE.
#       Author: visualge@gmail.com (Count Chu)
#       Created on 2025/1/1
#       Updated on 2025/7/5
#

import pandas as pd
import sys
import arrow
from typing import Any, Dict, Union, List
from pathlib import Path
from Count import cnt_util

br = breakpoint


class Artifact:
    def __init__(self, db_y: Dict[str, Any], date):
        self.home = db_y["__dir__"]
        self.date = date

        # artifactGroupDict[groupId] = artifactGroup
        # artifactGroup = {home, artifacts, artifactDict}
        # artifactDict[artifactId] = artifact

        self.artifactGroupDict = db_y["artifact"]

        for _, artifactGroup in self.artifactGroupDict.items():
            artifactGroup["artifactDict"] = cnt_util.build_d(artifactGroup["artifacts"])

    def get_path(
        self, group_id: str, artifact_id: str, postfix_ls: List[str] | None = None
    ) -> Path:
        artifactGroup = self.artifactGroupDict[group_id]
        artifact = artifactGroup["artifactDict"][artifact_id]
        name = artifact.get("path")

        if group_id == "log":
            if "time" in artifact and artifact["time"]:
                time_str = arrow.now().format("HH-mm")
                name = f"{self.date}-{time_str}-{name}"
            else:
                name = f"{self.date}-{name}"

        if postfix_ls is not None:
            for postfix in postfix_ls:
                name = f"{name}-{postfix}"

        if "ext" in artifact:
            name = f"{name}.{artifact['ext']}"

        out = Path(self.home) / artifactGroup["home"] / name
        return out


class FileTable:
    def __init__(self, home: str, path: str, table: Dict[str, Any]):
        self.id = table["id"]
        self.path = table["path"]
        self.columns = table["columns"]
        self.dirs = table.get("dirs", [])
        self.ext = table["ext"]

        self.realPath: Path = Path(home) / path / self.path
        self.loaded = False

    def load(self):
        assert self.realPath.exists(), self.realPath

        self.files: pd.DataFrame = pd.DataFrame()

        assert self.ext in [
            "xls",
            "json",
            "csv",
            "txt",
            "numbers",
            "yaml",
            "xml",
            "html",
        ], self.ext
        self.file_p_ls = [
            x for x in self.realPath.rglob("*") if x.suffix == f".{self.ext}"
        ]

        self._build_file_table()
        self.loaded = True

    def _build_file_table(self):
        path_ls = [str(file_p.relative_to(self.realPath)) for file_p in self.file_p_ls]
        df = pd.DataFrame({"path": path_ls})

        ls_d: Dict[str, Any] = {column: [] for column in self.columns}
        for file_p in self.file_p_ls:
            values = file_p.stem.split("#")
            if len(values) != len(self.columns):
                print("Error in file table building:")
                print(f"    {len(values)=}")
                print(f"    {len(self.columns)=}")
                print(f"    {values=}")
                print(f"    {self.columns=}")
                print(f"    {file_p=}")
                sys.exit(0)

            for column, value in zip(self.columns, values):
                ls_d[column].append(value)

        for column in self.columns:
            df[column] = ls_d[column]

        self.files: pd.DataFrame = df

    def split_path(self, file_p: Path) -> list[str]:
        values = file_p.stem.split("#")
        assert len(values) == len(self.columns), values
        return values

    def load_df(self) -> pd.DataFrame | None:
        assert self.loaded

        out = None

        for index, row in self.files.iterrows():  # type: ignore
            file_p: Path = self.realPath / row["path"]  # type: ignore
            if self.ext == "csv":
                df: pd.DataFrame = pd.read_csv(file_p)  # type: ignore
            else:
                raise Exception("Unsupported file extension")

            out = df if out is None else pd.concat([out, df])
        return out

    @staticmethod
    def load_json_as_array(json_p_ls: list[Path]) -> list[Dict[str, Any]]:
        out: list[Dict[str, Any]] = []
        for json_p in json_p_ls:
            if json_p.suffix == ".json":
                row = cnt_util.load_json(str(json_p))
                out += row if isinstance(row, list) else [row]
            else:
                raise Exception("Unsupported file extension")
        return out

    def load_json_as_tables(self, json_p_ls: list[Path]) -> list[Dict[str, Any]]:
        out: list[Dict[str, Any]] = []
        for json_p in json_p_ls:
            if json_p.suffix == ".json":
                data = cnt_util.load_json(str(json_p))
                values = self.split_path(json_p)
                table: Dict[str, Any] = {}

                for name, value in zip(self.columns, values):
                    assert name not in ["rows", "row"]
                    table[name] = value

                if type(data) is dict:
                    table["row"] = data
                elif type(data) is list:
                    table["rows"] = data

                out.append(table)
            else:
                raise Exception("Unsupported file extension")
        return out

    def get_rows(
        self, filter: Dict[str, Union[str, list[str]]], last: str | None = None
    ) -> pd.DataFrame:
        assert self.loaded

        df: pd.DataFrame = self.files.copy()

        if last is not None:
            df = df.sort_values(last, ascending=False)  # type: ignore

        f0 = None
        for column, value in filter.items():
            if type(value) is str:
                if f0 is None:
                    f0 = df[column] == value
                else:
                    f0 = f0 & (df[column] == value)
            elif type(value) is list:
                if f0 is None:
                    f0 = df[column].isin(value)  # type: ignore
                else:
                    f0 = f0 & df[column].isin(value)  # type: ignore
            elif value is None:
                continue
            else:
                assert False, f"Unsupported filter value type: {type(value)}"

        if f0 is None:
            rows = df

            if last is not None:
                columns: list[str] = []
                for column in self.columns:
                    if column != last:
                        columns.append(column)
                if columns != []:
                    rows = rows.groupby(columns).first().reset_index()  # type: ignore
                else:
                    last_value = self.get_last_value(last)
                    rows = rows[rows[last] == last_value]  # type: ignore

        else:
            rows: pd.DataFrame = df[f0]

            # if last is assigned, get the last rows.
            # For example:
            #   rows:
            #       [0] 2025-07-09, 0056.TW
            #       [1] 2025-07-09, 0050.TW
            #       [2] 2025-07-08, 0056.TW
            #       [3] 2025-07-08, 0050.TW
            #   Get [0] and [1]

            if last is not None:
                columns: list[str] = []
                for column in self.columns:
                    if column != last:
                        columns.append(column)
                rows = rows.groupby(columns).first().reset_index()  # type: ignore

        return rows

    def get_files(
        self, filter: Dict[str, Union[str, list[str]]], last: str | None = None
    ) -> list[Path]:
        assert self.loaded, "File table is not loaded."

        rows = self.get_rows(filter, last)
        return [self.realPath / row["path"] for _, row in rows.iterrows()]  # type: ignore

    def get_one_file(
        self, filter: Dict[str, Union[str, list[str]]], last: str | None = None
    ) -> Path | None:
        files = self.get_files(filter, last)
        assert len(files) <= 1, files
        if len(files) == 0:
            return None

        file = files[0]

        return file

    def build_file_p(self, columns: Dict[str, Any]) -> Path | None:
        # Check columns

        if len(columns) != len(self.columns):
            print("Column count does not match.")
            return None

        for column in columns.keys():
            assert column in self.columns, column

        # if len(columns) != len(self.columns):
        #    return None

        stem = "".join(
            f"{value}#" for key, value in columns.items() if key in self.columns
        )
        out = self.realPath

        if self.dirs != None:
            for column in self.columns:
                if column in self.dirs:
                    out = out / columns[column]

        return out / f"{stem[:-1]}.{self.ext}"

    def get_last_value(self, column: str) -> Any:
        assert self.loaded

        df: pd.DataFrame = self.files.copy()
        df2 = df.sort_values(column, ascending=False, inplace=False)  # type: ignore

        out: Any = df2.iloc[0][column]  # type: ignore
        return out  # type: ignore


class Database:
    def __init__(self, db_y: Dict[str, Any]):
        self.home = db_y["__dir__"]

        db = db_y["database"]
        self.path = db["path"]

        self.file_d = None
        if "files" in db:
            self.file_d = cnt_util.build_d(db["files"])

        self.table_d = None
        if "tables" in db:
            self.table_d = cnt_util.build_d(db["tables"])

    def get_path(self, file_id: str) -> Path:
        out = Path(self.home) / self.path / self.file_d[file_id]["path"]
        return out

    def build_file_table(self, table_id: str) -> FileTable:
        assert table_id in self.table_d, table_id
        table = self.table_d[table_id]
        ft = FileTable(self.home, self.path, table)
        return ft
