from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class SchemaInfo:
    rows: int
    columns: int

    numeric_columns: list[str]
    categorical_columns: list[str]
    datetime_columns: list[str]

    target_column: Optional[str]

    missing_summary: dict[str, int]


class SchemaInfer:

    def infer(
        self,
        dataframe: pd.DataFrame,
        target_column: Optional[str] = None,
    ) -> SchemaInfo:

        numeric_columns = dataframe.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = dataframe.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        datetime_columns = dataframe.select_dtypes(
            include=["datetime"]
        ).columns.tolist()

        missing_summary = (
            dataframe
            .isnull()
            .sum()
            .to_dict()
        )

        return SchemaInfo(
            rows=len(dataframe),
            columns=len(dataframe.columns),

            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
            datetime_columns=datetime_columns,

            target_column=target_column,

            missing_summary=missing_summary,
        )