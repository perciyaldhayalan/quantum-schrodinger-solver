from dataclasses import dataclass

from scipy.constants import electron_volt, hbar, m_e, nano


@dataclass(frozen=True, slots=True)
class NaturalUnits:
    hbar: float = 1.0
    mass: float = 1.0


NATURAL_UNITS = NaturalUnits()

HBAR_SI: float = hbar
ELECTRON_MASS_SI: float = m_e
ELECTRON_VOLT_JOULE: float = electron_volt
NANOMETER_METER: float = nano