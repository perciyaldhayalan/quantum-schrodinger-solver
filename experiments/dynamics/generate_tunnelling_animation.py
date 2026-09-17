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
    analyze_wavepacket,
    gaussian_wavepacket,
)
from schrodinger.visualization.animation import (
    create_tunnelling_animation,
    save_animation_gif,
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

    mass = 1.0
    hbar = 1.0

    dt = 0.001
    steps = 10000
    snapshot_interval = 50

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
        "Generating quantum tunnelling animation..."
    )

    print(
        f"Mean kinetic energy: "
        f"{diagnostics.mean_kinetic_energy:.6f}"
    )

    print(
        f"Barrier height: "
        f"{barrier_height:.6f}"
    )

    print(
        f"Sub-barrier mean energy: "
        f"{diagnostics.mean_kinetic_energy < barrier_height}"
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
        f"Animation frames: "
        f"{len(snapshots)}"
    )

    figure, animation = (
        create_tunnelling_animation(
            grid=grid,
            snapshots=snapshots,
            barrier_left=barrier_left,
            barrier_right=barrier_right,
            barrier_height=barrier_height,
            interval=50,
        )
    )

    output_path = (
        "results/animations/tunnelling/"
        "quantum_tunnelling.gif"
    )

    save_animation_gif(
        animation=animation,
        path=output_path,
        fps=20,
        dpi=120,
    )

    plt.close(
        figure
    )

    print(
        f"Animation saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()