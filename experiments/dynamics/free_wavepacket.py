from schrodinger.grid import Grid1D
from schrodinger.time_dependent.wavepacket import (
    analyze_wavepacket,
    gaussian_wavepacket,
)


def main() -> None:
    grid = Grid1D(
        -30.0,
        30.0,
        6001,
    )

    center = -8.0
    sigma = 1.5
    wave_number = 2.0
    mass = 1.0
    hbar = 1.0

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=center,
        sigma=sigma,
        wave_number=wave_number,
    )

    result = analyze_wavepacket(
        wavefunction=wavefunction,
        grid=grid,
        mass=mass,
        hbar=hbar,
    )

    expected_momentum = (
        hbar
        * wave_number
    )

    expected_delta_p = (
        hbar
        / (
            2.0
            * sigma
        )
    )

    expected_uncertainty = (
        hbar / 2.0
    )

    expected_kinetic_energy = (
        (
            expected_momentum**2
            + expected_delta_p**2
        )
        / (
            2.0
            * mass
        )
    )

    print(
        "Gaussian Wavepacket Diagnostics"
    )
    print(
        "--------------------------------"
    )

    print(
        f"Grid points: {grid.size}"
    )

    print(
        f"dx: {grid.dx:.8f}"
    )

    print(
        f"Center x0: {center:.8f}"
    )

    print(
        f"Sigma: {sigma:.8f}"
    )

    print(
        f"Wave number k0: "
        f"{wave_number:.8f}"
    )

    print()

    print(
        f"Norm: "
        f"{result.norm:.12f}"
    )

    print(
        f"<x>: "
        f"{result.position:.8f}"
    )

    print(
        f"Expected <x>: "
        f"{center:.8f}"
    )

    print(
        f"<p>: "
        f"{result.momentum:.8f}"
    )

    print(
        f"Expected <p>: "
        f"{expected_momentum:.8f}"
    )

    print()

    print(
        f"Delta x: "
        f"{result.position_uncertainty:.8f}"
    )

    print(
        f"Expected Delta x: "
        f"{sigma:.8f}"
    )

    print(
        f"Delta p: "
        f"{result.momentum_uncertainty:.8f}"
    )

    print(
        f"Expected Delta p: "
        f"{expected_delta_p:.8f}"
    )

    print(
        f"Delta x Delta p: "
        f"{result.uncertainty_product:.8f}"
    )

    print(
        f"Expected hbar/2: "
        f"{expected_uncertainty:.8f}"
    )

    print()

    print(
        f"<T>: "
        f"{result.mean_kinetic_energy:.8f}"
    )

    print(
        f"Expected <T>: "
        f"{expected_kinetic_energy:.8f}"
    )


if __name__ == "__main__":
    main()