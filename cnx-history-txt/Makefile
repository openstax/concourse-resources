build:
	python setup.py sdist
	docker build -t openstax/concourse-history-txt-resource .

publish: build
	docker push openstax/concourse-history-txt-resource

test:
	pytest tests/test_resource.py -vvv
