FROM python:3.12
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    geci-test-tools \
    mutmut==2.* \
    mypy \
    pandas-stubs \
    pylint \
    pytest \
    pytest-cov \
    pytest-mock \
    pytest-mpl
