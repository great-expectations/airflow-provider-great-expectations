from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from airflow.exceptions import AirflowException

try:  # airflow 3
    from airflow.sdk import BaseHook
except ImportError:  # airflow 2
    from airflow.hooks.base import BaseHook  # type: ignore[attr-defined,no-redef]


from great_expectations_provider.common.gx_context_actions import load_data_context


class IncompleteGXCloudConfigError(AirflowException):
    """Great Expectations connection configuration is not complete.

    Attributes:
        missing_keys: Required configuration keys which were not provided.
    """

    def __init__(
        self,
        missing_keys: list[str] | None = None,
    ):
        self.missing_keys = missing_keys or []
        message = (
            f"The following GX Cloud variables are required but were not provided: {', '.join(self.missing_keys)}. "
            "Please use the Airflow Connection UI to update your configuration and try again."
        )
        super().__init__(message)


@dataclass(frozen=True)
class GXCloudConfig:
    cloud_access_token: str
    cloud_organization_id: str
    cloud_workspace_id: str


class GXCloudHook(BaseHook):
    """
    Connect to the GX Cloud managed backend.

    :gx_cloud_conn_id str: name of the GX Cloud connection
    """

    conn_name_attr = "gx_cloud_conn_id"
    default_conn_name = "gx_cloud_default"
    conn_type = "gx_cloud"
    hook_name = "Great Expectations Cloud"

    def __init__(self, gx_cloud_conn_id: str = default_conn_name):
        super().__init__()
        self.gx_cloud_conn_id = gx_cloud_conn_id

    def get_conn(self) -> GXCloudConfig:  # type: ignore[override]
        config = self.get_connection(self.gx_cloud_conn_id)
        missing_keys = []
        if not config.password:
            missing_keys.append("GX Cloud Access Token")
        if not config.login:
            missing_keys.append("GX Cloud Organization ID")

        # Extract cloud_workspace_id from extra field
        cloud_workspace_id = config.extra_dejson.get("cloud_workspace_id")
        if not cloud_workspace_id:
            missing_keys.append("GX Cloud Workspace ID")

        if missing_keys:
            raise IncompleteGXCloudConfigError(missing_keys)

        return GXCloudConfig(
            cloud_access_token=config.password,
            cloud_organization_id=config.login,
            cloud_workspace_id=cloud_workspace_id,
        )

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        """Return custom field behaviour."""
        return {
            "hidden_fields": ["schema", "port", "host"],
            "relabeling": {
                "login": "GX Cloud Organization ID",
                "password": "GX Cloud Access Token",
                "extra": 'GX Cloud Workspace ID (JSON: {"cloud_workspace_id": "your-workspace-id"})',
            },
            "placeholders": {
                "extra": '{"cloud_workspace_id": "your-workspace-id"}',
            },
        }

    def test_connection(self) -> tuple[bool, str]:
        try:
            config = self.get_conn()
            load_data_context(context_type="cloud", gx_cloud_config=config)
            return True, "Connection successful."
        except Exception as error:
            return False, str(error)
