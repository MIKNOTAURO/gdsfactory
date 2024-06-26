from __future__ import annotations

import gdsfactory as gf


@gf.cell
def spiral_gc(**kwargs):
    c = gf.c.spiral(**kwargs)
    c.info["doe"] = "spirals_sc"
    c.info["measurement"] = "optical_loopback4"
    c.info["analysis"] = "optical_loopback4_spirals"
    return c


@gf.cell
def mzi_gc(length_x=10, **kwargs):
    c = gf.components.mzi2x2_2x2_phase_shifter(length_x=length_x, **kwargs)
    c.info["doe"] = "mzi"
    c.info["measurement"] = "optical_loopback4"
    c.info["analysis"] = "optical_loopback4_mzi"
    return c


def sample_reticle() -> gf.Component:
    """Returns MZI with TE grating couplers."""
    mzis = [mzi_gc(length_x=lengths) for lengths in [100, 200, 300]]
    rings = [
        gf.components.ring_single_heater(length_x=length_x) for length_x in [10, 20, 30]
    ]

    spirals = [spiral_gc(length=length) for length in [20e3, 40e3, 60e3]]

    # rings_te = [
    #     gf.components.add_fiber_array_optical_south_electrical_north(
    #         ring,
    #         electrical_port_names=["l_e2", "r_e2"],
    #     )
    #     for ring in rings
    # ]

    components = mzis + rings + spirals

    c = gf.pack(components)
    if len(c) > 1:
        c = gf.pack(c)[0]
    return c[0]


if __name__ == "__main__":
    c = sample_reticle()
    gdspath = c.write_gds("mask.gds")
    # csvpath = write_labels(gdspath, prefixes=[""], layer_label="TEXT")
    # df = pd.read_csv(csvpath)
    # print(df)
    c.show()
