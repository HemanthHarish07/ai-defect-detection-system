# Model Training Guide

## Overview

This project uses **Vision Transformer (ViT)** from Hugging Face (`google/vit-base-patch16-224`) fine-tuned on defect detection data.

## Training on MVTec AD Dataset

### 1. Download MVTec AD Dataset

- Visit: https://www.mvtec.com/company/research/datasets/mvtec-ad
- Download the official dataset (3.6 GB)
- Extract to a known location

### 2. Prepare Dataset Structure

Organize images into folders:

```text
/path/to/mvtec_ad/
├── texture/
│   ├── train/
│   │   ├── good/
│   │   └── defective/
│   └── test/
├── carpet/
├── wood/
...
```

Or use the provided sample generator:

```bash
python sample_data/generate_samples.py --output sample_data/demo
```

This creates a minimal 3-image training set for testing.

### 3. Install Training Dependencies

```bash
pip install -r ai-service/requirements.txt
```

### 4. Train the Model

From the repository root:

```bash
cd ai-service
python training/train.py \
  --dataset_path ../sample_data/demo \
  --output_dir ./model \
  --epochs 2 \
  --batch_size 8
```

**Options:**

- `--dataset_path`: Path to dataset with `normal/` and `defective/` folders
- `--output_dir`: Where to save the fine-tuned model
- `--epochs`: Number of training epochs (3-5 recommended)
- `--batch_size`: Batch size (8, 16, or 32)

### 5. Verify Model

The trained model files will be saved in `ai-service/model/`:

```text
ai-service/model/
├── config.json
├── pytorch_model.bin
├── preprocessor_config.json
└── ...
```

### 6. Use Trained Model

The AI service automatically loads from `ai-service/model/` if it exists, otherwise falls back to the pretrained model.

To rebuild with the trained model:

```bash
docker-compose build ai-service
docker-compose up
```

## Training on Custom Dataset

Replace the dataset path with your own:

```bash
python training/train.py \
  --dataset_path /path/to/your/dataset \
  --output_dir ./model \
  --epochs 5 \
  --batch_size 16
```

**Dataset requirements:**

- At least 50 images per class (normal/defective)
- PNG or JPEG format
- 224x224 pixel resolution (automatically resized)
- Balanced classes for best results

## Model Architecture

- **Base Model:** Vision Transformer (ViT-B/16)
- **Patch Size:** 16x16
- **Input Resolution:** 224x224
- **Classifier:** 2-class (defective/non-defective)
- **Training Framework:** Transformers + PyTorch

## Inference Performance

Expected inference time on CPU: ~200-500ms per image
Expected inference time on GPU: ~50-100ms per image

## Notes

- Training on full MVTec AD dataset takes ~2-3 hours on GPU
- Sample dataset trains in <1 minute (for testing only)
- Model size: ~340 MB (PyTorch binary)
- Transfer learning fine-tuning is much faster than training from scratch
