from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from schrodinger.analysis.errors import (
    absolute_error,
    relative_error,
)
from schrodinger.grid import Grid1D
from schrodinger.stationary.analytic import (
    infinite_well_energy,
)
from schrodinger.stationary.solver import (
    solve_stationary,
)

ArrayFloat = NDArray[np.float64]
ArrayInt = NDArray[np.int64]


@dataclass(frozen=True, slots=True)
class ConvergenceResult:
    grid_points: ArrayInt
    grid_spacings: ArrayFloat
    numerical_energies: ArrayFloat
    exact_energy: float
    absolute_errors: ArrayFloat
    relative_errors: ArrayFloat
    observed_order: float


def estimate_convergence_order(
    grid_spacings: ArrayFloat,
    errors: ArrayFloat,
) -> float:
    if grid_spacings.ndim != 1:
        raise ValueError(
            "grid_spacings must be one-dimensional."
        )

    if errors.ndim != 1:
        raise ValueError(
            "errors must be one-dimensional."
        )

    if grid_spacings.size != errors.size:
        raise ValueError(
            "grid_spacings and errors must have "
            "the same size."
        )

    if grid_spacings.size < 2:
        raise ValueError(
            "at least two data points are required."
        )

    if not np.all(np.isfinite(grid_spacings)):
        raise ValueError(
            "grid_spacings must be finite."
        )

    if not np.all(np.isfinite(errors)):
        raise ValueError(
            "errors must be finite."
        )

    if np.any(grid_spacings <= 0.0):
        raise ValueError(
            "grid_spacings must be positive."
        )

    if np.any(errors <= 0.0):
        raise ValueError(
            "errors must be positive."
        )

    log_dx = np.log(grid_spacings)
    log_error = np.log(errors)

    coefficients = np.polyfit(
        log_dx,
        log_error,
        deg=1,
    )

    return float(coefficients[0])


def infinite_well_convergence(
    point_counts: ArrayInt,
    quantum_number: int = 1,
    length: float = 1.0,
    hbar: float = 1.0,
    mass: float = 1.0,
) -> ConvergenceResult:
    if point_counts.ndim != 1:
        raise ValueError(
            "point_counts must be one-dimensional."
        )

    if point_counts.size < 2:
        raise ValueError(
            "at least two grid sizes are required."
        )

    if np.any(point_counts < 3):
        raise ValueError(
            "all grid sizes must contain at least 3 points."
        )

    exact = infinite_well_energy(
        quantum_number=quantum_number,
        length=length,
        hbar=hbar,
        mass=mass,
    )

    spacings = np.empty(
        point_counts.size,
        dtype=np.float64,
    )

    numerical_energies = np.empty(
        point_counts.size,
        dtype=np.float64,
    )

    absolute_errors = np.empty(
        point_counts.size,
        dtype=np.float64,
    )

    relative_error_values = np.empty(
        point_counts.size,
        dtype=np.float64,
    )

    for index, points in enumerate(
        point_counts
    ):
        grid = Grid1D(
            0.0,
            length,
            int(points),
        )

        potential = np.zeros(
            grid.interior_size,
            dtype=np.float64,
        )

        solutions = solve_stationary(
            grid=grid,
            potential=potential,
            states=quantum_number,
            hbar=hbar,
            mass=mass,
        )

        numerical = solutions[
            quantum_number - 1
        ].energy

        spacings[index] = grid.dx
        numerical_energies[index] = numerical

        absolute_errors[index] = absolute_error(
            numerical=numerical,
            exact=exact,
        )

        relative_error_values[index] = relative_error(
            numerical=numerical,
            exact=exact,
        )

    observed_order = estimate_convergence_order(
        grid_spacings=spacings,
        errors=absolute_errors,
    )

    return ConvergenceResult(
        grid_points=np.asarray(
            point_counts,
            dtype=np.int64,
        ),
        grid_spacings=spacings,
        numerical_energies=numerical_energies,
        exact_energy=exact,
        absolute_errors=absolute_errors,
        relative_errors=relative_error_values,
        observed_order=observed_order,
    )