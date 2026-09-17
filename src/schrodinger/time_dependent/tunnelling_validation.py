from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.analysis.tunnelling import (
    rectangular_barrier_transmission,
)
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.momentum_space import (
    momentum_distribution,
)

ArrayComplex = NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class PacketTransmissionPrediction:
    transmission: float
    positive_momentum_probability: float


def packet_averaged_transmission(
    wavefunction: ArrayComplex,
    grid: Grid1D,
    barrier_height: float,
    barrier_width: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> PacketTransmissionPrediction:
    if not np.isfinite(barrier_height):
        raise ValueError(
            "barrier_height must be finite."
        )

    if barrier_height < 0.0:
        raise ValueError(
            "barrier_height must be non-negative."
        )

    if not np.isfinite(barrier_width):
        raise ValueError(
            "barrier_width must be finite."
        )

    if barrier_width <= 0.0:
        raise ValueError(
            "barrier_width must be positive."
        )

    if not np.isfinite(mass):
        raise ValueError(
            "mass must be finite."
        )

    if mass <= 0.0:
        raise ValueError(
            "mass must be positive."
        )

    distribution = momentum_distribution(
        wavefunction=wavefunction,
        grid=grid,
        hbar=hbar,
    )

    positive_mask = (
        distribution.momentum > 0.0
    )

    positive_probability = float(
        np.sum(
            distribution.probability_density[
                positive_mask
            ]
        )
        * distribution.dp
    )

    if positive_probability <= 0.0:
        raise ValueError(
            "wavepacket contains no "
            "positive-momentum probability."
        )

    weighted_transmission = 0.0

    momenta = distribution.momentum[
        positive_mask
    ]

    probabilities = (
        distribution.probability_density[
            positive_mask
        ]
    )

    for momentum, probability in zip(
        momenta,
        probabilities,
        strict=True,
    ):
        energy = (
            momentum**2
            / (
                2.0
                * mass
            )
        )

        if energy <= 0.0:
            continue

        result = (
            rectangular_barrier_transmission(
                energy=float(energy),
                barrier_height=barrier_height,
                barrier_width=barrier_width,
                mass=mass,
                hbar=hbar,
            )
        )

        weighted_transmission += (
            result.transmission
            * float(probability)
            * distribution.dp
        )

    weighted_transmission /= (
        positive_probability
    )

    return PacketTransmissionPrediction(
        transmission=float(
            weighted_transmission
        ),
        positive_momentum_probability=(
            positive_probability
        ),
    )