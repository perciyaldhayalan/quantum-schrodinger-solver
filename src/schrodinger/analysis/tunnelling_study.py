from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

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

ArrayComplex = NDArray[np.complex128]
ArrayFloat = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class TunnellingStudyResult:
    barrier_heights: ArrayFloat
    barrier_widths: ArrayFloat
    tdse_transmissions: ArrayFloat
    stationary_transmissions: ArrayFloat
    reflection_probabilities: ArrayFloat
    barrier_probabilities: ArrayFloat
    total_probabilities: ArrayFloat
    agreement_errors: ArrayFloat


def run_tunnelling_study(
    grid: Grid1D,
    initial_wavefunction: ArrayComplex,
    barrier_heights: ArrayFloat,
    barrier_widths: ArrayFloat,
    dt: float,
    steps: int,
    mass: float = 1.0,
    hbar: float = 1.0,
    separation_tolerance: float = 1e-3,
) -> TunnellingStudyResult:
    _validate_study_inputs(
        barrier_heights=barrier_heights,
        barrier_widths=barrier_widths,
    )

    if barrier_heights.size != barrier_widths.size:
        raise ValueError(
            "barrier_heights and barrier_widths "
            "must have the same size."
        )

    count = barrier_heights.size

    tdse_transmissions = np.empty(
        count,
        dtype=np.float64,
    )

    stationary_transmissions = np.empty(
        count,
        dtype=np.float64,
    )

    reflection_probabilities = np.empty(
        count,
        dtype=np.float64,
    )

    barrier_probabilities = np.empty(
        count,
        dtype=np.float64,
    )

    total_probabilities = np.empty(
        count,
        dtype=np.float64,
    )

    agreement_errors = np.empty(
        count,
        dtype=np.float64,
    )

    for index in range(count):
        height = float(
            barrier_heights[index]
        )

        width = float(
            barrier_widths[index]
        )

        barrier_left = (
            -width / 2.0
        )

        barrier_right = (
            width / 2.0
        )

        potential = (
            rectangular_barrier_on_interior(
                grid=grid,
                barrier_left=barrier_left,
                barrier_right=barrier_right,
                barrier_height=height,
            )
        )

        propagator = CrankNicolsonPropagator(
            grid=grid,
            potential=potential,
            dt=dt,
            mass=mass,
            hbar=hbar,
        )

        final_wavefunction = (
            propagator.propagate(
                wavefunction=initial_wavefunction,
                steps=steps,
            )
        )

        tdse_result = (
            extract_asymptotic_scattering(
                wavefunction=final_wavefunction,
                grid=grid,
                barrier_left=barrier_left,
                barrier_right=barrier_right,
                separation_tolerance=(
                    separation_tolerance
                ),
            )
        )

        if not tdse_result.separated:
            raise RuntimeError(
                "wavepacket has not sufficiently "
                "separated from the barrier."
            )

        stationary_result = (
            packet_averaged_transmission(
                wavefunction=initial_wavefunction,
                grid=grid,
                barrier_height=height,
                barrier_width=width,
                mass=mass,
                hbar=hbar,
            )
        )

        tdse_transmissions[index] = (
            tdse_result.transmission
        )

        stationary_transmissions[index] = (
            stationary_result.transmission
        )

        reflection_probabilities[index] = (
            tdse_result.reflection
        )

        barrier_probabilities[index] = (
            tdse_result.barrier_probability
        )

        total_probabilities[index] = (
            tdse_result.total_probability
        )

        agreement_errors[index] = abs(
            tdse_result.transmission
            - stationary_result.transmission
        )

    return TunnellingStudyResult(
        barrier_heights=np.asarray(
            barrier_heights,
            dtype=np.float64,
        ).copy(),
        barrier_widths=np.asarray(
            barrier_widths,
            dtype=np.float64,
        ).copy(),
        tdse_transmissions=tdse_transmissions,
        stationary_transmissions=(
            stationary_transmissions
        ),
        reflection_probabilities=(
            reflection_probabilities
        ),
        barrier_probabilities=(
            barrier_probabilities
        ),
        total_probabilities=(
            total_probabilities
        ),
        agreement_errors=agreement_errors,
    )


def _validate_study_inputs(
    barrier_heights: ArrayFloat,
    barrier_widths: ArrayFloat,
) -> None:
    if barrier_heights.ndim != 1:
        raise ValueError(
            "barrier_heights must be "
            "one-dimensional."
        )

    if barrier_widths.ndim != 1:
        raise ValueError(
            "barrier_widths must be "
            "one-dimensional."
        )

    if barrier_heights.size == 0:
        raise ValueError(
            "barrier_heights must not be empty."
        )

    if barrier_widths.size == 0:
        raise ValueError(
            "barrier_widths must not be empty."
        )

    if not np.all(
        np.isfinite(barrier_heights)
    ):
        raise ValueError(
            "barrier_heights must be finite."
        )

    if not np.all(
        np.isfinite(barrier_widths)
    ):
        raise ValueError(
            "barrier_widths must be finite."
        )

    if np.any(
        barrier_heights < 0.0
    ):
        raise ValueError(
            "barrier_heights must be "
            "non-negative."
        )

    if np.any(
        barrier_widths <= 0.0
    ):
        raise ValueError(
            "barrier_widths must be positive."
        )