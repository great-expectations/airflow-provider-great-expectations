from __future__ import annotations

import logging
from functools import cache
from typing import TYPE_CHECKING

import pytest
from airflow.models.dagbag import DagBag
from airflow.utils.db import create_default_connections
from airflow.utils.session import NEW_SESSION, provide_session
from airflow.utils.state import DagRunState, State

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

pytestmark = pytest.mark.integration

log = logging.getLogger(__name__)


@provide_session
def get_session(session: Session = NEW_SESSION):
    create_default_connections(session)
    return session


@cache
def get_dag_bag() -> DagBag:
    return DagBag(dag_folder="great_expectations_provider/example_dags")


@pytest.fixture()
def session():
    return get_session()


class TestExampleDag:
    def test_example_dag(self, session: Session, dag_maker):
        dag_id = "gx_provider_example_dag"

        with dag_maker(dag_id=dag_id) as dag:
            dag_run = dag.test()

            assert dag_run.get_state() == DagRunState.SUCCESS
            assert all(
                [ti.state == State.SUCCESS for ti in dag_run.get_task_instances()]
            )


class TestBatchParametersDag:
    def test(self, session: Session, dag_maker):
        dag_id = "gx_provider_example_dag_with_batch_parameters"

        with dag_maker(dag_id=dag_id) as dag:
            dag_run = dag.test()

        assert dag_run.get_state() == DagRunState.SUCCESS
        assert all([ti.state == State.SUCCESS for ti in dag_run.get_task_instances()])
