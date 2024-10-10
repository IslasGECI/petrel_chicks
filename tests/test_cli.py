from petrel_chicks import cli
from typer.testing import CliRunner

runner = CliRunner()


def tests_plot():
    result = runner.invoke(cli, ["version", "--help"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["plot-peak-mass-model", "--help"])
    assert result.exit_code == 0
    assert " Input file path " in result.stdout
    assert " Season " in result.stdout
