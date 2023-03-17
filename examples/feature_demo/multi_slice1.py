"""
Volume and Mesh Slicing 1
=========================

Slice a volume and a mesh through the three primary planes (XY, XZ, YZ).
This example uses a mesh object with custom texture coordinates. This
is a generic approach. See multi_slice2.py for a simpler way.
"""
# sphinx_gallery_pygfx_render = True

from time import time

import imageio.v3 as iio
import numpy as np
from wgpu.gui.auto import WgpuCanvas, run
import pygfx as gfx


canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)
scene = gfx.Scene()

dark_gray = np.array((169, 167, 168, 255)) / 255
light_gray = np.array((100, 100, 100, 255)) / 255
background = gfx.Background(None, gfx.BackgroundMaterial(light_gray, dark_gray))
scene.add(background)

scene.add(gfx.AxesHelper(size=50))

vol = iio.imread("imageio:stent.npz").astype("float32") / 2000
tex = gfx.Texture(vol, dim=3)
view = tex.get_view(filter="linear")
material = gfx.MeshBasicMaterial(map=view)

planes = []
texcoords = {
    0: [[0.5, 0, 0], [0.5, 1, 0], [0.5, 0, 1], [0.5, 1, 1]],
    1: [[0, 0.5, 0], [1, 0.5, 0], [0, 0.5, 1], [1, 0.5, 1]],
    2: [[0, 0, 0.5], [1, 0, 0.5], [0, 1, 0.5], [1, 1, 0.5]],
}
sizes = {
    0: (vol.shape[1], vol.shape[0]),  # YZ plane
    1: (vol.shape[2], vol.shape[0]),  # XZ plane
    2: (vol.shape[2], vol.shape[1]),  # XY plane (default)
}
for axis in [0, 1, 2]:
    geometry = gfx.plane_geometry(*sizes[axis], 1, 1)
    geometry.texcoords = gfx.Buffer(np.array(texcoords[axis], dtype="f4"))
    plane = gfx.Mesh(geometry, material)
    planes.append(plane)
    scene.add(plane)

    if axis == 0:  # YZ plane
        plane.rotation.set_from_euler(gfx.linalg.Euler(0.5 * np.pi, 0.5 * np.pi))
    elif axis == 1:  # XZ plane
        plane.rotation.set_from_euler(gfx.linalg.Euler(0.5 * np.pi))
    # else: XY plane

# camera = gfx.PerspectiveCamera(70, 16 / 9)
camera = gfx.PerspectiveCamera(0)
camera.up = 0, 0, 1
camera.position.set(200, 200, 200)
camera.show_pos((0, 0, 0))

controller = gfx.OrbitController(camera, register_events=renderer)


def animate():
    t = np.cos(time() / 2)
    plane = planes[2]
    plane.position.z = t * vol.shape[0] * 0.5
    plane.geometry.texcoords.data[:, 2] = (t + 1) / 2
    plane.geometry.texcoords.update_range(0, plane.geometry.texcoords.nitems)

    renderer.render(scene, camera)
    canvas.request_draw()


if __name__ == "__main__":
    canvas.request_draw(animate)
    run()
