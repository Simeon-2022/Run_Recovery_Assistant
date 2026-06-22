PY=py -3

.PHONY: install-backend test-backend smoke-frontend test-all

install-backend:
	$(PY) -m pip install -r backend/requirements.txt

test-backend:
	$(PY) -m pytest backend/tests

smoke-frontend:
	@echo "Run frontend smoke test (requires Node.js and Playwright)"
	cd frontend && npm install && npm run smoke

test-all: install-backend test-backend smoke-frontend
