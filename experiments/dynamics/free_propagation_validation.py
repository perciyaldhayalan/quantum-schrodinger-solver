import numpy as np

from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.propagation import (
    free_particle_expected_position,
    free_particle_expected_width,
    propagate_with_snapshots,
)
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
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
    mass = 1.0
    hbar = 1.0
    dt = 0.001
    steps = 2000
    snapshot_interval = 250

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=center,
        sigma=sigma,
        wave_number=wave_number,
    )

    propagator = CrankNicolsonPropagator(
        grid=grid,
        potential=potential,
        dt=dt,
        mass=mass,
        hbar=hbar,
    )

    snapshots = propagate_with_snapshots(
        propagator=propagator,
        wavefunction=wavefunction,
        steps=steps,
        snapshot_interval=snapshot_interval,
    )

    print(
        "Free Gaussian Packet TDSE Validation"
    )

    print(
        "--------------------------------------------------------------"
    )

    print(
        f"{'t':>8} "
        f"{'<x> num':>12} "
        f"{'<x> exact':>12} "
        f"{'sigma num':>12} "
        f"{'sigma exact':>12} "
        f"{'norm':>14}"
    )

    maximum_position_error = 0.0
    maximum_width_relative_error = 0.0
    maximum_norm_drift = 0.0

    initial_norm = snapshots[0].norm

    for snapshot in snapshots:
        expected_position = (
            free_particle_expected_position(
                initial_position=center,
                wave_number=wave_number,
                time=snapshot.time,
                mass=mass,
                hbar=hbar,
            )
        )

        expected_width = (
            free_particle_expected_width(
                initial_sigma=sigma,
                time=snapshot.time,
                mass=mass,
                hbar=hbar,
            )
        )

        position_error = abs(
            snapshot.position
            - expected_position
        )

        width_relative_error = abs(
            snapshot.position_uncertainty
            - expected_width
        ) / expected_width

        norm_drift = abs(
            snapshot.norm
            - initial_norm
        )

        maximum_position_error = max(
            maximum_position_error,
            position_error,
        )

        maximum_width_relative_error = max(
            maximum_width_relative_error,
            width_relative_error,
        )

        maximum_norm_drift = max(
            maximum_norm_drift,
            norm_drift,
        )

        print(
            f"{snapshot.time:>8.3f} "
            f"{snapshot.position:>12.6f} "
            f"{expected_position:>12.6f} "
            f"{snapshot.position_uncertainty:>12.6f} "
            f"{expected_width:>12.6f} "
            f"{snapshot.norm:>14.10f}"
        )

    print()

    print(
        f"Maximum position error: "
        f"{maximum_position_error:.3e}"
    )

    print(
        f"Maximum width relative error: "
        f"{maximum_width_relative_error:.3e}"
    )

    print(
        f"Maximum norm drift: "
        f"{maximum_norm_drift:.3e}"
    )

    if maximum_position_error > 5e-3:
        raise RuntimeError(
            "free-particle position validation failed."
        )

    if maximum_width_relative_error > 3e-3:
        raise RuntimeError(
            "free-particle spreading validation failed."
        )

    if maximum_norm_drift > 1e-9:
        raise RuntimeError(
            "probability conservation validation failed."
        )


if __name__ == "__main__":
    main()