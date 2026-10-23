import os
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from pipeline.preprocessing import TextPreprocessor
from pipeline.inset_lexicon import InSetLexiconClassifier
from pipeline.classifiers import (
    LinearSVMClassifier,
    HybridSVMClassifier,
    CosineSimilarityClassifier,
    NeuralBiLSTMClassifier,
    XShotReasoningClassifier
)
from pipeline.evaluator import ModelEvaluator

class SentimentResearchService:
    _instance = None

    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.inset = InSetLexiconClassifier()
        self.svm = LinearSVMClassifier(ngram_range=(1, 2), min_df=2, C=1.0)
        self.cosine = CosineSimilarityClassifier()
        self.hybrid_svm = HybridSVMClassifier(C=1.0)
        self.bilstm = NeuralBiLSTMClassifier(embed_dim=64, hidden_dim=64, max_len=40)
        self.xshot = XShotReasoningClassifier()
        self.evaluator = ModelEvaluator(labels=["Negatif", "Netral", "Positif"])
        
        self.dataset_df: Optional[pd.DataFrame] = None
        self.evaluation_results: Optional[Dict[str, Any]] = None
        self.is_ready = False
        
        self._load_or_train()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SentimentResearchService()
        return cls._instance

    def _load_or_train(self):
        prep_csv = "data/dataset_ketenagakerjaan_preprocessed.csv"
        eval_json = "data/evaluasi_komparasi_sentimen.json"
        
        if os.path.exists(prep_csv):
            self.dataset_df = pd.read_csv(prep_csv)
            # Melatih SVM, Cosine, Hybrid SVM, & BiLSTM pada data latih (80%)
            train_mask = self.dataset_df["dataset_split"] == "Train (80%)"
            train_data = self.dataset_df[train_mask]
            
            X_train = train_data["processed_text"].fillna("").tolist()
            y_train = train_data["sentiment_ground_truth"].tolist()
            s_train = train_data["lexicon_score"].tolist()
            
            # 1. Melatih Baseline SVM
            self.svm.fit(X_train, y_train)
            
            # 2. Melatih Cosine Similarity
            self.cosine.fit(X_train, y_train, vectorizer=self.svm.vectorizer)
            
            # 3. Melatih Hybrid SVM
            self.hybrid_svm.fit(X_train, s_train, y_train, vectorizer=self.svm.vectorizer)
            
            # 4. Melatih Deep Learning BiLSTM
            self.bilstm.fit(X_train, y_train, epochs=25, lr=0.005)
            
            self.is_ready = True
            
        if os.path.exists(eval_json):
            with open(eval_json, "r", encoding="utf-8") as f:
                self.evaluation_results = json.load(f)

    def get_summary(self) -> Dict[str, Any]:
        """Mengambil ringkasan riset dan metrik komparasi multi-paradigma."""
        if not self.evaluation_results:
            return {"status": "error", "message": "Hasil evaluasi belum tersedia"}
        return self.evaluation_results

    def get_dataset_page(self, page: int = 1, page_size: int = 20, platform: str = "", sentiment: str = "", query: str = "", split: str = "all", status_filter: str = "all") -> Dict[str, Any]:
        """Mengambil data komentar terproses untuk tabel data eksplorasi di UI dengan filter split dan status tebakan."""
        if self.dataset_df is None:
            return {"items": [], "total": 0, "page": page, "pages": 0}
            
        filtered = self.dataset_df.copy()
        if platform and platform != "all":
            filtered = filtered[filtered["platform"].str.lower() == platform.lower()]
        if sentiment and sentiment != "all":
            filtered = filtered[filtered["sentiment_ground_truth"].str.lower() == sentiment.lower()]
        if query:
            q_lower = query.lower()
            filtered = filtered[filtered["text"].str.lower().str.contains(q_lower, na=False)]
            
        if split and split.lower() == "test":
            filtered = filtered[filtered["dataset_split"].str.contains("Test", case=False, na=False)]
        elif split and split.lower() == "train":
            filtered = filtered[filtered["dataset_split"].str.contains("Train", case=False, na=False)]

        # Status Mismatch Auditing
        gt = filtered["sentiment_ground_truth"]
        if status_filter == "mismatch":
            # Baris di mana minimal salah satu model meleset
            mask = (filtered["pred_lexicon"] != gt) | \
                   (filtered["pred_svm"] != gt) | \
                   (filtered["pred_cosine"] != gt) | \
                   (filtered.get("pred_hybrid_svm", filtered["pred_svm"]) != gt)
            filtered = filtered[mask]
        elif status_filter == "all_correct":
            # Baris di mana model-model utama kompak BENAR
            mask = (filtered["pred_lexicon"] == gt) & \
                   (filtered["pred_svm"] == gt) & \
                   (filtered["pred_cosine"] == gt) & \
                   (filtered.get("pred_hybrid_svm", gt) == gt)
            filtered = filtered[mask]
        elif status_filter == "mismatch_svm":
            filtered = filtered[filtered["pred_svm"] != gt]
        elif status_filter == "mismatch_hybrid":
            filtered = filtered[filtered.get("pred_hybrid_svm", filtered["pred_svm"]) != gt]
        elif status_filter == "mismatch_bilstm":
            filtered = filtered[filtered.get("pred_bilstm", filtered["pred_svm"]) != gt]
        elif status_filter == "mismatch_cosine":
            filtered = filtered[filtered["pred_cosine"] != gt]
        elif status_filter == "mismatch_lexicon":
            filtered = filtered[filtered["pred_lexicon"] != gt]
            
        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        
        page_items = filtered.iloc[start:end].to_dict(orient="records")
        pages = (total + page_size - 1) // page_size if page_size > 0 else 1
        
        return {
            "items": page_items,
            "total": total,
            "page": page,
            "pages": pages,
            "page_size": page_size
        }

    def predict_text(self, text: str) -> Dict[str, Any]:
        """
        Prediksi langsung untuk teks kustom menggunakan 6 model dari seluruh paradigma:
        1. Preprocessing 5 tahap (dengan detail audit perubahan)
        2. InSet Lexicon (Lexicon-Based)
        3. Cosine Similarity (Distance Metric)
        4. Linear SVM (Machine Learning Baseline)
        5. Hybrid SVM (Machine Learning Hybrid)
        6. Neural BiLSTM (Deep Learning dengan Word Attention Weights)
        7. X-Shot Reasoning (X-Shot Learning dengan Chain of Thought)
        """
        prep = self.preprocessor.preprocess_full(text)
        
        # 1. InSet Lexicon
        lex_res = self.inset.predict(prep["tokens_stemmed"])
        lex_score = lex_res["score"]
        
        # 2. Linear SVM (TF-IDF)
        svm_res = {"label": "Netral", "confidence": 0.0, "probabilities": {}}
        if self.is_ready:
            svm_res = self.svm.predict_single(prep["processed_text"])
            
        # 3. Cosine Similarity (TF-IDF Centroid)
        cos_res = {"label": "Netral", "best_similarity": 0.0, "similarities": {}}
        if self.is_ready:
            cos_res = self.cosine.predict_single(prep["processed_text"])

        # 4. Hybrid SVM (TF-IDF + InSet Score)
        hyb_res = {"label": "Netral", "confidence": 0.0, "probabilities": {}}
        if self.is_ready:
            hyb_res = self.hybrid_svm.predict_single(prep["processed_text"], lex_score)

        # 5. Neural BiLSTM with Word Attention
        bilstm_res = {"label": "Netral", "confidence": 0.0, "probabilities": {}, "word_attentions": []}
        if self.is_ready:
            bilstm_res = self.bilstm.predict_single(prep["processed_text"])

        # 6. X-Shot Reasoning (Chain of Thought)
        xshot_res = self.xshot.predict_single(text, prep["processed_text"])

        return {
            "input_text": text,
            "preprocessing": prep,
            "predictions": {
                "inset_lexicon": {
                    "paradigm": "Lexicon-Based",
                    "method": "InSet Lexicon",
                    "label": lex_res["label"],
                    "score": lex_res["score"],
                    "matched_words": lex_res["matched_words"]
                },
                "cosine_similarity": {
                    "paradigm": "Distance Metric",
                    "method": "Cosine Similarity",
                    "label": cos_res["label"],
                    "similarity": cos_res["best_similarity"],
                    "all_similarities": cos_res["similarities"]
                },
                "linear_svm": {
                    "paradigm": "Machine Learning (Baseline)",
                    "method": "Linear SVM",
                    "label": svm_res["label"],
                    "confidence": svm_res["confidence"],
                    "probabilities": svm_res["probabilities"]
                },
                "hybrid_svm": {
                    "paradigm": "Machine Learning (Hybrid)",
                    "method": "Hybrid SVM (TF-IDF + InSet)",
                    "label": hyb_res["label"],
                    "confidence": hyb_res["confidence"],
                    "probabilities": hyb_res["probabilities"],
                    "lexicon_contribution": hyb_res.get("lexicon_contribution", 0.0)
                },
                "neural_bilstm": {
                    "paradigm": "Deep Learning",
                    "method": "Neural BiLSTM (Attention)",
                    "label": bilstm_res["label"],
                    "confidence": bilstm_res["confidence"],
                    "probabilities": bilstm_res["probabilities"],
                    "word_attentions": bilstm_res.get("word_attentions", [])
                },
                "xshot_reasoning": {
                    "paradigm": "X-Shot Learning",
                    "method": "X-Shot Reasoning (CoT)",
                    "label": xshot_res["label"],
                    "confidence": xshot_res["confidence"],
                    "chain_of_thought": xshot_res.get("chain_of_thought", []),
                    "detected_keywords": xshot_res.get("detected_keywords", {}),
                    "nearest_exemplar": xshot_res.get("nearest_exemplar", {})
                }
            }
        }
