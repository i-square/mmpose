# Copyright (c) OpenMMLab. All rights reserved.
from typing import Optional

import numpy as np
from mmcv.transforms import LoadImageFromFile

from mmpose.registry import TRANSFORMS


@TRANSFORMS.register_module()
class LoadImage(LoadImageFromFile):
    """Load an image from file or from the np.ndarray in ``results['img']``.

    Required Keys:

        - img_path
        - img (optional)

    Modified Keys:

        - img
        - img_shape
        - ori_shape
        - img_path (optional)

    Args:
        to_float32 (bool): Whether to convert the loaded image to a float32
            numpy array. If set to False, the loaded image is an uint8 array.
            Defaults to False.
        color_type (str): The flag argument for :func:``mmcv.imfrombytes``.
            Defaults to 'color'.
        imdecode_backend (str): The image decoding backend type. The backend
            argument for :func:``mmcv.imfrombytes``.
            See :func:``mmcv.imfrombytes`` for details.
            Defaults to 'cv2'.
        backend_args (dict, optional): Arguments to instantiate the preifx of
            uri corresponding backend. Defaults to None.
        ignore_empty (bool): Whether to allow loading empty image or file path
            not existent. Defaults to False.
    """

    def transform(self, results: dict) -> Optional[dict]:
        """The transform function of :class:`LoadImage`.

        Args:
            results (dict): The result dict

        Returns:
            dict: The result dict.
        """

        if 'img' not in results:
            # Load image from file by :meth:`LoadImageFromFile.transform`
            results = super().transform(results)
        else:
            img = results['img']
            assert isinstance(img, np.ndarray)
            if self.to_float32:
                img = img.astype(np.float32)

            if 'img_path' not in results:
                results['img_path'] = None
            results['img_shape'] = img.shape[:2]
            results['ori_shape'] = img.shape[:2]

        img = results['img']
        assert img.ndim == 2 or img.ndim == 3
        if img.ndim == 2:
            img = np.repeat(img[..., None], 3, axis=-1)
        elif img.shape[2] == 1:
            img = np.repeat(img, 3, axis=-1)
        results['img'] = img
        return results
