from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy.optimize import brentq

Parity = Literal["even", "odd"]


@dataclass(frozen=True, slots=True)
class FiniteWellReferenceState:
    index: int
    parity: Parity
    z: float
    energy: float


def finite_well_strength(
    half_width: float,
    depth: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> float:
    values = (
        half_width,
        depth,
        mass,
        hbar,
    )

    if not all(np.isfinite(value) for value in values):
        raise ValueError(
            "finite-well parameters must be finite."
        )

    if half_width <= 0.0:
        raise ValueError(
            "half_width must be positive."
        )

    if depth <= 0.0:
        raise ValueError(
            "depth must be positive."
        )

    if mass <= 0.0:
        raise ValueError(
            "mass must be positive."
        )

    if hbar <= 0.0:
        raise ValueError(
            "hbar must be positive."
        )

    return float(
        half_width
        * np.sqrt(2.0 * mass * depth)
        / hbar
    )


def _radical(
    z: float,
    z0: float,
) -> float:
    value = z0**2 - z**2
    return float(
        np.sqrt(max(value, 0.0))
    )


def _even_equation(
    z: float,
    z0: float,
) -> float:
    return float(
        z * np.tan(z)
        - _radical(z=z, z0=z0)
    )


def _odd_equation(
    z: float,
    z0: float,
) -> float:
    return float(
        -z / np.tan(z)
        - _radical(z=z, z0=z0)
    )


def _root_intervals(
    z0: float,
    epsilon: float = 1e-10,
) -> list[tuple[Parity, float, float]]:
    if not np.isfinite(z0):
        raise ValueError("z0 must be finite.")

    if z0 <= 0.0:
        raise ValueError("z0 must be positive.")

    if not np.isfinite(epsilon):
        raise ValueError(
            "epsilon must be finite."
        )

    if epsilon <= 0.0:
        raise ValueError(
            "epsilon must be positive."
        )

    intervals: list[
        tuple[Parity, float, float]
    ] = []

    state_number = 0

    while True:
        lower = (
            state_number
            * np.pi
            / 2.0
        )

        upper = (
            (state_number + 1)
            * np.pi
            / 2.0
        )

        if lower >= z0:
            break

        left = max(
            lower + epsilon,
            epsilon,
        )

        right = min(
            upper - epsilon,
            z0 - epsilon,
        )

        if left < right:
            parity: Parity = (
                "even"
                if state_number % 2 == 0
                else "odd"
            )

            intervals.append(
                (
                    parity,
                    float(left),
                    float(right),
                )
            )

        state_number += 1

    return intervals


def finite_well_reference_states(
    half_width: float,
    depth: float,
    mass: float = 1.0,
    hbar: float = 1.0,
) -> tuple[FiniteWellReferenceState, ...]:
    z0 = finite_well_strength(
        half_width=half_width,
        depth=depth,
        mass=mass,
        hbar=hbar,
    )

    roots: list[
        tuple[Parity, float]
    ] = []

    for parity, left, right in _root_intervals(
        z0=z0,
    ):
        equation = (
            _even_equation
            if parity == "even"
            else _odd_equation
        )

        left_value = equation(
            left,
            z0,
        )

        right_value = equation(
            right,
            z0,
        )

        if not (
            np.isfinite(left_value)
            and np.isfinite(right_value)
        ):
            continue

        if left_value * right_value > 0.0:
            continue

        root = brentq(
            equation,
            left,
            right,
            args=(z0,),
            xtol=1e-13,
            rtol=1e-13,
            maxiter=200,
        )

        roots.append(
            (
                parity,
                float(root),
            )
        )

    states: list[
        FiniteWellReferenceState
    ] = []

    for index, (parity, z) in enumerate(roots):
        energy = (
            -depth
            + (
                hbar**2
                * z**2
                / (
                    2.0
                    * mass
                    * half_width**2
                )
            )
        )

        states.append(
            FiniteWellReferenceState(
                index=index,
                parity=parity,
                z=z,
                energy=float(energy),
            )
        )

    return tuple(states)