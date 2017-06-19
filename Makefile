.PHONY: docker run

docker:
	docker build . -f docker-files/Dockerfile -t off-nadir-optimization

run:
	docker run -it \
		-v $(PWD):/app \
		off-nadir-optimization \
		/app/test_solver.py

test:
	docker run -it \
		-v $(PWD):/app \
		off-nadir-optimization \
		pytest
