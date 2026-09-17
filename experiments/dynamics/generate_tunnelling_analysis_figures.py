import matplotlib.pyplot as plt
import numpy as np

from schrodinger.analysis.tunnelling_study import (
    run_tunnelling_study,
)
from schrodinger.grid import Grid1D
from schrodinger.time_dependent.wavepacket import (
    gaussian_wavepacket,
)
from schrodinger.visualization.probability import (
    save_figure,
)
from schrodinger.visualization.tunnelling_analysis import (
    plot_log_transmission_vs_width,
    plot_transmission_comparison,
    plot_transmission_vs_height,
    plot_transmission_vs_width,
)


def main() -> None:
    grid = Grid1D(
        -30.0,
        30.0,
        3001,
    )

    wavefunction = gaussian_wavepacket(
        grid=grid,
        center=-10.0,
        sigma=1.5,
        wave_number=2.0,
    )

    dt = 0.001
    steps = 10000

    widths = np.asarray(
        [
            0.5,
            0.75,
            1.0,
            1.25,
            1.5,
        ],
        dtype=np.float64,
    )

    width_heights = np.full(
        widths.shape,
        5.0,
        dtype=np.float64,
    )

    width_result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=width_heights,
        barrier_widths=widths,
        dt=dt,
        steps=steps,
        separation_tolerance=1e-3,
    )

    width_figure = (
        plot_transmission_vs_width(
            widths=widths,
            tdse_transmissions=(
                width_result.tdse_transmissions
            ),
            stationary_transmissions=(
                width_result.stationary_transmissions
            ),
        )
    )

    save_figure(
        figure=width_figure,
        path=(
            "results/figures/tunnelling/"
            "transmission_vs_width.png"
        ),
    )

    log_width_figure = (
        plot_log_transmission_vs_width(
            widths=widths,
            transmissions=(
                width_result.tdse_transmissions
            ),
        )
    )

    save_figure(
        figure=log_width_figure,
        path=(
            "results/figures/tunnelling/"
            "log_transmission_vs_width.png"
        ),
    )

    heights = np.asarray(
        [
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
        ],
        dtype=np.float64,
    )

    height_widths = np.full(
        heights.shape,
        1.0,
        dtype=np.float64,
    )

    height_result = run_tunnelling_study(
        grid=grid,
        initial_wavefunction=wavefunction,
        barrier_heights=heights,
        barrier_widths=height_widths,
        dt=dt,
        steps=steps,
        separation_tolerance=1e-3,
    )

    height_figure = (
        plot_transmission_vs_height(
            heights=heights,
            tdse_transmissions=(
                height_result.tdse_transmissions
            ),
            stationary_transmissions=(
                height_result.stationary_transmissions
            ),
        )
    )

    save_figure(
        figure=height_figure,
        path=(
            "results/figures/tunnelling/"
            "transmission_vs_height.png"
        ),
    )

    stationary_combined = np.concatenate(
        (
            width_result.stationary_transmissions,
            height_result.stationary_transmissions,
        )
    )

    tdse_combined = np.concatenate(
        (
            width_result.tdse_transmissions,
            height_result.tdse_transmissions,
        )
    )

    comparison_figure = (
        plot_transmission_comparison(
            stationary_transmissions=(
                stationary_combined
            ),
            tdse_transmissions=(
                tdse_combined
            ),
        )
    )

    save_figure(
        figure=comparison_figure,
        path=(
            "results/figures/validation/"
            "tdse_vs_stationary_transmission.png"
        ),
    )

    plt.close(
        width_figure
    )

    plt.close(
        log_width_figure
    )

    plt.close(
        height_figure
    )

    plt.close(
        comparison_figure
    )

    print(
        "Quantitative tunnelling figures "
        "generated successfully."
    )

    print(
        f"Maximum width-scan disagreement: "
        f"{np.max(width_result.agreement_errors):.8f}"
    )

    print(
        f"Maximum height-scan disagreement: "
        f"{np.max(height_result.agreement_errors):.8f}"
    )


if __name__ == "__main__":
    main()