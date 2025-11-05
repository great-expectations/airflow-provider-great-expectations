from great_expectations_provider.common.constants import VERSION


def get_provider_info():
    return {
        "package-name": "airflow-provider-great-expectations",
        "name": "Great Expectations Provider",
        "description": "An Apache Airflow provider for Great Expectations.",
        "versions": [VERSION],
        "hooks": [
            {
                "integration-name": "GX Cloud",
                "python-modules": ["great_expectations_provider.hooks.gx_cloud"],
            }
        ],
        "connection-types": [
            {
                "connection-type": "gx_cloud",
                "hook-class-name": "great_expectations_provider.hooks.gx_cloud.GXCloudHook",
                "hook-name": "Great Expectations Cloud",
                "ui_field_behaviour": {
                    "hidden_fields": ["port", "host", "extra"],
                    "relabeling": {
                        "login": "GX Cloud Organization ID",
                        "password": "GX Cloud Access Token",
                        "schema": "GX Cloud Workspace ID",
                    },
                },
            }
        ],
    }
