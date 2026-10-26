import os
import sys
import io
import json
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from sklearn.model_selection import train_test_split

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.preprocessing import TextPreprocessor
from pipeline.inset_lexicon import InSetLexiconClassifier
from pipeline.classifiers import (
    LinearSVMClassifier,
    HybridSVMClassifier,
    CosineSimilarityClassifier,
    NeuralBiLSTMClassifier,
    XShotReasoningClassifier,
    TORCH_AVAILABLE
)
from pipeline.evaluator import ModelEvaluator

def run_analysis_pipeline():
    print("=" * 75)
    print("ANALISIS SENTIMEN MULTI-PARADIGMA KELANGKAAN BBM DI INDONESIA")
    print("Perbandingan: InSet Lexicon, Linear SVM, Cosine Similarity, & Hybrid SVM")
    print("=" * 75)
    
    # 1. Jalur Dataset BBM
    raw_path = "data/dataset_bbm_raw.csv"
    if not os.path.exists(raw_path):
        raw_path = "data/dataset_ketenagakerjaan_raw.csv"

    prep_csv_path = "data/dataset_bbm_preprocessed.csv"
    prep_xlsx_path = "data/dataset_bbm_preprocessed.xlsx"

    preprocessor = TextPreprocessor()
    inset_classifier = InSetLexiconClassifier()

    print(f"\n[1] Membaca dataset: {raw_path}")
    df = pd.read_csv(raw_path)
    
    # Jalankan 5 tahap preprocessing NLP
    recompute = "--recompute" in sys.argv or "--force-preprocess" in sys.argv
    if os.path.exists(prep_csv_path) and not recompute:
        print(f"[2] Membaca dataset preprocessed yang sudah ada: {prep_csv_path}")
        df = pd.read_csv(prep_csv_path)
        if "cleaned_text" not in df.columns:
            df["cleaned_text"] = [preprocessor.clean_text(str(t).lower()) for t in df["text"]]
    else:
        print(f"[2] Menjalankan 5 Tahap Preprocessing NLP pada {len(df)} komentar...")
        case_folded_list, cleaned_text_list, tokens_raw_list = [], [], []
        tokens_normalized_list, tokens_no_stop_list = [], []
        tokens_stemmed_list, processed_text_list = [], []
        lexicon_scores, lexicon_preds = [], []

        for _, row in df.iterrows():
            txt = str(row.get("text", ""))
            prep = preprocessor.preprocess_full(txt)
            case_folded_list.append(prep["case_folded"])
            cleaned_text_list.append(prep.get("cleaned_text", ""))
            tokens_raw_list.append(", ".join(prep["tokens_raw"]))
            tokens_normalized_list.append(", ".join(prep["tokens_normalized"]))
            tokens_no_stop_list.append(", ".join(prep["tokens_no_stopwords"]))
            tokens_stemmed_list.append(", ".join(prep["tokens_stemmed"]))
            processed_text_list.append(prep["processed_text"])
            
            lex_res = inset_classifier.predict(prep["tokens_stemmed"])
            lexicon_scores.append(lex_res["score"])
            lexicon_preds.append(lex_res["label"])

        df["case_folded"] = case_folded_list
        df["cleaned_text"] = cleaned_text_list
        df["tokens_raw"] = tokens_raw_list
        df["tokens_normalized"] = tokens_normalized_list
        df["tokens_no_stopwords"] = tokens_no_stop_list
        df["tokens_stemmed"] = tokens_stemmed_list
        df["processed_text"] = processed_text_list
        df["lexicon_score"] = lexicon_scores
        df["pred_lexicon"] = lexicon_preds

    # Filter teks valid (panjang karakter > 2)
    valid_mask = df["processed_text"].str.strip().str.len() > 2
    df = df[valid_mask].copy().reset_index(drop=True)

    # Memuat Ground Truth Resmi Hasil Pelabelan LLM
    gt_csv_path = "data/dataset_bbm_ground_truth.csv"
    if os.path.exists(gt_csv_path):
        gt_df = pd.read_csv(gt_csv_path)
        id_to_gt = dict(zip(gt_df["id"], gt_df["sentiment_ground_truth"]))
        id_to_reason = dict(zip(gt_df["id"], gt_df.get("ground_truth_reason", "Opini masyarakat seputar kelangkaan BBM")))
        df["sentiment_ground_truth"] = df["id"].map(id_to_gt).fillna("Negatif")
        df["ground_truth_reason"] = df["id"].map(id_to_reason).fillna("Opini masyarakat seputar kelangkaan BBM")
        print(f"[3] Ground Truth LLM dimuat dari {gt_csv_path}:")
        print(df["sentiment_ground_truth"].value_counts().to_string())
    else:
        # Fallback jika file ground truth belum diekspor
        df["sentiment_ground_truth"] = df.get("sentiment_ground_truth", "Negatif")

    # Partisi Dataset Terstratifikasi (80% Train, 20% Test)
    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["sentiment_ground_truth"]
    )
    test_indices = set(test_df.index)
    df["dataset_split"] = ["Test (20%)" if i in test_indices else "Train (80%)" for i in df.index]

    train_df = df[df["dataset_split"] == "Train (80%)"].copy()
    test_df = df[df["dataset_split"] == "Test (20%)"].copy()

    print(f"\n[3] Partisi Dataset Terstratifikasi:")
    print(f"    - Train Set (80%): {len(train_df)} sampel")
    print(f"    - Test Set  (20%): {len(test_df)} sampel")
    print(f"    - Distribusi Kelas Ground Truth:")
    print(df["sentiment_ground_truth"].value_counts().to_string())

    X_train_text = train_df["processed_text"].fillna("").tolist()
    y_train = train_df["sentiment_ground_truth"].tolist()
    s_train = train_df["lexicon_score"].tolist()

    X_test_text = test_df["processed_text"].fillna("").tolist()
    y_test_true = test_df["sentiment_ground_truth"].tolist()
    s_test = test_df["lexicon_score"].tolist()
    test_raw_texts = test_df["text"].fillna("").tolist()

    # ---------------------------------------------------------
    # 1. METODE 1: InSet Lexicon
    # ---------------------------------------------------------
    print("\n[4] Evaluasi Metode 1: InSet Lexicon...")
    test_tokens = [str(t).split(", ") for t in test_df["tokens_stemmed"]]
    y_pred_lexicon = [inset_classifier.predict(tok)["label"] for tok in test_tokens]

    # ---------------------------------------------------------
    # 2. METODE 2: Linear SVM (Pure TF-IDF Unigram & Bigram)
    # ---------------------------------------------------------
    print("[5] Melatih & Evaluasi Metode 2: Linear SVM (Pure TF-IDF)...")
    svm_classifier = LinearSVMClassifier(ngram_range=(1, 2), min_df=2, C=1.0)
    svm_classifier.fit(X_train_text, y_train)
    y_pred_svm = svm_classifier.predict(X_test_text)

    # ---------------------------------------------------------
    # 3. METODE 3: Cosine Similarity (TF-IDF Centroid Prototype)
    # ---------------------------------------------------------
    print("[6] Melatih & Evaluasi Metode 3: Cosine Similarity (Nearest Centroid)...")
    cos_classifier = CosineSimilarityClassifier()
    cos_classifier.fit(X_train_text, y_train, vectorizer=svm_classifier.vectorizer)
    y_pred_cosine = cos_classifier.predict(X_test_text)

    # ---------------------------------------------------------
    # 4. METODE 4: Hybrid SVM (TF-IDF + InSet Lexicon Score)
    # ---------------------------------------------------------
    print("[7] Melatih & Evaluasi Metode 4: Hybrid SVM (TF-IDF + InSet Score)...")
    hybrid_classifier = HybridSVMClassifier(vectorizer=svm_classifier.vectorizer, C=1.0)
    hybrid_classifier.fit(X_train_text, s_train, y_train)
    y_pred_hybrid = hybrid_classifier.predict(X_test_text, s_test)

    # ---------------------------------------------------------
    # 5. METODE 5 & 6 (Deep Learning BiLSTM & X-Shot Reasoning)
    # ---------------------------------------------------------
    if TORCH_AVAILABLE:
        print("[8] Melatih & Evaluasi Metode 5: Deep Learning (Neural BiLSTM + Attention)...")
        bilstm_classifier = NeuralBiLSTMClassifier(embed_dim=64, hidden_dim=64, max_len=40)
        bilstm_classifier.fit(X_train_text, y_train, epochs=25, lr=0.005)
        y_pred_bilstm = bilstm_classifier.predict(X_test_text)
    else:
        print("[8] Neural BiLSTM: Dilewati (Torch tidak diinstal, fokus pada SVM & Klasik ML).")
        bilstm_classifier = None
        y_pred_bilstm = y_pred_svm

    print("[9] Evaluasi Metode 6: X-Shot Reasoning (Contextual Chain-of-Thought)...")
    xshot_classifier = XShotReasoningClassifier()
    y_pred_xshot = xshot_classifier.predict(test_raw_texts, X_test_text)

    # ---------------------------------------------------------
    # Hitung Metrik Evaluasi Komprehensif
    # ---------------------------------------------------------
    print("\n[10] Menghitung Metrik Evaluasi Komparatif:")
    evaluator = ModelEvaluator(labels=["Negatif", "Netral", "Positif"])

    eval_lexicon = evaluator.evaluate(y_test_true, y_pred_lexicon, method_name="InSet Lexicon")
    eval_svm = evaluator.evaluate(y_test_true, y_pred_svm, method_name="Linear SVM")
    eval_cosine = evaluator.evaluate(y_test_true, y_pred_cosine, method_name="Cosine Similarity")
    eval_hybrid = evaluator.evaluate(y_test_true, y_pred_hybrid, method_name="Hybrid SVM (TF-IDF + InSet)")
    eval_bilstm = evaluator.evaluate(y_test_true, y_pred_bilstm, method_name="Neural BiLSTM (Attention)")
    eval_xshot = evaluator.evaluate(y_test_true, y_pred_xshot, method_name="X-Shot Reasoning (CoT)")

    summary_data = [
        {
            "Paradigma": "Lexicon-Based",
            "Metode": "InSet Lexicon",
            "Akurasi": f"{eval_lexicon['accuracy']*100:.2f}%",
            "Precision (Macro)": f"{eval_lexicon['macro_avg']['precision']*100:.2f}%",
            "Recall (Macro)": f"{eval_lexicon['macro_avg']['recall']*100:.2f}%",
            "F1-Score (Macro)": f"{eval_lexicon['macro_avg']['f1_score']*100:.2f}%",
            "F1-Score (Weighted)": f"{eval_lexicon['weighted_avg']['f1_score']*100:.2f}%"
        },
        {
            "Paradigma": "Machine Learning (Baseline)",
            "Metode": "Linear SVM",
            "Akurasi": f"{eval_svm['accuracy']*100:.2f}%",
            "Precision (Macro)": f"{eval_svm['macro_avg']['precision']*100:.2f}%",
            "Recall (Macro)": f"{eval_svm['macro_avg']['recall']*100:.2f}%",
            "F1-Score (Macro)": f"{eval_svm['macro_avg']['f1_score']*100:.2f}%",
            "F1-Score (Weighted)": f"{eval_svm['weighted_avg']['f1_score']*100:.2f}%"
        },
        {
            "Paradigma": "Machine Learning (Hybrid)",
            "Metode": "Hybrid SVM (TF-IDF + InSet)",
            "Akurasi": f"{eval_hybrid['accuracy']*100:.2f}%",
            "Precision (Macro)": f"{eval_hybrid['macro_avg']['precision']*100:.2f}%",
            "Recall (Macro)": f"{eval_hybrid['macro_avg']['recall']*100:.2f}%",
            "F1-Score (Macro)": f"{eval_hybrid['macro_avg']['f1_score']*100:.2f}%",
            "F1-Score (Weighted)": f"{eval_hybrid['weighted_avg']['f1_score']*100:.2f}%"
        },
        {
            "Paradigma": "Distance Metric",
            "Metode": "Cosine Similarity",
            "Akurasi": f"{eval_cosine['accuracy']*100:.2f}%",
            "Precision (Macro)": f"{eval_cosine['macro_avg']['precision']*100:.2f}%",
            "Recall (Macro)": f"{eval_cosine['macro_avg']['recall']*100:.2f}%",
            "F1-Score (Macro)": f"{eval_cosine['macro_avg']['f1_score']*100:.2f}%",
            "F1-Score (Weighted)": f"{eval_cosine['weighted_avg']['f1_score']*100:.2f}%"
        },
        {
            "Paradigma": "X-Shot Learning",
            "Metode": "X-Shot Reasoning (CoT)",
            "Akurasi": f"{eval_xshot['accuracy']*100:.2f}%",
            "Precision (Macro)": f"{eval_xshot['macro_avg']['precision']*100:.2f}%",
            "Recall (Macro)": f"{eval_xshot['macro_avg']['recall']*100:.2f}%",
            "F1-Score (Macro)": f"{eval_xshot['macro_avg']['f1_score']*100:.2f}%",
            "F1-Score (Weighted)": f"{eval_xshot['weighted_avg']['f1_score']*100:.2f}%"
        }
    ]

    summary_df = pd.DataFrame(summary_data)
    print("\n" + "=" * 80)
    print(f"TABEL EVALUASI KOMPARATIF METODE SENTIMEN (TEST SET N={len(test_df)})")
    print("=" * 80)
    print(summary_df.to_string(index=False))
    print("=" * 80)

    # ---------------------------------------------------------
    # Prediksi untuk Seluruh Dataset (Full Predictions)
    # ---------------------------------------------------------
    all_texts = df["processed_text"].fillna("").tolist()
    all_raws = df["text"].fillna("").tolist()
    all_scores = df["lexicon_score"].tolist()

    df["pred_svm"] = svm_classifier.predict(all_texts)
    df["pred_cosine"] = cos_classifier.predict(all_texts)
    df["pred_hybrid_svm"] = hybrid_classifier.predict(all_texts, all_scores)
    df["pred_bilstm"] = df["pred_svm"]
    df["pred_xshot"] = xshot_classifier.predict(all_raws, all_texts)

    # Simpan Dataset Preprocessed Lengkap (BBM & Fallback Ketenagakerjaan)
    df.to_csv(prep_csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(prep_xlsx_path, index=False)
    
    # Sinkronkan juga ke dataset_ketenagakerjaan_preprocessed agar dashboard web langsung membaca data BBM
    df.to_csv("data/dataset_ketenagakerjaan_preprocessed.csv", index=False, encoding="utf-8-sig")
    df.to_excel("data/dataset_ketenagakerjaan_preprocessed.xlsx", index=False)

    print(f"\n[11] Dataset preprocessed lengkap berhasil disimpan:")
    print(f"     - {prep_csv_path}")
    print(f"     - {prep_xlsx_path}")

    # Simpan Laporan Evaluasi Lengkap JSON & XLSX
    eval_report = {
        "dataset_info": {
            "total_samples": len(df),
            "train_samples": len(train_df),
            "test_samples": len(test_df),
            "platforms": df["platform"].value_counts().to_dict(),
            "sentiment_distribution": df["sentiment_ground_truth"].value_counts().to_dict()
        },
        "evaluation_summary": summary_data,
        "detailed_metrics": {
            "inset_lexicon": eval_lexicon,
            "cosine_similarity": eval_cosine,
            "linear_svm": eval_svm,
            "hybrid_svm": eval_hybrid,
            "xshot_reasoning": eval_xshot
        }
    }

    report_json_path = "data/evaluasi_komparasi_sentimen.json"
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(eval_report, f, indent=2, ensure_ascii=False)

    eval_xlsx_path = "data/evaluasi_komparasi_sentimen.xlsx"
    with pd.ExcelWriter(eval_xlsx_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Ringkasan Perbandingan", index=False)

        all_evals = [
            ("InSet Lexicon", eval_lexicon),
            ("Linear SVM", eval_svm),
            ("Hybrid SVM (TF-IDF + InSet)", eval_hybrid),
            ("Cosine Similarity", eval_cosine),
            ("X-Shot Reasoning", eval_xshot)
        ]

        per_class_rows = []
        for method, res in all_evals:
            for cls_name, m in res["per_class"].items():
                per_class_rows.append({
                    "Metode": method,
                    "Kelas Sentimen": cls_name,
                    "Precision": f"{m['precision']*100:.2f}%",
                    "Recall": f"{m['recall']*100:.2f}%",
                    "F1-Score": f"{m['f1_score']*100:.2f}%",
                    "Support": m["support"]
                })
        pd.DataFrame(per_class_rows).to_excel(writer, sheet_name="Metrik Per Kelas", index=False)

        cm_rows = []
        for method, res in all_evals:
            cm = res["confusion_matrix"]
            labels = res["labels"]
            for i, actual in enumerate(labels):
                row_dict = {"Metode": method, "Aktual (Ground Truth)": actual}
                for j, pred in enumerate(labels):
                    row_dict[f"Prediksi: {pred}"] = cm[i][j]
                cm_rows.append(row_dict)
        pd.DataFrame(cm_rows).to_excel(writer, sheet_name="Confusion Matrices", index=False)

    print(f"\n[12] Laporan komparasi evaluasi berhasil diekspor ke:")
    print(f"     - {report_json_path}")
    print(f"     - {eval_xlsx_path}")
    print("\n" + "=" * 75)
    print("ANALISIS MULTI-PARADIGMA SELESAI DENGAN SUKSES!")
    print("=" * 75)

    return eval_report

if __name__ == "__main__":
    run_analysis_pipeline()
