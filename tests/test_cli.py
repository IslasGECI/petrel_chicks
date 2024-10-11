from petrel_chicks import cli
from typer.testing import CliRunner
from geci_test_tools import assert_exist, if_exist_remove

runner = CliRunner()


def tests_plot():
    result = runner.invoke(cli, ["version", "--help"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["plot-peak-mass-model", "--help"])
    assert result.exit_code == 0
    assert " Input file path " in result.stdout
    assert " Season " in result.stdout
    assert " Output file path " in result.stdout

    data_path = "tests/data/medidas_morfometricas_con_edades.csv"
    output_path = "tests/data/peak_mass_model.png"
    if_exist_remove(output_path)
    result = runner.invoke(
        cli,
        [
            "plot-peak-mass-model",
            "--data-path",
            data_path,
            "--season",
            2015,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    assert_exist(output_path)
