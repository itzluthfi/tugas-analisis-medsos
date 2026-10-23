from typing import List, Dict, Any
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

class ModelEvaluator:
    def __init__(self, labels: List[str] = ["Negatif", "Netral", "Positif"]):
        self.labels = labels

    def evaluate(self, y_true: List[str], y_pred: List[str], method_name: str = "Model") -> Dict[str, Any]:
        """
        Menghitung metrik evaluasi lengkap:
        - Akurasi
        - Precision, Recall, F1-Score (Macro Avg & Weighted Avg)
        - Precision, Recall, F1-Score per kelas (Positif, Negatif, Netral)
        - Confusion Matrix
        """
        acc = accuracy_score(y_true, y_pred)
        
        # Macro average
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=self.labels, average="macro", zero_division=0
        )
        
        # Weighted average
        p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=self.labels, average="weighted", zero_division=0
        )
        
        # Per class metrics
        p_class, r_class, f1_class, support_class = precision_recall_fscore_support(
            y_true, y_pred, labels=self.labels, average=None, zero_division=0
        )
        
        per_class_results = {}
        for idx, lbl in enumerate(self.labels):
            per_class_results[lbl] = {
                "precision": round(float(p_class[idx]), 4),
                "recall": round(float(r_class[idx]), 4),
                "f1_score": round(float(f1_class[idx]), 4),
                "support": int(support_class[idx])
            }
            
        cm = confusion_matrix(y_true, y_pred, labels=self.labels)
        
        return {
            "method": method_name,
            "accuracy": round(float(acc), 4),
            "macro_avg": {
                "precision": round(float(p_macro), 4),
                "recall": round(float(r_macro), 4),
                "f1_score": round(float(f1_macro), 4)
            },
            "weighted_avg": {
                "precision": round(float(p_weighted), 4),
                "recall": round(float(r_weighted), 4),
                "f1_score": round(float(f1_weighted), 4)
            },
            "per_class": per_class_results,
            "confusion_matrix": cm.tolist(),
            "labels": self.labels,
            "total_samples": len(y_true)
        }
