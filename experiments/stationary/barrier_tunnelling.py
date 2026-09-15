import numpy as np

from schrodinger.analysis.tunnelling import (
    rectangular_barrier_transmission,
    tunnelling_decay_constant,
)


def main() -> None:
    barrier_height = 5.0
    barrier_width = 1.0
    mass = 1.0
    hbar = 1.0

    energies = np.asarray(
        [
            0.5,
            1.0,
            2.0,
            3.0,
            4.0,
            4.5,
            5.0,
            6.0,
            8.0,
            10.0,
        ],
        dtype=np.float64,
    )

    print(
        "Rectangular Barrier Transmission"
    )
    print(
        "--------------------------------"
    )

    print(
        f"Barrier height: {barrier_height:.4f}"
    )
    print(
        f"Barrier width:  {barrier_width:.4f}"
    )
    print()

    print(
        f"{'Energy':>10} "
        f"{'Regime':>16} "
        f"{'T':>14} "
        f"{'R':>14}"
    )

    for energy in energies:
        result = rectangular_barrier_transmission(
            energy=float(energy),
            barrier_height=barrier_height,
            barrier_width=barrier_width,
            mass=mass,
            hbar=hbar,
        )

        print(
            f"{energy:>10.4f} "
            f"{result.regime:>16} "
            f"{result.transmission:>14.8f} "
            f"{result.reflection:>14.8f}"
        )

    tunnelling_energy = 2.0

    kappa = tunnelling_decay_constant(
        energy=tunnelling_energy,
        barrier_height=barrier_height,
        mass=mass,
        hbar=hbar,
    )

    print()
    print(
        "Sub-barrier diagnostic"
    )
    print(
        "--------------------------------"
    )
    print(
        f"Energy: {tunnelling_energy:.4f}"
    )
    print(
        f"Kappa: {kappa:.8f}"
    )
    print(
        f"Penetration length 1/kappa: "
        f"{1.0 / kappa:.8f}"
    )


if __name__ == "__main__":
    main()