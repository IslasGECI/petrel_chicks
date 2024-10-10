from petrel_chicks import cli
from typer.testing import CliRunner

runner = CliRunner()


def tests_plot():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
