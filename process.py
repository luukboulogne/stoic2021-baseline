from typing import Dict
from pathlib import Path
import SimpleITK
import torch

from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)

from utils import MultiClassAlgorithm, to_input_format, unpack_single_output, device
from algorithm.preprocess import preprocess
from algorithm.i3d.i3dpt import I3D


COVID_OUTPUT_NAME = Path("probability-covid-19")
SEVERE_OUTPUT_NAME = Path("probability-severe-covid-19")


class StoicAlgorithm(MultiClassAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
            input_path=Path("/input/images/ct/"),
            output_path=Path("/output/")
        )

        # load model
        self.model = I3D(nr_outputs=2)
        self.model = self.model.to(device)
        self.model.load_state_dict(torch.load('./algorithm/model_covid.pth', map_location=torch.device(device)))
        self.model = self.model.eval()

    def predict(self, *, input_image: SimpleITK.Image) -> Dict:
        # pre-processing
        input_image = preprocess(input_image)
        input_image = to_input_format(input_image)

        # run model
        with torch.no_grad():
            output = torch.sigmoid(self.model(input_image))
        prob_covid, prob_severe = unpack_single_output(output)

        return {
            COVID_OUTPUT_NAME: prob_covid,
            SEVERE_OUTPUT_NAME: prob_severe
        }


if __name__ == "__main__":
    StoicAlgorithm().process()
