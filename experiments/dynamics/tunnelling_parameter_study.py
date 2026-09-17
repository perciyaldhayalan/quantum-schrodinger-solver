import numpy as np

from schrodinger.analysis.tunnelling_study import (
    TunnellingStudyResult,
    run_tunnelling_study,
)
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.wavepacket import (
    analyze_wavepacket,
    gaussian_wavepacket,
)


def print_results(
    title: str,
    result: TunnellingStudyResult,
) -> None:
    print()
    print(title)
    print(
        "------------------------------------------------"
    )

    print(
        f"{'V0':>8} "
        f"{'L':>8} "
        f"{'T TDSE':>12} "
        f"{'T theory':>12} "
        f"{'|Delta T|':>12}"
    )

    for index in range(
        result.barrier_heights.size
    ):
        print(
            f"{result.barrier_heights[index]:>8.3f} "
            f"{result.barrier_widths[index]:>8.3f} "
            f"{result.tdse_transmissions[index]:>12.8f} "
            f"{result.stationary_transmissions[index]:>12.8f} "
            f"{result.agreement_errors[index]:>12.8f}"
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
    steps = 10000

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

    print(
        "Quantum Tunnelling Parameter Study"
    )

    print(
        "================================================"
    )

    print(
        f"Initial mean kinetic energy: "
        f"{diagnostics.mean_kinetic_energy:.6f}"
    )

    width_values = np.asarray(
        [
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
        ],
        dtype=np.float64,
    )

    width_heights = np.full(
        width_values.shape,
        5.0,
        dtype=np.float64,
    )

    width_result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=width_heights,
        barrier_widths=width_values,
        dt=dt,
        steps=steps,
        mass=mass,
        hbar=hbar,
        separation_tolerance=1e-3,
    )

    print_results(
        title="Barrier Width Scan",
        result=width_result,
    )

    height_values = np.asarray(
        [
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
        ],
        dtype=np.float64,
    )

    height_widths = np.full(
        height_values.shape,
        1.0,
        dtype=np.float64,
    )

    height_result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=height_values,
        barrier_widths=height_widths,
        dt=dt,
        steps=steps,
        mass=mass,
        hbar=hbar,
        separation_tolerance=1e-3,
    )

    print_results(
        title="Barrier Height Scan",
        result=height_result,
    )

    if not np.all(
        np.diff(
            width_result.tdse_transmissions
        )
        < 0.0
    ):
        raise RuntimeError(
            "TDSE transmission did not decrease "
            "monotonically with barrier width."
        )

    if not np.all(
        np.diff(
            height_result.tdse_transmissions
        )
        < 0.0
    ):
        raise RuntimeError(
            "TDSE transmission did not decrease "
            "monotonically with barrier height."
        )

    maximum_probability_error = max(
        float(
            np.max(
                np.abs(
                    width_result.total_probabilities
                    - 1.0
                )
            )
        ),
        float(
            np.max(
                np.abs(
                    height_result.total_probabilities
                    - 1.0
                )
            )
        ),
    )

    print()

    print(
        f"Maximum probability error: "
        f"{maximum_probability_error:.3e}"
    )

    if maximum_probability_error > 1e-8:
        raise RuntimeError(
            "probability conservation failed."
        )


if __name__ == "__main__":
    main()