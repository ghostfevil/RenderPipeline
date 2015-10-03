
from panda3d.core import Texture

from ..RenderStage import RenderStage
from ..Util.Image import Image


class FlagUsedCellsStage(RenderStage):

    """ This stage flags all used cells based on the depth buffer """

    def __init__(self, pipeline):
        RenderStage.__init__(self, "FlagUsedCellsStage", pipeline)
        self._tile_amount = None

    def set_tile_amount(self, tile_amount):
        """ Sets the cell tile size """
        self._tile_amount = tile_amount

    def get_input_pipes(self):
        return ["GBufferDepth"]

    def get_produced_pipes(self):
        return {"FlaggedCells": self._cell_grid_flags.tex}

    def create(self):

        self._target = self._create_target("FlagUsedCells")
        # self._target.addColorTexture()
        self._target.prepareOffscreenBuffer()

        self._cell_grid_flags = Image.create_2d_array("CellGridFlags",
            self._tile_amount.x, self._tile_amount.y,
            self._pipeline.settings.lightGridSlices,
            Texture.T_float, Texture.F_r16)
        self._cell_grid_flags.set_clear_color(0)

        self._target.setShaderInput("cellGridFlags", self._cell_grid_flags.tex)

    def update(self):
        self._cell_grid_flags.clear_image()

    def set_shaders(self):
        self._target.setShader(self._load_shader("Stages/FlagUsedCells.fragment"))

    def resize(self):
        RenderStage.resize(self)
        self.debug("Resizing pass")

    def cleanup(self):
        RenderStage.cleanup(self)
        self.debug("Cleanup pass")
