FROM python:3.11
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    geci-test-tools \
    mutmut \
    mypy \
    pandas-stubs \
    pylint \
    pytest \
    pytest-cov \
    pytest-mock \
    pytest-mpl
