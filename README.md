Setup Instructions

1. Install [Devbox](https://www.jetpack.io/devbox/docs/quickstart/).
2. Install an isolated Python version with Devbox. This may take a little while.
  ```shell
  make env
  ```

3. Create a virtual environment and install Poetry to manage the Python dependencies.
  ```shell
  make setup
  ```

4. Use poetry to install the Python dependencies. 
  ```shell
  make init
  ```