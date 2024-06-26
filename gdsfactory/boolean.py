from __future__ import annotations

from typing import TYPE_CHECKING

import kfactory as kf

from gdsfactory.component import Component, boolean_operations

if TYPE_CHECKING:
    from gdsfactory.typings import ComponentOrReference, LayerSpec


@kf.cell
def boolean(
    A: ComponentOrReference,
    B: ComponentOrReference,
    operation: str,
    layer1: LayerSpec | None = None,
    layer2: LayerSpec | None = None,
    layer: LayerSpec = (1, 0),
) -> Component:
    """Performs boolean operations between 2 Component/Reference/list objects.

    ``operation`` should be one of {'not', 'and', 'or', 'xor', 'A-B', 'B-A', 'A+B'}.
    Note that 'A+B' is equivalent to 'or', 'A-B' is equivalent to 'not', and
    'B-A' is equivalent to 'not' with the operands switched

    You can also use gdsfactory.drc.boolean_klayout

    Args:
        A: Component(/Reference) or list of Component(/References).
        B: Component(/Reference) or list of Component(/References).
        operation: {'not', 'and', 'or', 'xor', 'A-B', 'B-A', 'A+B'}.
        layer1: Specific layer to get polygons.
        layer2: Specific layer to get polygons.
        layer: Specific layer to put polygon geometry on.

    Returns: Component with polygon(s) of the boolean operations between
      the 2 input Components performed.

    Notes
    -----
    - 'A+B' is equivalent to 'or'.
    - 'A-B' is equivalent to 'not'.
    - 'B-A' is equivalent to 'not' with the operands switched.

    .. plot::
      :include-source:

      import gdsfactory as gf

      c1 = gf.components.circle(radius=10).ref()
      c2 = gf.components.circle(radius=9).ref()
      c2.movex(5)

      c = gf.boolean(c1, c2, operation="xor")
      c.plot()

    """
    from gdsfactory import get_layer

    if operation not in boolean_operations:
        raise ValueError(
            f"Boolean operation {operation} not supported. Choose from {list(boolean_operations.keys())}"
        )

    c = Component()
    layer1 = layer1 or layer
    layer2 = layer2 or layer

    layer_index1 = get_layer(layer1)
    layer_index2 = get_layer(layer2)
    layer_index = get_layer(layer)

    a = A._kdb_cell if isinstance(A, Component) else A.cell
    b = B._kdb_cell if isinstance(B, Component) else B.cell

    for r1, r2 in zip(
        a.begin_shapes_rec(layer_index1),
        b.begin_shapes_rec(layer_index2),
    ):
        r1 = kf.kdb.Region(r1)
        r2 = kf.kdb.Region(r2)
        if isinstance(A, kf.Instance):
            r1.transform(A.cplx_trans)
        if isinstance(B, kf.Instance):
            r1.transform(B.cplx_trans)
        f = boolean_operations[operation]
        r = f(r1, r2)
        r = c.shapes(layer_index).insert(r)

    return c


if __name__ == "__main__":
    import gdsfactory as gf

    # c = gf.Component()
    # e2 = c << gf.components.ellipse(radii=(10, 6))
    # e3 = c << gf.components.ellipse(radii=(10, 4))
    # e3.d.movex(5)
    # c = boolean(A=e2, B=e3, operation="and")

    core = gf.c.coupler()
    clad = gf.c.bbox(core, layer=(2, 0))
    c = boolean(clad, core, operation="not", layer=(3, 0), layer1=(2, 0), layer2=(1, 0))
    c.show()
