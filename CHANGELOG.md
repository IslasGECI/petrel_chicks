# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Fixed

### Changed

### Removed

## [0.6.0] - 2025-09-19
### Added
- The method `plot_model_for_all_seasons()` from class `_Plotter_model_for_all_seasons` now plots the maximum peak mass as a point.

## [0.5.2] - 2025-07-24
### Fixed
- Function `set_ticks_and_limits()` set the y limits only with first and last rounded values for arrays of any length.

## [0.5.1] - 2025-07-24
### Fixed
- Function `set_ticks_and_limits()` set the y limits only with first and last rounded values.

## [0.5.0] - 2025-07-17

### Added
- The command `plot-all-peak-mass-models` now receives the font family name as argument.

## [0.4.2] - 2025-07-14
### Fixed
- Set the figure dpi to 600 in the command `plot-all-peak-mass-models`
- Set the figure label font size to 18 in the command `plot-all-peak-mass-models`

## [0.4.1] - 2024-11-11
### Changed
- Change the units in the "Chick age" axis

## [0.4.0] - 2024-11-11

### Added

- New command `plot-all-peak-mass-models` to `petrel-chicks` entrypoint.

## [0.3.0] - 2024-10-11

### Added

- New cli entrypoint `petrel-chicks`.
- New command `plot-peak-mass-model` to `petrel-chicks` entrypoint.


## [0.2.1] - 2024-08-02

### Fixed

- Function `fill_empty_age()` correctly fill with different nests. This functions now expect `ID_nido` and `Year` columns to fill age by each chick.

## [0.2.0] - 2024-08-01

### Added

- Add function `fill_empty_age()` to complete chicks age in all rows.

[unreleased]: https://github.com/IslasGECI/petrel_chicks/compare/v0.1.0...HEAD
