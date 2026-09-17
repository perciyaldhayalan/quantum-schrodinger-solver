from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.grid import Grid1D

ArrayComplex = NDArray[np.complex128]
ArrayFloat = NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class MomentumDistribution:
    momentum: ArrayFloat
    probability_density: ArrayFloat
    dp: float


def momentum_distribution(
    wavefunction: ArrayComplex,
    grid: Grid1D,
    hbar: float = 1.0,
) -> MomentumDistribution:
    _validate_inputs(
        wavefunction=wavefunction,
        grid=grid,
        hbar=hbar,
    )

    shifted_wavefunction = np.fft.ifftshift(
        wavefunction
    )

    transform = np.fft.fft(
        shifted_wavefunction
    )

    transform = np.fft.fftshift(
        transform
    )

    wave_numbers = (
        2.0
        * np.pi
        * np.fft.fftshift(
            np.fft.fftfreq(
                grid.size,
                d=grid.dx,
            )
        )
    )

    momentum = (
        hbar
        * wave_numbers
    )

    momentum_wavefunction = (
        grid.dx
        / np.sqrt(
            2.0
            * np.pi
            * hbar
        )
        * transform
    )

    probability_density = np.asarray(
        np.abs(
            momentum_wavefunction
        )
        ** 2,
        dtype=np.float64,
    )

    momentum = np.asarray(
        momentum,
        dtype=np.float64,
    )

    dp = float(
        momentum[1]
        - momentum[0]
    )

    normalization = float(
        np.sum(
            probability_density
        )
        * dp
    )

    if normalization <= 0.0:
        raise ValueError(
            "momentum distribution has "
            "zero probability."
        )

    probability_density = (
        probability_density
        / normalization
    )

    return MomentumDistribution(
        momentum=momentum,
        probability_density=probability_density,
        dp=dp,
    )


def _validate_inputs(
    wavefunction: ArrayComplex,
    grid: Grid1D,
    hbar: float,
) -> None:
    if wavefunction.ndim != 1:
        raise ValueError(
            "wavefunction must be one-dimensional."
        )

    if wavefunction.size != grid.size:
        raise ValueError(
            "wavefunction size must match grid size."
        )

    if not np.all(
        np.isfinite(wavefunction)
    ):
        raise ValueError(
            "wavefunction values must be finite."
        )

    if not np.isfinite(hbar):
        raise ValueError(
            "hbar must be finite."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )