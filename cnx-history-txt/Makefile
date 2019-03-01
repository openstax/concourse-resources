build:
	python setup.py sdist
	docker build -t m1yag1/concourse-history-txt-resource .

publish: build
	docker push m1yag1/concourse-history-txt-resource
