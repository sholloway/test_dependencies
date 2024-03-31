.PHONY: env setup init run test benchmark viz_benchmark check

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

# Initialize the project with Poetry.
# This only needs to be done once.
# There are a few dev dependencies (bpython, line-profiler, pudb)
# that need to be compiled on install. This doesn't play well 
# with the nix-based project setup (i.e. devbox). 
# To work around this:
# 1. make env
# 2. make setup
# 3. exit
# 4. make init
# 5. make env
init:
	@( \
	source .venv/bin/activate; \
	poetry config virtualenvs.in-project true --local; \
	poetry install; \
	)

# Runs the app in production mode.
# Typical development flow is:
# make check test run
run:
	@( \
	source .venv/bin/activate; \
	poetry run python -O test_dependencies \
		--dependency_list ./examples/2k.csv \
		--changed_list ./examples/changed_list.txt \
		--degrees 3; \
	)

# Run unit tests. Includes all files in ./test named test_*.py and *_test.py.
# To run a single test in a test class do something like:
# 	poetry run pytest ./tests/core/task_scheduler_test.py::TestTaskScheduler::test_running_simple_functions -s
# 
# Use the -s flag to have print statements show up during test runs.
# 	poetry run pytest -k "simulation_test.py" -s
#
# Use --durations=0 to find slow running tests.
# 	poetry run pytest --durations=0
test:
	@( \
	source .venv/bin/activate; \
	poetry run pytest; \
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