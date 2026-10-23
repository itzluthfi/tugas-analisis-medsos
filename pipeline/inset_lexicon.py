import os
import csv
from typing import Dict, List, Tuple, Any

class InSetLexiconClassifier:
    def __init__(self, 
                 pos_path: str = "data/lexicon/inset/positive.tsv", 
                 neg_path: str = "data/lexicon/inset/negative.tsv"):
        self.lexicon: Dict[str, float] = {}
        self.negation_words = {
            "tidak", "bukan", "belum", "kurang", "jangan", "tak", "tiada", "tanpa",
            "kaga", "gak", "ga", "ngga", "nggak"
        }
        self.load_lexicon(pos_path, neg_path)

    def load_lexicon(self, pos_path: str, neg_path: str):
        """Membaca InSet positive.tsv dan negative.tsv"""
        loaded_pos = 0
        loaded_neg = 0
        
        if os.path.exists(pos_path):
            with open(pos_path, mode="r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f, delimiter="\t")
                next(reader, None) # skip header
                for row in reader:
                    if len(row) >= 2:
                        word = row[0].strip().lower()
                        try:
                            weight = float(row[1].strip())
                            self.lexicon[word] = weight
                            loaded_pos += 1
                        except ValueError:
                            pass

        if os.path.exists(neg_path):
            with open(neg_path, mode="r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f, delimiter="\t")
                next(reader, None) # skip header
                for row in reader:
                    if len(row) >= 2:
                        word = row[0].strip().lower()
                        try:
                            weight = float(row[1].strip())
                            self.lexicon[word] = weight
                            loaded_neg += 1
                        except ValueError:
                            pass
                            
        # Domain-specific sentiment enhancements untuk konteks krisis ketenagakerjaan
        domain_weights = {
            "phk": -4.0,
            "pemutusan hubungan kerja": -4.0,
            "pengangguran": -3.5,
            "nganggur": -3.5,
            "krisis": -3.5,
            "bangkrut": -4.0,
            "tutup": -2.0,
            "pailit": -4.0,
            "sulit": -3.0,
            "susah": -3.0,
            "derita": -3.5,
            "miris": -3.0,
            "kecewa": -3.0,
            "lapangan kerja": 1.5,
            "lowongan": 1.5,
            "rekrutmen": 1.5,
            "solusi": 2.5,
            "bantuan": 2.0,
            "optimis": 3.0,
            "semangat": 3.0,
            "sukses": 3.5,
            "rezeki": 3.0,
            "peluang": 2.5,
            "kebijakan": 0.0,
            "pemerintah": 0.0,
            "industri": 0.0,
            "perusahaan": 0.0
        }
        self.lexicon.update(domain_weights)
        print(f"[InSetLexicon] Loaded {loaded_pos} pos, {loaded_neg} neg. Total lexicon: {len(self.lexicon)}")

    def score_tokens(self, tokens: List[str]) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Menghitung skor sentimen berdasarkan token dengan penanganan negasi (negation handling).
        Jika kata didahului negasi (e.g. 'tidak bagus'), polaritas skor dibalik.
        """
        total_score = 0.0
        matched_details = []
        n = len(tokens)
        
        i = 0
        while i < n:
            tok = tokens[i]
            
            # Cek apakah token saat ini adalah kata negasi
            if tok in self.negation_words and (i + 1) < n:
                # Periksa kata berikutnya
                next_tok = tokens[i + 1]
                
                # Cek apakah kata berikutnya ada di leksikon
                if next_tok in self.lexicon:
                    orig_weight = self.lexicon[next_tok]
                    # Balikkan nilai polaritas (inversi negasi)
                    inverted_weight = -1.0 * orig_weight
                    total_score += inverted_weight
                    matched_details.append({
                        "phrase": f"{tok} {next_tok}",
                        "original_weight": orig_weight,
                        "adjusted_weight": inverted_weight,
                        "is_negated": True
                    })
                    i += 2 # loncat 2 token
                    continue
            
            # Cek n-gram 2 kata (jika ada frasa di leksikon)
            if i + 1 < n:
                bigram = f"{tok} {tokens[i+1]}"
                if bigram in self.lexicon:
                    w = self.lexicon[bigram]
                    total_score += w
                    matched_details.append({
                        "phrase": bigram,
                        "original_weight": w,
                        "adjusted_weight": w,
                        "is_negated": False
                    })
                    i += 2
                    continue
                    
            # Cek unigram (kata tunggal)
            if tok in self.lexicon:
                w = self.lexicon[tok]
                total_score += w
                matched_details.append({
                    "phrase": tok,
                    "original_weight": w,
                    "adjusted_weight": w,
                    "is_negated": False
                })
                
            i += 1
            
        return total_score, matched_details

    def predict(self, tokens: List[str]) -> Dict[str, Any]:
        """
        Klasifikasi sentimen:
        - Skor > 0  => Positif
        - Skor < 0  => Negatif
        - Skor == 0 => Netral
        """
        score, details = self.score_tokens(tokens)
        
        if score > 0:
            label = "Positif"
        elif score < 0:
            label = "Negatif"
        else:
            label = "Netral"
            
        return {
            "score": round(score, 3),
            "label": label,
            "matched_words": details
        }
