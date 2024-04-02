.PHONY: env setup init run_2k run_100k test benchmark viz_benchmark check

# Creates an isolated Nix shell for working in.
# Note: This is optional. If you're not using Nix and manage your Python install
# some other way, then just ignore this make target.
# Installs Python, git, make, cloc the first time it's run.
env:
	devbox shell 

# Create a Python virtual environment, install pip, and install Poetry.
setup:
	@( \
	set -e ; \
	python -m venv ./.venv; \
	source .venv/bin/activate; \
	python -m ensurepip --upgrade; \
	python -m pip install --upgrade pip; \
	pip install -r requirements.txt; \
	)

# Initialize the project with Poetry and install dependencies.
init:
	@( \
	source .venv/bin/activate; \
	poetry config virtualenvs.in-project true --local; \
	poetry install; \
	)

# Runs the app in production mode with a 2000 member DAG.
run_2k:
	@( \
	source .venv/bin/activate; \
	poetry run python -O test_dependencies \
		--dependency_list ./examples/2k.csv \
		--changed_list ./examples/2k_changed_list.txt \
		--degrees 3; \
	)

# Runs the app in production mode with a 100K+ member DAG.
run_100k:
	@( \
	source .venv/bin/activate; \
	poetry run python -O test_dependencies \
		--dependency_list ./examples/100k.csv \
		--changed_list ./examples/100k_changed_list.txt \
		--degrees 5; \
	)

# Run unit tests. Includes all files in ./test named test_*.py and *_test.py.
test:
	@( \
	source .venv/bin/activate; \
	poetry run pytest ./tests; \
	)

# Run all of the benchmark tests.
# 
# Outputs a table with the following columns:
# 	min: The fastest round.
# 	mean: The average round
# 	max: The slowest round
#		median: The 50th-percentile.
#		stddev: The standard deviation. Lower values suggest more consistent performance.
#		iqr: (Interquartile Range): A statistical measure that represents the range 
#         between the first quartile (25th percentile) and the third quartile 
#         (75th percentile) of a dataset. A larger IQR could indicate more 
#					variability in performance, while a smaller IQR suggests more consistent performance.
#		outliers: Data points that significantly deviate from the rest of the data in a dataset.
#		ops: 1000 operations per second. Higher the better.
#		rounds: The number of times a benchmark round was ran.
#		iterations: The number of iterations per round.
benchmark:
	@( \
	source .venv/bin/activate; \
	poetry run pytest benchmarks --benchmark-columns="min, mean, max, median, stddev, iqr, outliers, ops, rounds, iterations"; \
	)

# Run the benchmarks and generate histograms for each test group.
# Use the -m option to only generate an image for a specific group name.
viz_benchmark:
	@( \
	source .venv/bin/activate; \
	poetry run pytest ./benchmarks --benchmark-histogram=./benchmark_histograms/$(shell date +%m_%d_%y@%H_%M)/; \
	)

# Perform static type checking on the project.
check:
	@( \
	source .venv/bin/activate; \
	poetry run mypy --check-untyped-defs --config-file mypy.ini -p test_dependencies; \
	)