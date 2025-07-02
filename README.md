# 3D Brain Anomaly Detection & AR/VR Viewer

A web application that processes MRI brain scans to detect tumors using AI and visualizes them in immersive 3D, AR, and VR environments.

## 🧠 Features

- **AI-Powered Tumor Detection**: Uses a 3D U-Net model to segment brain tumors from MRI scans
- **Multiple Viewing Modes**: 
  - 3D interactive viewer with model-viewer
  - AR mode for mobile devices
  - VR mode with A-Frame for immersive experience
- **Real-time Processing**: Upload `.nii` files and get immediate 3D visualizations
- **Modern UI**: Beautiful glassmorphism design with smooth animations

## 🚀 Technology Stack

### Backend
- **FastAPI**: High-performance web framework
- **PyTorch**: Deep learning for tumor segmentation
- **MONAI**: Medical imaging AI toolkit
- **Nibabel**: NIfTI file processing
- **Trimesh**: 3D mesh processing and GLB export

### Frontend
- **HTML5/CSS3/JavaScript**: Modern web technologies
- **Model-viewer**: Google's 3D model viewer with AR support
- **A-Frame**: WebXR framework for VR experiences

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- GPU support recommended for faster AI inference

### Local Development
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd brain_arvr_website
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 5000
   ```

4. Open the frontend:
   - Open `frontend/index.html` in your browser
   - Or serve it with a local server for best results

## 🏥 Usage

1. **Upload MRI Scan**: Click to upload a `.nii` file
2. **AI Processing**: The system automatically:
   - Segments the brain tumor using 3D U-Net
   - Generates 3D mesh models (.obj, .mtl)
   - Creates VR-ready GLB files
3. **View Results**: Choose your preferred viewing mode:
   - **3D View**: Interactive model with camera controls
   - **AR View**: Mobile AR experience
   - **VR View**: Immersive VR with head tracking

## 🔧 API Endpoints

- `POST /upload/`: Upload MRI scan for processing
- `GET /viewer`: 3D/AR viewer interface  
- `GET /viewer_vr`: VR viewer interface
- `GET /output/{filename}`: Download processed 3D models

## 🌐 Deployment

This application is configured for deployment on Render.com:

1. Push code to GitHub
2. Connect GitHub repository to Render
3. Deploy as a Web Service
4. The app will automatically install dependencies and start

## 🧪 Model Information

The AI model is a 3D U-Net trained on the BraTS 2020 dataset for brain tumor segmentation. The model file should be placed in `backend/model/3d_unet_brats2020.pth`.

## 📱 Browser Support

- **Desktop**: Chrome, Firefox, Safari, Edge
- **Mobile AR**: Chrome on Android, Safari on iOS
- **VR**: WebXR-compatible browsers and devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- BraTS Challenge for the dataset
- MONAI community for medical imaging tools
- Google Model Viewer and A-Frame teams 