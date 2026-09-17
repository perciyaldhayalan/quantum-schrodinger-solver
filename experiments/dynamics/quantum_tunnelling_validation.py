
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.scattering import (
    extract_asymptotic_scattering,
    rectangular_barrier_on_interior,
)
from schrodinger.time_dependent.tunnelling_validation import (
    packet_averaged_transmission,
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

    barrier_left = -0.5
    barrier_right = 0.5
    barrier_height = 5.0

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

    initial_diagnostics = analyze_wavepacket(
        wavefunction=wavefunction,
        grid=grid,
        mass=mass,
        hbar=hbar,
    )

    stationary_prediction = (
        packet_averaged_transmission(
            wavefunction=wavefunction,
            grid=grid,
            barrier_height=barrier_height,
            barrier_width=(
                barrier_right
                - barrier_left
            ),
            mass=mass,
            hbar=hbar,
        )
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

    final_state = propagator.propagate(
        wavefunction=wavefunction,
        steps=steps,
    )

    tdse_result = extract_asymptotic_scattering(
        wavefunction=final_state,
        grid=grid,
        barrier_left=barrier_left,
        barrier_right=barrier_right,
        separation_tolerance=1e-3,
    )

    prediction_error = abs(
        tdse_result.transmission
        - stationary_prediction.transmission
    )

    print(
        "Quantum Tunnelling Validation"
    )

    print(
        "----------------------------------------------"
    )

    print(
        f"Final time: "
        f"{steps * dt:.6f}"
    )

    print(
        f"Barrier height: "
        f"{barrier_height:.6f}"
    )

    print(
        f"Barrier width: "
        f"{barrier_right - barrier_left:.6f}"
    )

    print(
        f"Initial mean kinetic energy: "
        f"{initial_diagnostics.mean_kinetic_energy:.6f}"
    )

    print(
        f"Mean energy below barrier: "
        f"{initial_diagnostics.mean_kinetic_energy < barrier_height}"
    )

    print()

    print(
        f"TDSE reflection R: "
        f"{tdse_result.reflection:.8f}"
    )

    print(
        f"TDSE transmission T: "
        f"{tdse_result.transmission:.8f}"
    )

    print(
        f"Barrier probability: "
        f"{tdse_result.barrier_probability:.8e}"
    )

    print(
        f"Total probability: "
        f"{tdse_result.total_probability:.12f}"
    )

    print(
        f"Separated: "
        f"{tdse_result.separated}"
    )

    print()

    print(
        f"Positive-p incident probability: "
        f"{stationary_prediction.positive_momentum_probability:.8f}"
    )

    print(
        f"Packet-averaged stationary T: "
        f"{stationary_prediction.transmission:.8f}"
    )

    print(
        f"|T_TDSE - T_stationary|: "
        f"{prediction_error:.8f}"
    )

    if not tdse_result.separated:
        raise RuntimeError(
            "wavepacket has not sufficiently "
            "separated from the barrier."
        )

    if abs(
        tdse_result.total_probability
        - 1.0
    ) > 1e-8:
        raise RuntimeError(
            "probability conservation failed."
        )

    if tdse_result.transmission <= 0.0:
        raise RuntimeError(
            "no quantum tunnelling detected."
        )

    if prediction_error > 0.03:
        raise RuntimeError(
            "TDSE transmission does not agree "
            "with the packet-averaged stationary "
            "prediction."
        )


if __name__ == "__main__":
    main()