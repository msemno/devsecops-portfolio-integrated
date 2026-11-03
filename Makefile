.PHONY: test lint policy policy-negative app docker-build kind-install

test:
	python -m pytest -q
lint:
	ruff check service labsec tests
policy:
	python -m labsec.cli policy --k8s k8s/base/deployment.yaml --tf-plan fixtures/terraform/secure-plan.json
policy-negative:
	bash scripts/negative_tests.sh
app:
	uvicorn service.main:app --host 127.0.0.1 --port 8080
image:
	docker build -f docker/Dockerfile -t devsecops-demo:local .
