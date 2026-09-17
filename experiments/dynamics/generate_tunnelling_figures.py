import matplotlib.pyplot as plt

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.propagation import (
    propagate_with_snapshots,
)
from schrodinger.time_dependent.scattering import (
    rectangular_barrier_on_interior,
)
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)
from schrodinger.visualization.probability import (
    save_figure,
)
from schrodinger.visualization.tunnelling import (
    plot_scattering_probabilities,
    plot_tunnelling_snapshots,
)


def main() -> None:
    grid = Grid1D(
        -30.0,
        30.0,
        3001,
    )

    center = -10.0
    sigma = 1.5
    wave_number = 2.0

    barrier_left = -0.5
    barrier_right = 0.5
    barrier_height = 5.0

    dt = 0.001
    steps = 10000
    snapshot_interval = 250

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=center,
        sigma=sigma,
        wave_number=wave_number,
    )

    potential = rectangular_barrier_on_interior(
        grid=grid,
        barrier_left=barrier_left,
        barrier_right=barrier_right,
        barrier_height=barrier_height,
    )

    propagator = CrankNicolsonPropagator(
        grid=grid,
        potential=potential,
        dt=dt,
    )

    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavefunction,
        steps=steps,
        snapshot_interval=snapshot_interval,
    )

    selected_times = {
        0.0,
        2.5,
        4.5,
        5.0,
        5.5,
        7.5,
        10.0,
    }

    selected_snapshots = [
        snapshot
        for snapshot in snapshots
        if any(
            abs(
                snapshot.time
                - selected_time
            )
            < 1e-10
            for selected_time in selected_times
        )
    ]

    snapshot_figure = (
        plot_tunnelling_snapshots(
            grid=grid,
            snapshots=selected_snapshots,
            barrier_left=barrier_left,
            barrier_right=barrier_right,
            barrier_height=barrier_height,
            title=(
                "Gaussian Wavepacket "
                "Scattering from a "
                "Rectangular Barrier"
            ),
        )
    )

    save_figure(
        figure=snapshot_figure,
        path=(
            "results/figures/dynamics/"
            "tunnelling_snapshots.png"
        ),
    )

    probability_figure = (
        plot_scattering_probabilities(
            grid=grid,
            snapshots=snapshots,
            barrier_left=barrier_left,
            barrier_right=barrier_right,
            title=(
                "Reflection, Barrier and "
                "Transmission Probabilities"
            ),
        )
    )

    save_figure(
        figure=probability_figure,
        path=(
            "results/figures/tunnelling/"
            "scattering_probabilities.png"
        ),
    )

    plt.close(
        snapshot_figure
    )

    plt.close(
        probability_figure
    )

    print(
        "TDSE tunnelling figures "
        "generated successfully."
    )


if __name__ == "__main__":
    main()