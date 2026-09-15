
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.propagation import (
    propagate_with_snapshots,
)
from schrodinger.time_dependent.scattering import (
    rectangular_barrier_on_interior,
    scattering_probabilities,
)
from schrodinger.time_dependent.wavepacket import (
    analyze_wavepacket,
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

    barrier_left = -0.5
    barrier_right = 0.5
    barrier_height = 5.0

    dt = 0.001
    steps = 6000
    snapshot_interval = 500

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=center,
        sigma=sigma,
        wave_number=wave_number,
    )

    diagnostics = analyze_wavepacket(
        wavefunction=wavefunction,
        grid=grid,
        mass=mass,
        hbar=hbar,
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
        "Time-Dependent Rectangular Barrier Scattering"
    )

    print(
        "------------------------------------------------------------"
    )

    print(
        f"Barrier height: "
        f"{barrier_height:.6f}"
    )

    print(
        f"Barrier width:  "
        f"{barrier_right - barrier_left:.6f}"
    )

    print(
        f"Initial <T>:    "
        f"{diagnostics.mean_kinetic_energy:.6f}"
    )

    print(
        f"Sub-barrier:    "
        f"{diagnostics.mean_kinetic_energy < barrier_height}"
    )

    print()

    print(
        f"{'t':>8} "
        f"{'P_left':>12} "
        f"{'P_barrier':>12} "
        f"{'P_right':>12} "
        f"{'Total':>12}"
    )

    maximum_probability_error = 0.0

    for snapshot in snapshots:
        probabilities = (
            scattering_probabilities(
                wavefunction=snapshot.wavefunction,
                grid=grid,
                barrier_left=barrier_left,
                barrier_right=barrier_right,
            )
        )

        probability_error = abs(
            probabilities.total
            - 1.0
        )

        maximum_probability_error = max(
            maximum_probability_error,
            probability_error,
        )

        print(
            f"{snapshot.time:>8.3f} "
            f"{probabilities.left:>12.8f} "
            f"{probabilities.barrier:>12.8f} "
            f"{probabilities.right:>12.8f} "
            f"{probabilities.total:>12.8f}"
        )

    print()

    print(
        f"Maximum probability error: "
        f"{maximum_probability_error:.3e}"
    )

    if maximum_probability_error > 1e-9:
        raise RuntimeError(
            "scattering probability "
            "conservation failed."
        )


if __name__ == "__main__":
    main()