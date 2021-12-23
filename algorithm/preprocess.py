import numpy as np
import SimpleITK as sitk
from typing import Iterable


def clip_and_normalize(np_image: np.ndarray,
                       clip_min: int = -1100,
                       clip_max: int = 300
                       ) -> np.ndarray:
    np_image = np.clip(np_image, clip_min, clip_max)
    np_image = (np_image - clip_min) / (clip_max - clip_min)
    return np_image


def resample(itk_image: sitk.Image,
             new_spacing: Iterable[float],
             outside_val: float = 0
             ) -> sitk.Image:

    shape = itk_image.GetSize()
    spacing = itk_image.GetSpacing()
    output_shape = tuple(int(round(s * os / ns)) for s, os, ns in zip(shape, spacing, new_spacing))
    return sitk.Resample(
        itk_image,
        output_shape,
        sitk.Transform(),
        sitk.sitkLinear,
        itk_image.GetOrigin(),
        new_spacing,
        itk_image.GetDirection(),
        outside_val,
        sitk.sitkFloat32,
    )


def center_crop(np_image: np.ndarray,
                new_shape: Iterable[int],
                outside_val: float = 0
                ) -> np.ndarray:
    output_image = np.full(new_shape, outside_val, np_image.dtype)

    slices = tuple()
    offsets = tuple()
    for it, sh in enumerate(new_shape):
        size = sh // 2
        if it == 0:
            center = np_image.shape[it] - size
        else:
            center = (np_image.shape[it] // 2)
        start = center - size
        stop = center + size + (sh % 2)

        # computing what area of the original image will be in the cropped output
        slce = slice(max(0, start), min(np_image.shape[it], stop))
        slices += (slce,)

        # computing offset to pad if the crop is partly outside of the scan
        offset = slice(-min(0, start), 2 * size - max(0, (start + 2 * size) - np_image.shape[it]))
        offsets += (offset,)

    output_image[offsets] = np_image[slices]

    return output_image


def preprocess(input_image: sitk.Image,
               new_spacing: Iterable[float] = (1.6, 1.6, 1.6),
               new_shape: Iterable[int] = (240, 240, 240),
               ) -> np.ndarray:

    input_image = resample(input_image, new_spacing=new_spacing)
    input_image = sitk.GetArrayFromImage(input_image)
    input_image = center_crop(input_image, new_shape=new_shape)
    input_image = clip_and_normalize(input_image)
    return input_image


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import sys

    def show(im, title):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        ax1.imshow(im[im.shape[0] // 2, :, :])
        ax2.imshow(im[:, im.shape[1] // 2, :])
        ax3.imshow(im[:, :, im.shape[2] // 2])
        plt.title(title)
        plt.show()

    print('loading')
    input_image = sitk.ReadImage(sys.argv[1])
    show(sitk.GetArrayFromImage(input_image), 'loaded')
    print('resampling')
    input_image = resample(input_image, new_spacing=(1.6, 1.6, 1.6))
    input_image = sitk.GetArrayFromImage(input_image)
    show(input_image, 'resampled')
    print('cropping')
    input_image = center_crop(input_image, new_shape=(240, 240, 240))
    show(input_image, 'cropped')
    print('normalizing')
    input_image = clip_and_normalize(input_image)
    show(input_image, 'clipped')
    print('done.')
