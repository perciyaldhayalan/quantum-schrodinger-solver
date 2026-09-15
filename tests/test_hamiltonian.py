import numpy as np
import pytest
from scipy.sparse import csr_matrix

from schrodinger.grid import Grid1D
from schrodinger.hamiltonian import (
    build_hamiltonian,
    is_hermitian,
    kinetic_energy_operator,
    potential_energy_operator,
)


def test_kinetic_operator_shape() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    kinetic = kinetic_energy_operator(grid)

    assert kinetic.shape == (3, 3)


def test_kinetic_operator_values() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    kinetic = kinetic_energy_operator(
        grid=grid,
        hbar=1.0,
        mass=1.0,
    )

    expected = np.array(
        [
            [4.0, -2.0, 0.0],
            [-2.0, 4.0, -2.0],
            [0.0, -2.0, 4.0],
        ],
        dtype=np.float64,
    )

    np.testing.assert_allclose(
        kinetic.toarray(),
        expected,
    )


def test_potential_operator() -> None:
    potential = np.array(
        [1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    operator = potential_energy_operator(potential)

    expected = np.diag(
        [1.0, 2.0, 3.0],
    )

    np.testing.assert_allclose(
        operator.toarray(),
        expected,
    )


def test_build_free_particle_hamiltonian() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    hamiltonian = build_hamiltonian(
        grid=grid,
        potential=potential,
    )

    kinetic = kinetic_energy_operator(grid)

    np.testing.assert_allclose(
        hamiltonian.toarray(),
        kinetic.toarray(),
    )


def test_build_hamiltonian_with_potential() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    potential = np.array(
        [1.0, 2.0, 3.0],
        dtype=np.float64,
    )

    hamiltonian = build_hamiltonian(
        grid=grid,
        potential=potential,
    )

    expected = np.array(
        [
            [5.0, -2.0, 0.0],
            [-2.0, 6.0, -2.0],
            [0.0, -2.0, 7.0],
        ],
        dtype=np.float64,
    )

    np.testing.assert_allclose(
        hamiltonian.toarray(),
        expected,
    )


def test_kinetic_operator_is_sparse() -> None:
    grid = Grid1D(-5.0, 5.0, 101)

    kinetic = kinetic_energy_operator(grid)

    assert isinstance(kinetic, csr_matrix)


def test_hamiltonian_is_sparse() -> None:
    grid = Grid1D(-5.0, 5.0, 101)

    potential = np.zeros(
        grid.interior_size,
        dtype=np.float64,
    )

    hamiltonian = build_hamiltonian(
        grid=grid,
        potential=potential,
    )

    assert isinstance(hamiltonian, csr_matrix)


def test_kinetic_operator_is_hermitian() -> None:
    grid = Grid1D(-5.0, 5.0, 101)

    kinetic = kinetic_energy_operator(grid)

    assert is_hermitian(kinetic)


def test_hamiltonian_is_hermitian() -> None:
    grid = Grid1D(-5.0, 5.0, 101)

    potential = 0.5 * grid.interior**2

    hamiltonian = build_hamiltonian(
        grid=grid,
        potential=potential,
    )

    assert is_hermitian(hamiltonian)


def test_non_hermitian_matrix() -> None:
    matrix = csr_matrix(
        np.array(
            [
                [1.0, 2.0],
                [0.0, 1.0],
            ],
            dtype=np.float64,
        )
    )

    assert not is_hermitian(matrix)


def test_build_hamiltonian_rejects_wrong_potential_size() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    potential = np.zeros(
        5,
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="potential size must match",
    ):
        build_hamiltonian(
            grid=grid,
            potential=potential,
        )


def test_potential_operator_rejects_non_finite_values() -> None:
    potential = np.array(
        [0.0, np.inf, 1.0],
        dtype=np.float64,
    )

    with pytest.raises(
        ValueError,
        match="potential values must be finite",
    ):
        potential_energy_operator(potential)


def test_kinetic_operator_rejects_zero_mass() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    with pytest.raises(
        ValueError,
        match="mass must be positive",
    ):
        kinetic_energy_operator(
            grid=grid,
            mass=0.0,
        )


def test_kinetic_operator_rejects_negative_mass() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    with pytest.raises(
        ValueError,
        match="mass must be positive",
    ):
        kinetic_energy_operator(
            grid=grid,
            mass=-1.0,
        )


def test_kinetic_operator_rejects_zero_hbar() -> None:
    grid = Grid1D(-1.0, 1.0, 5)

    with pytest.raises(
        ValueError,
        match="hbar must be positive",
    ):
        kinetic_energy_operator(
            grid=grid,
            hbar=0.0,
        )