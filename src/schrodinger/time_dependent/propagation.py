from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.grid import Grid1D
from schrodinger.stationary.observables import (
    calculate_observables,
)
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)

ArrayComplex = NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class PropagationSnapshot:
    step: int
    time: float
    wavefunction: ArrayComplex
    norm: float
    position: float
    momentum: float
    position_uncertainty: float


def free_particle_expected_position(
    initial_position: float,
    wave_number: float,
    time: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> float:
    _validate_free_particle_parameters(
        wave_number=wave_number,
        time=time,
        mass=mass,
        hbar=hbar,
    )

    if not np.isfinite(initial_position):
        raise ValueError(
            "initial_position must be finite."
        )

    velocity = (
        hbar
        * wave_number
        / mass
    )

    return float(
        initial_position
        + velocity
        * time
    )


def free_particle_expected_width(
    initial_sigma: float,
    time: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> float:
    if not np.isfinite(initial_sigma):
        raise ValueError(
            "initial_sigma must be finite."
        )

    if initial_sigma <= 0.0:
        raise ValueError(
            "initial_sigma must be positive."
        )

    _validate_free_particle_parameters(
        wave_number=0.0,
        time=time,
        mass=mass,
        hbar=hbar,
    )

    spreading_term = (
        hbar
        * time
        / (
            2.0
            * mass
            * initial_sigma**2
        )
    )

    return float(
        initial_sigma
        * np.sqrt(
            1.0
            + spreading_term**2
        )
    )


def free_particle_expected_momentum(
    wave_number: float,
    hbar: float = 1.0,
) -> float:
    if not np.isfinite(wave_number):
        raise ValueError(
            "wave_number must be finite."
        )

    if not np.isfinite(hbar):
        raise ValueError(
            "hbar must be finite."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )

    return float(
        hbar
        * wave_number
    )


def create_snapshot(
    wavefunction: ArrayComplex,
    grid: Grid1D,
    step: int,
    dt: float,
    hbar: float = 1.0,
) -> PropagationSnapshot:
    if isinstance(step, bool):
        raise TypeError(
            "step must be an integer."
        )

    if not isinstance(
        step,
        (int, np.integer),
    ):
        raise TypeError(
            "step must be an integer."
        )

    if step < 0:
        raise ValueError(
            "step must be non-negative."
        )

    if not np.isfinite(dt):
        raise ValueError(
            "dt must be finite."
        )

    if dt <= 0.0:
        raise ValueError(
            "dt must be positive."
        )

    observables = calculate_observables(
        wavefunction=wavefunction,
        grid=grid,
        hbar=hbar,
    )

    norm = float(
        np.sum(
            np.abs(wavefunction) ** 2
        )
        * grid.dx
    )

    return PropagationSnapshot(
        step=int(step),
        time=float(step * dt),
        wavefunction=np.asarray(
            wavefunction,
            dtype=np.complex128,
        ).copy(),
        norm=norm,
        position=observables.position,
        momentum=observables.momentum,
        position_uncertainty=(
            observables.position_uncertainty
        ),
    )


def propagate_with_snapshots(
    propagator: CrankNicolsonPropagator,
    wavefunction: ArrayComplex,
    steps: int,
    snapshot_interval: int,
) -> list[PropagationSnapshot]:
    if isinstance(steps, bool):
        raise TypeError(
            "steps must be an integer."
        )

    if not isinstance(
        steps,
        (int, np.integer),
    ):
        raise TypeError(
            "steps must be an integer."
        )

    if steps < 0:
        raise ValueError(
            "steps must be non-negative."
        )

    if isinstance(snapshot_interval, bool):
        raise TypeError(
            "snapshot_interval must be an integer."
        )

    if not isinstance(
        snapshot_interval,
        (int, np.integer),
    ):
        raise TypeError(
            "snapshot_interval must be an integer."
        )

    if snapshot_interval <= 0:
        raise ValueError(
            "snapshot_interval must be positive."
        )

    state = np.asarray(
        wavefunction,
        dtype=np.complex128,
    ).copy()

    snapshots = [
        create_snapshot(
            wavefunction=state,
            grid=propagator.grid,
            step=0,
            dt=propagator.dt,
            hbar=propagator.hbar,
        )
    ]

    for step in range(
        1,
        int(steps) + 1,
    ):
        state = propagator.step(
            wavefunction=state
        )

        if (
            step % snapshot_interval == 0
            or step == steps
        ):
            snapshots.append(
                create_snapshot(
                    wavefunction=state,
                    grid=propagator.grid,
                    step=step,
                    dt=propagator.dt,
                    hbar=propagator.hbar,
                )
            )

    return snapshots


def _validate_free_particle_parameters(
    wave_number: float,
    time: float,
    mass: float,
    hbar: float,
) -> None:
    values = (
        wave_number,
        time,
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

    if time < 0.0:
        raise ValueError(
            "time must be non-negative."
        )

    if mass <= 0.0:
        raise ValueError(
            "mass must be positive."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )