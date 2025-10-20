import pandas as pd
from pandera.errors import SchemaError, SchemaErrors


class FakeBackend:
    def failure_cases_metadata(self, schema_name, schema_errors):
        failure_cases = pd.DataFrame(
            [
                {
                    "index": 0,
                    "column": "produto",
                    "failure_case": None,
                    "check": "not_nullable",
                },
                {
                    "index": 1,
                    "column": "quantidade",
                    "failure_case": "abc",
                    "check": "type",
                },
                {
                    "index": 2,
                    "column": "preco_unitario",
                    "failure_case": "",
                    "check": "nullable",
                },
                {
                    "index": 3,
                    "column": "data",
                    "failure_case": "1",
                    "check": "nullable",
                },
            ]
        )
        return type(
            "Meta",
            (),
            {
                "failure_cases": failure_cases,
                "message": {"errors": "Mocked pandera error"},
                "error_counts": {"total": 4},
            },
        )


class FakeSchema:
    name = "fake_schema"

    @staticmethod
    def get_backend(data):
        return FakeBackend()


class FakePanderaModel:
    @staticmethod
    def to_schema():
        class FakeSchemaColumns:
            columns = {
                "produto": None,
                "quantidade": None,
                "preco_unitario": None,
                "data": None,
            }

        return FakeSchemaColumns()

    @staticmethod
    def validate(df, lazy=True):
        fake_error_list = [
            SchemaError(
                schema=None, data=None, message="mock error", failure_cases=None
            )
        ]

        error = SchemaErrors(
            schema=FakeSchema(), schema_errors=fake_error_list, data=df
        )

        raise error
