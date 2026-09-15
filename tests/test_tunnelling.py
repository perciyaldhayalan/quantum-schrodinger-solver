import numpy as np
import pytest

from schrodinger.analysis.tunnelling import (
    propagation_wave_number,
    rectangular_barrier_transmission,
    transmission_scan,
    tunnelling_decay_constant,
)


def test_tunnelling_decay_constant() -> None:
    result = tunnelling_decay_constant(
        energy=2.0,
        barrier_height=5.0,
        mass=1.0,
        hbar=1.0,
    )

    expected = np.sqrt(6.0)

    assert result == pytest.approx(
        expected
    )


def test_propagation_wave_number() -> None:
    result = propagation_wave_number(
        energy=8.0,
        barrier_height=5.0,
        mass=1.0,
        hbar=1.0,
    )

    expected = np.sqrt(6.0)

    assert result == pytest.approx(
        expected
    )


def test_sub_barrier_transmission_is_nonzero() -> None:
    result = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    assert result.regime == "tunnelling"
    assert 0.0 < result.transmission < 1.0


def test_probability_is_conserved() -> None:
    result = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    assert (
        result.transmission
        + result.reflection
    ) == pytest.approx(1.0)


def test_wider_barrier_reduces_tunnelling() -> None:
    narrow = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=5.0,
        barrier_width=0.5,
    )

    medium = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    wide = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=5.0,
        barrier_width=1.5,
    )

    assert (
        narrow.transmission
        > medium.transmission
        > wide.transmission
    )


def test_higher_barrier_reduces_tunnelling() -> None:
    low = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=3.0,
        barrier_width=1.0,
    )

    medium = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    high = rectangular_barrier_transmission(
        energy=2.0,
        barrier_height=8.0,
        barrier_width=1.0,
    )

    assert (
        low.transmission
        > medium.transmission
        > high.transmission
    )


def test_above_barrier_regime() -> None:
    result = rectangular_barrier_transmission(
        energy=8.0,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    assert result.regime == "above-barrier"
    assert 0.0 <= result.transmission <= 1.0
    assert 0.0 <= result.reflection <= 1.0


def test_threshold_regime() -> None:
    result = rectangular_barrier_transmission(
        energy=5.0,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    assert result.regime == "threshold"
    assert 0.0 < result.transmission < 1.0


def test_transmission_scan() -> None:
    energies = np.asarray(
        [
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
        ],
        dtype=np.float64,
    )

    result = transmission_scan(
        energies=energies,
        barrier_height=5.0,
        barrier_width=1.0,
    )

    assert result.shape == energies.shape
    assert np.all(result >= 0.0)
    assert np.all(result <= 1.0)


def test_invalid_energy_rejected() -> None:
    with pytest.raises(ValueError):
        rectangular_barrier_transmission(
            energy=0.0,
            barrier_height=5.0,
            barrier_width=1.0,
        )


def test_invalid_barrier_width_rejected() -> None:
    with pytest.raises(ValueError):
        rectangular_barrier_transmission(
            energy=2.0,
            barrier_height=5.0,
            barrier_width=0.0,
        )


def test_decay_constant_rejects_above_barrier_energy() -> None:
    with pytest.raises(ValueError):
        tunnelling_decay_constant(
            energy=6.0,
            barrier_height=5.0,
        )


def test_propagation_wave_number_rejects_sub_barrier_energy() -> None:
    with pytest.raises(ValueError):
        propagation_wave_number(
            energy=2.0,
            barrier_height=5.0,
        )