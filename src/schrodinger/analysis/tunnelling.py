from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

ArrayFloat = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class BarrierTransmissionResult:
    energy: float
    barrier_height: float
    barrier_width: float
    transmission: float
    reflection: float
    regime: str


def tunnelling_decay_constant(
    energy: float,
    barrier_height: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> float:
    _validate_parameters(
        energy=energy,
        barrier_height=barrier_height,
        mass=mass,
        hbar=hbar,
    )

    if energy >= barrier_height:
        raise ValueError(
            "tunnelling decay constant requires "
            "energy below the barrier height."
        )

    return float(
        np.sqrt(
            2.0
            * mass
            * (barrier_height - energy)
        )
        / hbar
    )


def propagation_wave_number(
    energy: float,
    barrier_height: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> float:
    _validate_parameters(
        energy=energy,
        barrier_height=barrier_height,
        mass=mass,
        hbar=hbar,
    )

    if energy <= barrier_height:
        raise ValueError(
            "propagation wave number requires "
            "energy above the barrier height."
        )

    return float(
        np.sqrt(
            2.0
            * mass
            * (energy - barrier_height)
        )
        / hbar
    )


def rectangular_barrier_transmission(
    energy: float,
    barrier_height: float,
    barrier_width: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> BarrierTransmissionResult:
    _validate_parameters(
        energy=energy,
        barrier_height=barrier_height,
        mass=mass,
        hbar=hbar,
    )

    if not np.isfinite(barrier_width):
        raise ValueError(
            "barrier_width must be finite."
        )

    if barrier_width <= 0.0:
        raise ValueError(
            "barrier_width must be positive."
        )

    if np.isclose(
        energy,
        barrier_height,
        rtol=1e-12,
        atol=1e-14,
    ):
        transmission = 1.0 / (
            1.0
            + (
                mass
                * barrier_height
                * barrier_width**2
                / (2.0 * hbar**2)
            )
        )

        regime = "threshold"

    elif energy < barrier_height:
        kappa = tunnelling_decay_constant(
            energy=energy,
            barrier_height=barrier_height,
            mass=mass,
            hbar=hbar,
        )

        denominator = (
            1.0
            + (
                barrier_height**2
                * np.sinh(
                    kappa * barrier_width
                )
                ** 2
                / (
                    4.0
                    * energy
                    * (
                        barrier_height
                        - energy
                    )
                )
            )
        )

        transmission = 1.0 / denominator
        regime = "tunnelling"

    else:
        wave_number = propagation_wave_number(
            energy=energy,
            barrier_height=barrier_height,
            mass=mass,
            hbar=hbar,
        )

        denominator = (
            1.0
            + (
                barrier_height**2
                * np.sin(
                    wave_number
                    * barrier_width
                )
                ** 2
                / (
                    4.0
                    * energy
                    * (
                        energy
                        - barrier_height
                    )
                )
            )
        )

        transmission = 1.0 / denominator
        regime = "above-barrier"

    transmission = float(
        np.clip(
            transmission,
            0.0,
            1.0,
        )
    )

    reflection = float(
        1.0 - transmission
    )

    return BarrierTransmissionResult(
        energy=energy,
        barrier_height=barrier_height,
        barrier_width=barrier_width,
        transmission=transmission,
        reflection=reflection,
        regime=regime,
    )


def transmission_scan(
    energies: ArrayFloat,
    barrier_height: float,
    barrier_width: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> ArrayFloat:
    if energies.ndim != 1:
        raise ValueError(
            "energies must be one-dimensional."
        )

    if energies.size == 0:
        raise ValueError(
            "energies must not be empty."
        )

    if not np.all(
        np.isfinite(energies)
    ):
        raise ValueError(
            "energies must be finite."
        )

    transmissions = [
        rectangular_barrier_transmission(
            energy=float(energy),
            barrier_height=barrier_height,
            barrier_width=barrier_width,
            mass=mass,
            hbar=hbar,
        ).transmission
        for energy in energies
    ]

    return np.asarray(
        transmissions,
        dtype=np.float64,
    )


def _validate_parameters(
    energy: float,
    barrier_height: float,
    mass: float,
    hbar: float,
) -> None:
    values = (
        energy,
        barrier_height,
        mass,
        hbar,
    )

    if not all(
        np.isfinite(value)
        for value in values
    ):
        raise ValueError(
            "physical parameters must be finite."
        )

    if energy <= 0.0:
        raise ValueError(
            "energy must be positive."
        )

    if barrier_height <= 0.0:
        raise ValueError(
            "barrier_height must be positive."
        )

    if mass <= 0.0:
        raise ValueError(
            "mass must be positive."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )