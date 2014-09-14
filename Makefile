run:
	OLDPATH=$PYTHONPATH
	export PYTHONPATH=$PYTHONPATH:`pwd`
	./bin/vcii
	export PYTHONPATH=$OLDPATH

test:
	coverage run --branch --source=vcii --omit='*__*','*test*' -m unittest
	coverage report

clean:
	rm -rf MANIFEST htmlcov dist build
