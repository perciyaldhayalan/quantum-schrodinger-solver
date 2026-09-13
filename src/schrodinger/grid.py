from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class Grid1D:
    x_min: float
    x_max: float
    points: int
    values: NDArray[np.float64] = field(init=False, repr=False)
    dx: float = field(init=False)

    def __post_init__(self) -> None:
        if not np.isfinite(self.x_min):
            raise ValueError("x_min must be finite.")

        if not np.isfinite(self.x_max):
            raise ValueError("x_max must be finite.")

        if self.x_min >= self.x_max:
            raise ValueError("x_min must be smaller than x_max.")

        if isinstance(self.points, bool) or not isinstance(self.points, int):
            raise TypeError("points must be an integer.")

        if self.points < 3:
            raise ValueError("points must be at least 3.")

        values = np.linspace(
            self.x_min,
            self.x_max,
            self.points,
            dtype=np.float64,
        )

        dx = float(values[1] - values[0])

        object.__setattr__(self, "values", values)
        object.__setattr__(self, "dx", dx)

    @property
    def size(self) -> int:
        return self.points

    @property
    def length(self) -> float:
        return self.x_max - self.x_min

    @property
    def interior(self) -> NDArray[np.float64]:
        return self.values[1:-1]

    @property
    def interior_size(self) -> int:
        return self.points - 2

    @property
    def left_boundary(self) -> float:
        return float(self.values[0])

    @property
    def right_boundary(self) -> float:
        return float(self.values[-1])