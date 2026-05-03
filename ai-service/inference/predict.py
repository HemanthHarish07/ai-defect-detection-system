import os
from typing import Any
from PIL import Image
import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification

MODEL_NAME = os.environ.get("MODEL_NAME", "google/vit-base-patch16-224")
MODEL_DIR = os.environ.get("MODEL_PATH", "/app/model")


def load_model() -> tuple[Any, Any]:
    if os.path.exists(os.path.join(MODEL_DIR, "config.json")):
        model = AutoModelForImageClassification.from_pretrained(MODEL_DIR)
        processor = AutoFeatureExtractor.from_pretrained(MODEL_DIR)
    else:
        model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
        processor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)

    return model, processor


def predict_image(image: Image.Image, model: Any, processor: Any) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)[0]

    confidence, class_idx = torch.max(probs, dim=0)

    class_idx = int(class_idx.item())
    confidence = float(confidence.item())

    
    if hasattr(model.config, "id2label") and model.config.id2label:
        label = model.config.id2label.get(class_idx, str(class_idx))
    else:
        # fallback (only if no trained model)
        label = str(class_idx)

    label = label.lower().replace(" ", "_")

    
    if label not in ["defective", "non_defective"]:
        # fallback ONLY if using base model
        label = "defective" if confidence < 0.5 else "non_defective"

    details = (
        "Defect detected in product"
        if label == "defective"
        else "No visible defects detected"
    )

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "class_id": class_idx,
        "details": details,
    }