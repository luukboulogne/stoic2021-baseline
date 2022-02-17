from typing import Dict
from pathlib import Path
import SimpleITK
from tensorflow.keras import models
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)

from utils import MultiClassAlgorithm, to_input_format, unpack_single_output, device
from algorithm.preprocess import preprocess


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
        self.model = models.load_model('./algorithm/shallow/')

    def predict(self, *, input_image: SimpleITK.Image) -> Dict:
        # pre-processing
        input_image = preprocess(input_image)
        input_image = np.array([input_image])

        # run model
        predicttions = self.model.predict(input_image)
        covid, severe = predicttions
        prob_covid, prob_severe = covid[0].astype(float)[0], severe[0].astype(float)[0]

        return {
            COVID_OUTPUT_NAME: prob_covid,
            SEVERE_OUTPUT_NAME: prob_severe
        }


if __name__ == "__main__":
    StoicAlgorithm().process()
