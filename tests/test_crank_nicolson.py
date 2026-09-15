import numpy as np
import pytest
from numpy.typing import NDArray

from schrodinger.analysis.normalization import (
    probability_norm,
)
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.crank_nicolson import (
    CrankNicolsonPropagator,
)
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)

ArrayComplex = NDArray[np.complex128]


@pytest.fixture
def grid() -> Grid1D:
    return Grid1D(
        -30.0,
        30.0,
        3001,
    )


@pytest.fixture
def potential(
    grid: Grid1D,
) -> NDArray[np.float64]:
    return np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )


@pytest.fixture
def wavepacket(
    grid: Grid1D,
) -> ArrayComplex:
    return gaussian_wavepacket(
        grid=grid,
        center=-10.0,
        sigma=1.5,
        wave_number=2.0,
    )


@pytest.fixture
def propagator(
    grid: Grid1D,
    potential: NDArray[np.float64],
) -> CrankNicolsonPropagator:
    return CrankNicolsonPropagator(
        grid=grid,
        potential=potential,
        dt=0.001,
        mass=1.0,
        hbar=1.0,
    )


def test_single_step_preserves_shape(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    result = propagator.step(
        wavefunction=wavepacket
    )

    assert result.shape == (
        wavepacket.shape
    )

    assert np.iscomplexobj(
        result
    )


def test_single_step_changes_wavefunction(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    result = propagator.step(
        wavefunction=wavepacket
    )

    assert not np.allclose(
        result,
        wavepacket,
        rtol=1e-12,
        atol=1e-12,
    )


def test_dirichlet_boundaries_are_zero(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    result = propagator.step(
        wavefunction=wavepacket
    )

    assert result[0] == 0.0
    assert result[-1] == 0.0


def test_single_step_conserves_probability(
    grid: Grid1D,
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    initial_norm = probability_norm(
        wavefunction=wavepacket,
        dx=grid.dx,
    )

    result = propagator.step(
        wavefunction=wavepacket
    )

    final_norm = probability_norm(
        wavefunction=result,
        dx=grid.dx,
    )

    assert final_norm == pytest.approx(
        initial_norm,
        abs=1e-10,
    )


def test_many_steps_conserve_probability(
    grid: Grid1D,
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    initial_norm = probability_norm(
        wavefunction=wavepacket,
        dx=grid.dx,
    )

    result = propagator.propagate(
        wavefunction=wavepacket,
        steps=500,
    )

    final_norm = probability_norm(
        wavefunction=result,
        dx=grid.dx,
    )

    assert final_norm == pytest.approx(
        initial_norm,
        abs=1e-9,
    )


def test_zero_steps_returns_same_state(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    result = propagator.propagate(
        wavefunction=wavepacket,
        steps=0,
    )

    assert np.array_equal(
        result,
        wavepacket,
    )

    assert result is not wavepacket


def test_input_wavefunction_is_not_modified(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    original = wavepacket.copy()

    propagator.step(
        wavefunction=wavepacket
    )

    assert np.array_equal(
        wavepacket,
        original,
    )


def test_invalid_potential_size_rejected(
    grid: Grid1D,
) -> None:
    potential = np.zeros(
        grid.interior_size - 1,
        dtype=np.float64,
    )

    with pytest.raises(ValueError):
        CrankNicolsonPropagator(
            grid=grid,
            potential=potential,
            dt=0.001,
        )


def test_invalid_dt_rejected(
    grid: Grid1D,
    potential: NDArray[np.float64],
) -> None:
    with pytest.raises(ValueError):
        CrankNicolsonPropagator(
            grid=grid,
            potential=potential,
            dt=0.0,
        )


def test_negative_steps_rejected(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    with pytest.raises(ValueError):
        propagator.propagate(
            wavefunction=wavepacket,
            steps=-1,
        )


def test_non_integer_steps_rejected(
    propagator: CrankNicolsonPropagator,
    wavepacket: ArrayComplex,
) -> None:
    with pytest.raises(TypeError):
        propagator.propagate(
            wavefunction=wavepacket,
            steps=1.5,  # type: ignore[arg-type]
        )


def test_invalid_wavefunction_size_rejected(
    propagator: CrankNicolsonPropagator,
) -> None:
    invalid = np.zeros(
        100,
        dtype=np.complex128,
    )

    with pytest.raises(ValueError):
        propagator.step(
            wavefunction=invalid
        )