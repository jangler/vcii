export PYTHONPATH=.

run:
	./bin/vcii

test:
	coverage run --branch --source=vcii --omit='*__*','*test*' -m unittest
	coverage report

clean:
	rm -rf MANIFEST htmlcov dist build
