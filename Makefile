style_code:
	black app/
	ruff check --fix

docker_push:
	docker build --platform=linux/amd64 -t shantibb/backend .
	docker push shantibb/backend
