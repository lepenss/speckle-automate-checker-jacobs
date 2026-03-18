"""Geometry utilities for Speckle objects."""

from specklepy.objects.base import Base


def get_mesh_centroid(obj: Base) -> tuple[float, float, float]:
    display_value = getattr(obj, "displayValue", None)
    if not display_value:
        return (0.0, 0.0, 0.0)
    first = display_value[0]
    units = getattr(first, "units", None)
    
    apply_inch_conversion = units == "in"
    factor = 0.0254 if apply_inch_conversion else 0.001

    if getattr(first, "speckle_type", None) == "Speckle.Core.Models.Instances.InstanceProxy":
        x = first.transform[3]
        y = first.transform[7]
        
        return (x * factor, y * factor, 0)

    sum_x = 0.0
    sum_y = 0.0
    sum_z = 0.0
    num_vertices = 0
    for display_value_item in display_value:
        if getattr(display_value_item, "speckle_type", None) == "Objects.Geometry.Mesh":
            vertices = getattr(display_value_item, "vertices", None) or []
            local_count = len(vertices) // 3
            if local_count:
                num_vertices += local_count
                sum_x += sum(vertices[i * 3] for i in range(local_count))
                sum_y += sum(vertices[i * 3 + 1] for i in range(local_count))
                sum_z += sum(vertices[i * 3 + 2] for i in range(local_count))
        elif getattr(display_value_item, "speckle_type", None) == "Objects.Geometry.Line":
            line = display_value_item
            num_vertices += 1
            sum_x += (line.start.x + line.end.x) / 2
            sum_y += (line.start.y + line.end.y) / 2
            sum_z += (line.start.z + line.end.z) / 2

    if num_vertices == 0:
        return (0.0, 0.0, 0.0)

    return (factor * sum_x / num_vertices, factor * sum_y / num_vertices, factor * sum_z / num_vertices)
