import nibabel as nib
import numpy as np
from skimage import measure
import os

def export_obj_with_materials(brain_nii_path, tumor_mask_path, output_obj_path):
    brain_nii = nib.load(brain_nii_path)
    tumor_nii = nib.load(tumor_mask_path)
    brain_data = brain_nii.get_fdata()
    tumor_data = tumor_nii.get_fdata()
    
    combined_volume = np.zeros_like(brain_data, dtype=np.uint8)
    combined_volume[brain_data > 0] = 1
    combined_volume[tumor_data > 0] = 2

    verts_all = []
    faces_all = []
    materials = []
    vert_offset = 0

    labels = {1: 'brain', 2: 'tumor'}
    for label_val, mat_name in labels.items():
        binary_volume = (combined_volume == label_val).astype(np.uint8)
        if np.sum(binary_volume) == 0:
            continue
        verts, faces, _, _ = measure.marching_cubes(binary_volume, level=0.5)

        verts_all.extend(verts)
        faces_all.append((faces + vert_offset, mat_name))
        vert_offset += len(verts)
        materials.append(mat_name)

    with open(output_obj_path, "w") as f:
        f.write(f"mtllib {os.path.basename(output_obj_path).replace('.obj', '.mtl')}\n")
        for v in verts_all:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

        for faces, mat in faces_all:
            f.write(f"usemtl {mat}\n")
            for face in faces:
                f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    mtl_path = output_obj_path.replace('.obj', '.mtl')
    with open(mtl_path, "w") as f:
        if "brain" in materials:
            f.write("newmtl brain\n")
            f.write("Kd 0.8 0.8 0.8\n")
            f.write("d 0.3\n")
            f.write("illum 2\n")
        if "tumor" in materials:
            f.write("newmtl tumor\n")
            f.write("Kd 1.0 0.0 0.0\n")
            f.write("d 1.0\n")
            f.write("illum 2\n")

    print(f"OBJ and MTL files written to: {output_obj_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    brain_nii = os.path.join(base_dir, "input", "uploaded.nii")
    mask_nii = os.path.join(base_dir, "output", "predicted_mask.nii.gz")
    obj_out = os.path.join(base_dir, "output", "brain_with_tumor.obj")

    export_obj_with_materials(brain_nii, mask_nii, obj_out)