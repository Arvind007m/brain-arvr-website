import os
import torch
import nibabel as nib
import numpy as np
from monai.transforms import (
    LoadImaged, AddChanneld, Spacingd, Orientationd,
    ScaleIntensityd, ToTensord, Compose, Resize
)
from monai.networks.nets import UNet
from monai.inferers import sliding_window_inference
from monai.data import Dataset

def segment_mri(input_nii_path, output_nii_path, model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    original_nii = nib.load(input_nii_path)
    original_shape = original_nii.shape
    original_affine = original_nii.affine

    transforms = Compose([
        LoadImaged(keys=["image"]),
        AddChanneld(keys=["image"]),
        Spacingd(keys=["image"], pixdim=(1.5, 1.5, 2.0), mode="bilinear"),
        Orientationd(keys=["image"], axcodes="RAS"),
        ScaleIntensityd(keys=["image"]),
        ToTensord(keys=["image"]),
    ])

    dataset = Dataset(data=[{"image": input_nii_path}], transform=transforms)
    data = dataset[0]
    image = data["image"].unsqueeze(0).to(device)

    model = UNet(
        spatial_dims=3,
        in_channels=1,
        out_channels=1,
        channels=(16, 32, 64, 128, 256),
        strides=(2, 2, 2, 2),
        num_res_units=2,
    ).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    with torch.no_grad():
        output = sliding_window_inference(image, roi_size=(128, 128, 64), sw_batch_size=1, predictor=model)
        output = torch.sigmoid(output)
        output = (output > 0.5).float()

    
    resized_output = Resize(spatial_size=original_shape, mode="nearest")(output[0][0].unsqueeze(0))
    output_np = resized_output.cpu().numpy()[0]

    nib_image = nib.Nifti1Image(output_np.astype(np.uint8), affine=original_affine)
    nib.save(nib_image, output_nii_path)
    print(f"Segmentation saved and aligned to: {output_nii_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "input", "uploaded.nii")
    model_path = os.path.join(base_dir, "model", "3d_unet_brats2020.pth")
    output_path = os.path.join(base_dir, "output", "predicted_mask.nii.gz")

    segment_mri(input_path, output_path, model_path)

