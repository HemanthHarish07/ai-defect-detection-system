import argparse
from pathlib import Path
from datasets import load_dataset
from transformers import (
    AutoFeatureExtractor,
    AutoModelForImageClassification,
    TrainingArguments,
    Trainer,
)
import torch

MODEL_NAME = "google/vit-base-patch16-224"


def parse_args():
    parser = argparse.ArgumentParser(description="Train defect detection ViT model")
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to dataset root with normal/defective folders")
    parser.add_argument("--output_dir", type=str, default="../model", help="Directory to save the trained model")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    return parser.parse_args()


def main():
    args = parse_args()
    data_path = Path(args.dataset_path)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset path not found: {args.dataset_path}")

    dataset = load_dataset("imagefolder", data_dir=str(data_path))
    labels = dataset["train"].features["label"].names

    extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(labels),
        id2label={i: label for i, label in enumerate(labels)},
        label2id={label: i for i, label in enumerate(labels)},
    )

    def transform(example):
        example["pixel_values"] = extractor(images=example["image"], return_tensors="pt")["pixel_values"][0]
        return example

    dataset = dataset.with_transform(transform)
    train_test = dataset["train"].train_test_split(test_size=0.15, seed=42)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        evaluation_strategy="epoch",
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        save_strategy="epoch",
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = logits.argmax(axis=-1)
        accuracy = (predictions == labels).astype(float).mean().item()
        return {"accuracy": accuracy}

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_test["train"],
        eval_dataset=train_test["test"],
        compute_metrics=compute_metrics,
        tokenizer=extractor,
    )

    trainer.train()
    trainer.save_model(args.output_dir)

    print(f"Saved fine-tuned model to {args.output_dir}")


if __name__ == "__main__":
    main()
