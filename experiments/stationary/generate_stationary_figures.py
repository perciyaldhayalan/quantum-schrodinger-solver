import matplotlib.pyplot as plt
import numpy as np

from schrodinger.grid import Grid1D
from schrodinger.stationary.solver import (
    solve_stationary,
)
from schrodinger.visualization.energy_levels import (
    plot_energy_levels,
)
from schrodinger.visualization.probability import (
    plot_probability_density,
    save_figure,
)
from schrodinger.visualization.stationary import (
    plot_stationary_states,
)


def main() -> None:
    grid = Grid1D(
        -6.0,
        6.0,
        1201,
    )

    potential = (
        0.5
        * grid.interior**2
    )

    states = solve_stationary(
        grid=grid,
        potential=potential,
        states=5,
    )

    full_potential = (
        0.5
        * grid.values**2
    )

    stationary_figure = (
        plot_stationary_states(
            grid=grid,
            potential=full_potential,
            states=states,
            title=(
                "Harmonic Oscillator "
                "Stationary States"
            ),
        )
    )

    save_figure(
        figure=stationary_figure,
        path=(
            "results/figures/stationary/"
            "harmonic_oscillator_states.png"
        ),
    )

    energies = np.asarray(
        [
            state.energy
            for state in states
        ],
        dtype=np.float64,
    )

    energy_figure = plot_energy_levels(
        energies=energies,
        title=(
            "Harmonic Oscillator "
            "Energy Levels"
        ),
    )

    save_figure(
        figure=energy_figure,
        path=(
            "results/figures/stationary/"
            "harmonic_oscillator_energies.png"
        ),
    )

    probability_figure = (
        plot_probability_density(
            grid=grid,
            wavefunction=(
                states[0].wavefunction
            ),
            title=(
                "Harmonic Oscillator "
                "Ground-State Probability"
            ),
        )
    )

    save_figure(
        figure=probability_figure,
        path=(
            "results/figures/stationary/"
            "harmonic_oscillator_ground_density.png"
        ),
    )

    plt.close(
        stationary_figure
    )

    plt.close(
        energy_figure
    )

    plt.close(
        probability_figure
    )

    print(
        "Stationary figures generated successfully."
    )


if __name__ == "__main__":
    main()