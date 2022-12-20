from pathlib import Path

from airflow.hooks import BaseHook

from src.utils.config import Config

PARDIR = Path(__file__).resolve().parent


class MainData(Config):

    def __init__(self):
        self.is_production = "production" == self.cached_get('ENVIRONMENT')
        self.is_test = "test" == self.cached_get('ENVIRONMENT')
        self.use_prod_tables_for_dependencies = (
            "true" == str(
                self.cached_get(
                    "USE_PROD_TABLES_FOR_DEPENDENCIES",
                    default="true"
                    )
                ).lower()
            )

    def sql_templates_path(self):
        return (PARDIR / "sql").as_posix()

    def domain_table(self, domain_name, entity):
        if self.is_production:
            return entity
        else:
            return f"{domain_name}__{entity}"

    def schema(self, schema, is_dependency=None):
        if self.is_production:
            return schema
        elif self.is_test():
            return self.test_schema()
        else:
            return self.development_schema(schema, is_dependency)

    def full_table_name(self, schema, table):
        return f"{self.schema(schema)}.{self.table(schema, table)}"

    def table(self, schema, table, is_dependency=None):
        if self.is_production():
            return table
        else:
            return self.development_table(schema, table, is_dependency)

    def redshift_copy_unload_role_arn(self):
        return self.get_config(
            "REDSHIFT_COPY_UNLOAD_ROLE_ARN",
            default=(
                "arn:aws:iam::"
                "220454698174:"
                "role/redshift-copy-unload-development")
            )

    def development_table(self, schema, table, is_dependency=None):
        if is_dependency and self.use_prod_tables_for_dependencies():
            dev_table = table
        else:
            dev_table = f"{schema}__{table}"

        return dev_table

    def development_schema(self, schema, is_dependency=None):
        if schema is None:
            dev_schema = "dev_analytics"
        elif is_dependency and self.use_prod_tables_for_dependencies():
            dev_schema = schema
        else:
            dev_schema = self.cached_get_config("DEVELOPMENT_SCHEMA")

        return dev_schema

    def s3_warehouse_bucket(self):
        if self.is_production:
            return 'main-data-warehouse'
        else:
            return 'main-data-warehouse-development'

    def reporting_schema(self, schema):
        schema_default = self.cached_get_config('REPORTING_SCHEMA')

        if self.is_production:
            return schema
        elif schema_default:
            return schema_default
        else:
            return self.development_schema(schema)

    def staging_schema(self, schema):
        schema_default = self.cached_get_config('STAGING_SCHEMA')

        if self.is_production:
            return schema
        elif schema_default:
            return schema_default
        else:
            return self.development_schema(schema)
