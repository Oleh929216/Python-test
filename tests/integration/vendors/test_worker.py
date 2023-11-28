import pytest
from pytest_lazyfixture import lazy_fixture

from pytest_celery import CELERY_SETUP_WORKER
from pytest_celery import DEFAULT_WORKER_ENV
from pytest_celery import CeleryBackendCluster
from pytest_celery import CeleryTestWorker
from pytest_celery import CeleryWorkerContainer
from tests.defaults import ALL_WORKERS_FIXTURES


@pytest.mark.parametrize("container", lazy_fixture(ALL_WORKERS_FIXTURES))
class test_celery_worker_container:
    def test_client(self, container: CeleryWorkerContainer):
        assert container.client
        assert container.client == container

    def test_celeryconfig(self, container: CeleryWorkerContainer):
        with pytest.raises(NotImplementedError):
            container.celeryconfig

    class test_disabling_cluster:
        @pytest.fixture
        def celery_backend_cluster(self) -> CeleryBackendCluster:
            return None

        def test_disabling_backend_cluster(self, container: CeleryWorkerContainer):
            assert container.logs().count("results:     disabled://")

            results = DEFAULT_WORKER_ENV["CELERY_BROKER_URL"]
            assert container.logs().count(f"transport:   {results}")


@pytest.mark.parametrize("worker", [lazy_fixture(CELERY_SETUP_WORKER)])
class test_base_test_worker:
    def test_config(self, worker: CeleryTestWorker):
        with pytest.raises(NotImplementedError):
            worker.config()
