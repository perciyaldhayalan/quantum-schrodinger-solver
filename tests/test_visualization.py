import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

matplotlib.use("Agg")

from schrodinger.grid import Grid1D
from schrodinger.stationary.solver import (
    solve_stationary,
)
from schrodinger.visualization.energy_levels import (
    plot_energy_levels,
)
from schrodinger.visualization.probability import (
    plot_probability_density,
    probability_density,
    save_figure,
)
from schrodinger.visualization.stationary import (
    plot_stationary_states,
)


def test_probability_density() -> None:
    wavefunction = np.asarray(
        [
            1.0 + 0.0j,
            0.0 + 1.0j,
        ],
        dtype=np.complex128,
    )

    result = probability_density(
        wavefunction=wavefunction
    )

    assert np.allclose(
        result,
        np.asarray(
            [
                1.0,
                1.0,
            ]
        ),
    )


def test_probability_plot_created() -> None:
    grid = Grid1D(
        -5.0,
        5.0,
        501,
    )

    wavefunction = np.exp(
        -(grid.values**2)
    ).astype(
        np.complex128
    )

    figure = plot_probability_density(
        grid=grid,
        wavefunction=wavefunction,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_energy_level_plot_created() -> None:
    energies = np.asarray(
        [
            0.5,
            1.5,
            2.5,
        ],
        dtype=np.float64,
    )

    figure = plot_energy_levels(
        energies=energies
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_stationary_state_plot_created() -> None:
    grid = Grid1D(
        -6.0,
        6.0,
        801,
    )

    interior_potential = (
        0.5
        * grid.interior**2
    )

    states = solve_stationary(
        grid=grid,
        potential=interior_potential,
        states=3,
    )

    full_potential = (
        0.5
        * grid.values**2
    )

    figure = plot_stationary_states(
        grid=grid,
        potential=full_potential,
        states=states,
    )

    assert len(
        figure.axes
    ) == 1

    plt.close(
        figure
    )


def test_save_figure(
    tmp_path: pytest.TempPathFactory,
) -> None:
    figure = plot_energy_levels(
        energies=np.asarray(
            [
                0.5,
                1.5,
            ],
            dtype=np.float64,
        )
    )

    output = (
        tmp_path
        / "energy_levels.png"
    )

    save_figure(
        figure=figure,
        path=output,
    )

    assert output.exists()

    plt.close(
        figure
    )


def test_empty_energy_array_rejected() -> None:
    with pytest.raises(ValueError):
        plot_energy_levels(
            energies=np.asarray(
                [],
                dtype=np.float64,
            )
        )


def test_invalid_probability_wavefunction_rejected() -> None:
    with pytest.raises(ValueError):
        probability_density(
            wavefunction=np.asarray(
                [
                    np.nan,
                    1.0,
                ],
                dtype=np.float64,
            )
        )