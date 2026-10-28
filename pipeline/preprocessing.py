import os
import re
import csv
from typing import List, Dict, Set, Tuple, Any
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class TextPreprocessor:
    def __init__(self, slang_dict_path: str = "data/lexicon/colloquial-indonesian-lexicon.csv"):
        # 1. Inisialisasi Stemmer Sastrawi dengan Caching
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()
        self._stem_cache: Dict[str, str] = {}
        
        # 2. Inisialisasi Kamus Normalisasi Slang / Kata Alay
        self.slang_map: Dict[str, str] = {}
        self._load_slang_dictionary(slang_dict_path)
        self._add_custom_slang_mappings()
        
        # 3. Inisialisasi Stopwords dengan Pengecualian Kata Negasi
        self._init_stopwords()
        
    def _load_slang_dictionary(self, path: str):
        if os.path.exists(path):
            try:
                with open(path, mode="r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        slang = row.get("slang", "").strip().lower()
                        formal = row.get("formal", "").strip().lower()
                        if slang and formal:
                            self.slang_map[slang] = formal
            except Exception as e:
                print(f"[Warning] Gagal membaca slang lexicon: {e}")
                
    def _add_custom_slang_mappings(self):
        """Tambahan mapping kata slang populer di percakapan krisis kelangkaan BBM di media sosial"""
        custom_maps = {
            "gak": "tidak", "ga": "tidak", "ngga": "tidak", "nggak": "tidak", "kaga": "tidak",
            "gk": "tidak", "ndak": "tidak", "tak": "tidak", "tdk": "tidak",
            "bkn": "bukan", "blm": "belum", "belom": "belum", "krg": "kurang",
            "jgn": "jangan", "bgt": "sangat", "banget": "sangat", "bngt": "sangat",
            "tp": "tetapi", "tpi": "tetapi", "tapi": "tetapi",
            "krn": "karena", "karna": "karena", "krena": "karena",
            "sdh": "sudah", "udh": "sudah", "udah": "sudah", "dah": "sudah",
            "jd": "jadi", "jdi": "jadi",
            "dgn": "dengan", "dg": "dengan", "dr": "dari", "dri": "dari",
            "utk": "untuk", "untk": "untuk", "buat": "untuk",
            "sy": "saya", "gue": "saya", "gua": "saya", "gw": "saya", "aku": "saya",
            "km": "kamu", "lu": "kamu", "loe": "kamu", "elo": "kamu",
            "mrk": "mereka", "dorang": "mereka",
            "loker": "lowongan kerja", "jobseeker": "pencari kerja",
            "phk": "pemutusan hubungan kerja", "freshgrad": "lulusan baru",
            "fg": "lulusan baru", "freshgraduate": "lulusan baru",
            "hrd": "human resources", "outsourcing": "alih daya",
            "umr": "upah minimum", "ump": "upah minimum",
            "nyari": "mencari", "dpt": "dapat", "dapet": "dapat", "dapetnya": "dapatnya",
            "bener": "benar", "bner": "benar", "susahh": "susah", "susahhh": "susah",
            "parahh": "parah", "parahhh": "parah", "capek": "lelah", "cape": "lelah",
            "nyerah": "menyerah", "pasrah": "menyerah", "bingung": "bingung",
            "pt": "perusahaan", "pabrik": "pabrik", "pemerintah": "pemerintah",
            "antri": "antre", "ngantri": "antre", "ngantre": "antre", "ngular": "mengular",
            "abis": "habis", "habiss": "habis", "bensin": "bahan bakar", "pertalit": "pertalite",
            "pertamak": "pertamax", "spbu": "stasiun pengisian bahan bakar", "pom": "stasiun pengisian bahan bakar",
            "nimbun": "timbun", "ngecer": "ecer", "bahlil": "menteri"
        }
        self.slang_map.update(custom_maps)

    def _init_stopwords(self):
        factory = StopWordRemoverFactory()
        default_stopwords = set(factory.get_stop_words())
        
        # PENTING: Kata-kata negasi dan sentimen KUNCI TIDAK BOLEH dihapus!
        # Jika 'tidak' dihapus, kalimat 'tidak bagus' berubah menjadi 'bagus' (merusak polaritas).
        self.negation_words = {
            "tidak", "bukan", "belum", "kurang", "jangan", "tak", "tiada", "tanpa"
        }
        self.sentiment_preserves = {
            "sangat", "amat", "terlalu", "parah", "krisis", "sulit", "susah", "gagal",
            "buruk", "rusak", "rugi", "miskin", "kecewa", "menyerah", "berat",
            "langka", "kosong", "habis", "antre", "antri", "menjerit", "mogok", "sengsara", "lancar", "aman"
        }
        
        # Hapus kata negasi & kata kunci dari set stopword
        self.stopwords = default_stopwords - self.negation_words - self.sentiment_preserves

    def clean_text(self, text: str) -> str:
        """Pembersihan awal: hapus URL, username mention, hashtag, karakter spesial, dan angka."""
        if not isinstance(text, str):
            return ""
        
        # Hapus URL
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        # Hapus mention (@username) dan hashtag (#tag)
        text = re.sub(r'@\w+', ' ', text)
        text = re.sub(r'#\w+', ' ', text)
        # Hapus karakter HTML
        text = re.sub(r'&\w+;', ' ', text)
        # Hapus angka
        text = re.sub(r'\d+', ' ', text)
        # Normalisasi huruf berulang (elongasi)
        text = re.sub(r'(.)\1{2,}', r'\1\1', text)
        # Hapus tanda baca dan simbol non-huruf
        text = re.sub(r'[^\w\s]', ' ', text)
        # Rapikan spasi
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def case_folding(self, text: str) -> str:
        """Tahap 1: Case Folding — Mengubah semua huruf menjadi huruf kecil."""
        return text.lower().strip()

    def tokenize(self, text: str) -> List[str]:
        """Tahap 2: Tokenisasi — Memecah kalimat menjadi token kata individual."""
        tokens = re.findall(r'\b[a-z]{2,}\b', text)
        return tokens

    def normalize_slang_with_audit(self, tokens: List[str]) -> Tuple[List[str], List[Dict[str, str]]]:
        """Tahap 3: Normalisasi Kata Alay dengan pencatatan transformasi audit."""
        normalized = []
        transformations = []
        for token in tokens:
            clean_tok = re.sub(r'(.)\1{2,}', r'\1', token)
            matched_key = None
            if clean_tok in self.slang_map:
                matched_key = clean_tok
            elif token in self.slang_map:
                matched_key = token

            if matched_key:
                expanded = self.slang_map[matched_key]
                transformations.append({"from": token, "to": expanded})
                for w in expanded.split():
                    normalized.append(w)
            else:
                normalized.append(token)
        return normalized, transformations

    def remove_stopwords_with_audit(self, tokens: List[str]) -> Tuple[List[str], List[str]]:
        """Tahap 4: Stopword Removal dengan pencatatan kata yang dibuang."""
        filtered = []
        removed = []
        for t in tokens:
            if t in self.stopwords:
                removed.append(t)
            else:
                filtered.append(t)
        return filtered, removed

    def stem_with_audit(self, tokens: List[str]) -> Tuple[List[str], List[Dict[str, str]]]:
        """Tahap 5: Stemming dengan pencatatan transformasi imbuhan ke kata dasar."""
        stemmed = []
        stem_audits = []
        for token in tokens:
            if token in self.negation_words:
                stemmed.append(token)
                continue
                
            if token not in self._stem_cache:
                self._stem_cache[token] = self.stemmer.stem(token)
            
            res = self._stem_cache[token]
            if res:
                if res != token:
                    stem_audits.append({"from": token, "to": res})
                stemmed.append(res)
            else:
                stemmed.append(token)
        return stemmed, stem_audits

    def preprocess_full(self, text: str) -> Dict[str, Any]:
        """
        Menjalankan seluruh 5 tahapan prapemrosesan secara berurutan dan terstruktur:
        1. Pembersihan & Case Folding
        2. Tokenisasi
        3. Normalisasi Kata Tidak Baku (dengan audit perubahan)
        4. Stopword Removal (Negation-Preserving dengan audit kata terhapus)
        5. Stemming Sastrawi (dengan audit perubahan kata berimbuhan)
        """
        case_folded_raw = self.case_folding(text)
        cleaned = self.clean_text(case_folded_raw)
        raw_tokens = self.tokenize(cleaned)
        
        normalized_tokens, slang_audits = self.normalize_slang_with_audit(raw_tokens)
        no_stop_tokens, removed_stops = self.remove_stopwords_with_audit(normalized_tokens)
        stemmed_tokens, stem_audits = self.stem_with_audit(no_stop_tokens)
        
        processed_text = " ".join(stemmed_tokens)
        
        return {
            "original_text": text,
            "case_folded": case_folded_raw,
            "cleaned_text": cleaned,
            "tokens_raw": raw_tokens,
            "tokens_normalized": normalized_tokens,
            "tokens_no_stopwords": no_stop_tokens,
            "tokens_stemmed": stemmed_tokens,
            "processed_text": processed_text,
            "slang_transformations": slang_audits,
            "removed_stopwords": removed_stops,
            "stemming_transformations": stem_audits
        }
