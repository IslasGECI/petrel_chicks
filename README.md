<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
# Petrel Chicks
[![codecov](https://codecov.io/gh/IslasGECI/petrel_chicks/graph/badge.svg?token=1595ab76-2b03-4082-914e-5de7cb35e27a)](https://codecov.io/gh/IslasGECI/petrel_chicks)
![example branch parameter](https://github.com/IslasGECI/petrel_chicks/actions/workflows/actions.yml/badge.svg)
![licencia](https://img.shields.io/github/license/IslasGECI/petrel_chicks)
![languages](https://img.shields.io/github/languages/top/IslasGECI/petrel_chicks)
![commits](https://img.shields.io/github/commit-activity/y/IslasGECI/petrel_chicks)
![PyPI - Version](https://img.shields.io/pypi/v/petrel-chicks)

Module to analyze the growth of petrel chicks. It fits mass-vs-age models per
season, estimates peak mass, and plots the fitted curves.

## Usage

This module installs the `petrel-chicks` command line interface with the
following commands:

### Plot all peak mass models

Fit and plot a mass-vs-age model for every season found in the data. The age at
peak mass is marked as a point on each curve:

```bash
petrel-chicks plot-all-peak-mass-models \
    --data-path data/raw/chicks.csv \
    --output-path reports/figures/all_peak_mass_models.png
```

Options:

| Option | Description | Default |
| --- | --- | --- |
| `--data-path` | Input file path | Required |
| `--font-name` | Font family for the figure | `STIXGeneral` |
| `--output-path` | Output file path | Required |
| `--age-at-peak-mass-label / --no-age-at-peak-mass-label` | Show age at peak mass label | `False` |

### Plot peak mass model

Plot the measured mass of the chicks together with the fitted model for a given
season:

```bash
petrel-chicks plot-peak-mass-model \
    --data-path data/raw/chicks.csv \
    --season 2019 \
    --output-path reports/figures/peak_mass_model_2019.png
```

Options:

| Option | Description | Default |
| --- | --- | --- |
| `--data-path` | Input file path | Required |
| `--season` | Season | Required |
| `--output-path` | Output file path | Required |

