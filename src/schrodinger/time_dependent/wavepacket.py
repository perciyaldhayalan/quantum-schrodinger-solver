from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.analysis.normalization import (
    normalize_wavefunction,
    probability_norm,
)
from schrodinger.grid import Grid1D
from schrodinger.stationary.observables import (
    calculate_observables,
)

ArrayComplex = NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class GaussianWavepacketParameters:
    center: float
    sigma: float
    wave_number: float


@dataclass(frozen=True, slots=True)
class WavepacketDiagnostics:
    norm: float
    position: float
    momentum: float
    position_uncertainty: float
    momentum_uncertainty: float
    uncertainty_product: float
    mean_kinetic_energy: float


def gaussian_wavepacket(
    grid: Grid1D,
    center: float,
    sigma: float,
    wave_number: float,
    normalize: bool = True,
) -> ArrayComplex:
    _validate_gaussian_parameters(
        grid=grid,
        center=center,
        sigma=sigma,
        wave_number=wave_number,
    )

    amplitude = (
        1.0
        / (
            2.0
            * np.pi
            * sigma**2
        )
        ** 0.25
    )

    envelope = np.exp(
        -(
            grid.values - center
        )
        ** 2
        / (
            4.0
            * sigma**2
        )
    )

    phase = np.exp(
        1j
        * wave_number
        * grid.values
    )

    wavefunction = np.asarray(
        amplitude
        * envelope
        * phase,
        dtype=np.complex128,
    )

    if normalize:
        wavefunction = np.asarray(
            normalize_wavefunction(
                wavefunction=wavefunction,
                dx=grid.dx,
            ),
            dtype=np.complex128,
        )

    return wavefunction


def gaussian_probability_density(
    wavefunction: ArrayComplex,
) -> NDArray[np.float64]:
    if wavefunction.ndim != 1:
        raise ValueError(
            "wavefunction must be one-dimensional."
        )

    if wavefunction.size == 0:
        raise ValueError(
            "wavefunction must not be empty."
        )

    if not np.all(
        np.isfinite(wavefunction)
    ):
        raise ValueError(
            "wavefunction values must be finite."
        )

    return np.asarray(
        np.abs(wavefunction) ** 2,
        dtype=np.float64,
    )


def mean_kinetic_energy(
    momentum: float,
    momentum_squared: float,
    mass: float = 1.0,
) -> float:
    if not np.isfinite(momentum):
        raise ValueError(
            "momentum must be finite."
        )

    if not np.isfinite(momentum_squared):
        raise ValueError(
            "momentum_squared must be finite."
        )

    if not np.isfinite(mass):
        raise ValueError(
            "mass must be finite."
        )

    if mass <= 0.0:
        raise ValueError(
            "mass must be positive."
        )

    if momentum_squared < 0.0:
        raise ValueError(
            "momentum_squared must be non-negative."
        )

    return float(
        momentum_squared
        / (2.0 * mass)
    )


def analyze_wavepacket(
    wavefunction: ArrayComplex,
    grid: Grid1D,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> WavepacketDiagnostics:
    observables = calculate_observables(
        wavefunction=wavefunction,
        grid=grid,
        hbar=hbar,
    )

    norm = probability_norm(
        wavefunction=wavefunction,
        dx=grid.dx,
    )

    kinetic_energy = mean_kinetic_energy(
        momentum=observables.momentum,
        momentum_squared=(
            observables.momentum_squared
        ),
        mass=mass,
    )

    return WavepacketDiagnostics(
        norm=norm,
        position=observables.position,
        momentum=observables.momentum,
        position_uncertainty=(
            observables.position_uncertainty
        ),
        momentum_uncertainty=(
            observables.momentum_uncertainty
        ),
        uncertainty_product=(
            observables.uncertainty_product
        ),
        mean_kinetic_energy=kinetic_energy,
    )


def _validate_gaussian_parameters(
    grid: Grid1D,
    center: float,
    sigma: float,
    wave_number: float,
) -> None:
    values = (
        center,
        sigma,
        wave_number,
    )

    if not all(
        np.isfinite(value)
        for value in values
    ):
        raise ValueError(
            "wavepacket parameters must be finite."
        )

    if sigma <= 0.0:
        raise ValueError(
            "sigma must be positive."
        )

    if not (
        grid.x_min
        < center
        < grid.x_max
    ):
        raise ValueError(
            "wavepacket center must lie "
            "inside the grid."
        )