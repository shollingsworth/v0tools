.DEFAULT_GOAL := pkg

docs := ./docs
srcdir := ./src
pkgname := v0tools

documentation: clean
	@echo "Running docs"
	mkdir -p $(docs)/static/api
	./scripts/gendoc.py
	pydoctor \
		-v \
		-W \
		--html-output=$(docs)/static/api \
		--buildtime="1996-06-17 15:00:00" \
		$(srcdir)/$(pkgname)
	./scripts/checkundocced.py

docker_tests:
	./scripts/dockertest.sh ./docker/deb36.Dockerfile
	./scripts/dockertest.sh ./docker/deb37.Dockerfile
	./scripts/dockertest.sh ./docker/deb38.Dockerfile
	./scripts/dockertest.sh ./docker/deb39.Dockerfile
	./scripts/dockertest.sh ./docker/deb310.Dockerfile
	./scripts/dockertest.sh ./docker/centos7.Dockerfile
	./scripts/dockertest.sh ./docker/arch.Dockerfile

install_local:
	pip3 install .

pkg: documentation clean
	@echo "Running PKG"
	python3 setup.py sdist
	twine check dist/*

upload:
	@echo "Running upload"
	twine upload --repository v0tools dist/*

bump_version:
	# order is important here
	./scripts/version_bump.py
	./scripts/gendoc.py
	git add ./docs/content/changelog/_index.md
	git add ./VERSION
	git diff HEAD
	git commit -S --amend
	bash -c "git tag v$$(cat VERSION)"

push:
	$(eval tag = $(shell cat VERSION))
	git push -u origin HEAD
	git push -u origin v$(tag)

release: pkg upload push
	@echo "Running Release"

test_create:
	./scripts/unittest_create.py

test: test_create
	./scripts/runtests.sh

clean:
	rm -rfv dist/* src/*.egg-info $(docs)/static/api
	find -type f -name '*.pyc' -delete -print
	find -type d -name __pycache__ -delete -print

server:
	rm -rfv $(docs)/public
	mkdir -p $(docs)/public
	bash -c "cd $(docs); hugo server"

hugo_deploy: documentation
	rm -rfv $(docs)/public
	mkdir -p $(docs)/public
	bash -c "cd $(docs); hugo; hugo deploy"
