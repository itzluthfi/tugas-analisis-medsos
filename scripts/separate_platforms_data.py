import os
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def separate_platforms():
    print("=" * 65)
    print("PEMISAHAN DATASET YOUTUBE & INSTAGRAM (RAW, GROUND TRUTH, PREPROCESSED)")
    print("=" * 65)

    os.makedirs("data", exist_ok=True)
    os.makedirs("data/youtube", exist_ok=True)
    os.makedirs("data/instagram", exist_ok=True)

    # 1. Pisahkan Data Ground Truth
    gt_file = "data/dataset_bbm_ground_truth.csv"
    if os.path.exists(gt_file):
        df_gt = pd.read_csv(gt_file)
        
        # YouTube Ground Truth
        df_gt_yt = df_gt[df_gt["platform"] == "YouTube"].copy().reset_index(drop=True)
        df_gt_yt.to_csv("data/dataset_bbm_ground_truth_youtube.csv", index=False, encoding="utf-8-sig")
        df_gt_yt.to_excel("data/dataset_bbm_ground_truth_youtube.xlsx", index=False)
        df_gt_yt.to_csv("data/youtube/dataset_youtube_bbm_ground_truth.csv", index=False, encoding="utf-8-sig")
        df_gt_yt.to_excel("data/youtube/dataset_youtube_bbm_ground_truth.xlsx", index=False)
        
        # Instagram Ground Truth
        df_gt_ig = df_gt[df_gt["platform"] == "Instagram"].copy().reset_index(drop=True)
        df_gt_ig.to_csv("data/dataset_bbm_ground_truth_instagram.csv", index=False, encoding="utf-8-sig")
        df_gt_ig.to_excel("data/dataset_bbm_ground_truth_instagram.xlsx", index=False)
        df_gt_ig.to_csv("data/instagram/dataset_instagram_bbm_ground_truth.csv", index=False, encoding="utf-8-sig")
        df_gt_ig.to_excel("data/instagram/dataset_instagram_bbm_ground_truth.xlsx", index=False)
        
        print("\n[1] Pemisahan File Ground Truth Berhasil:")
        print(f"    - YouTube Ground Truth   : {len(df_gt_yt)} sampel")
        print(f"      -> data/dataset_bbm_ground_truth_youtube.csv (.xlsx)")
        print(f"      -> data/youtube/dataset_youtube_bbm_ground_truth.csv (.xlsx)")
        print(f"    - Instagram Ground Truth : {len(df_gt_ig)} sampel")
        print(f"      -> data/dataset_bbm_ground_truth_instagram.csv (.xlsx)")
        print(f"      -> data/instagram/dataset_instagram_bbm_ground_truth.csv (.xlsx)")

    # 2. Pisahkan Data Mentah (Raw)
    raw_file = "data/dataset_bbm_raw.csv"
    if os.path.exists(raw_file):
        df_raw = pd.read_csv(raw_file)
        
        # YouTube Raw
        df_raw_yt = df_raw[df_raw["platform"] == "YouTube"].copy().reset_index(drop=True)
        df_raw_yt.to_csv("data/dataset_bbm_raw_youtube.csv", index=False, encoding="utf-8-sig")
        df_raw_yt.to_excel("data/dataset_bbm_raw_youtube.xlsx", index=False)
        df_raw_yt.to_csv("data/youtube/dataset_youtube_bbm_raw.csv", index=False, encoding="utf-8-sig")
        df_raw_yt.to_excel("data/youtube/dataset_youtube_bbm_raw.xlsx", index=False)
        
        # Instagram Raw
        df_raw_ig = df_raw[df_raw["platform"] == "Instagram"].copy().reset_index(drop=True)
        df_raw_ig.to_csv("data/dataset_bbm_raw_instagram.csv", index=False, encoding="utf-8-sig")
        df_raw_ig.to_excel("data/dataset_bbm_raw_instagram.xlsx", index=False)
        df_raw_ig.to_csv("data/instagram/dataset_instagram_bbm_raw.csv", index=False, encoding="utf-8-sig")
        df_raw_ig.to_excel("data/instagram/dataset_instagram_bbm_raw.xlsx", index=False)
        
        print("\n[2] Pemisahan File Data Mentah (Raw) Berhasil:")
        print(f"    - YouTube Raw   : {len(df_raw_yt)} sampel")
        print(f"      -> data/dataset_bbm_raw_youtube.csv (.xlsx)")
        print(f"    - Instagram Raw : {len(df_raw_ig)} sampel")
        print(f"      -> data/dataset_bbm_raw_instagram.csv (.xlsx)")

    # 3. Pisahkan Data Preprocessed
    prep_file = "data/dataset_bbm_preprocessed.csv"
    if os.path.exists(prep_file):
        df_prep = pd.read_csv(prep_file)
        
        # YouTube Preprocessed
        df_prep_yt = df_prep[df_prep["platform"] == "YouTube"].copy().reset_index(drop=True)
        df_prep_yt.to_csv("data/dataset_bbm_preprocessed_youtube.csv", index=False, encoding="utf-8-sig")
        df_prep_yt.to_excel("data/dataset_bbm_preprocessed_youtube.xlsx", index=False)
        df_prep_yt.to_csv("data/youtube/dataset_youtube_bbm_preprocessed.csv", index=False, encoding="utf-8-sig")
        df_prep_yt.to_excel("data/youtube/dataset_youtube_bbm_preprocessed.xlsx", index=False)
        
        # Instagram Preprocessed
        df_prep_ig = df_prep[df_prep["platform"] == "Instagram"].copy().reset_index(drop=True)
        df_prep_ig.to_csv("data/dataset_bbm_preprocessed_instagram.csv", index=False, encoding="utf-8-sig")
        df_prep_ig.to_excel("data/dataset_bbm_preprocessed_instagram.xlsx", index=False)
        df_prep_ig.to_csv("data/instagram/dataset_instagram_bbm_preprocessed.csv", index=False, encoding="utf-8-sig")
        df_prep_ig.to_excel("data/instagram/dataset_instagram_bbm_preprocessed.xlsx", index=False)
        
        print("\n[3] Pemisahan File Preprocessed Berhasil:")
        print(f"    - YouTube Preprocessed   : {len(df_prep_yt)} sampel")
        print(f"      -> data/dataset_bbm_preprocessed_youtube.csv (.xlsx)")
        print(f"    - Instagram Preprocessed : {len(df_prep_ig)} sampel")
        print(f"      -> data/dataset_bbm_preprocessed_instagram.csv (.xlsx)")

    print("\n" + "=" * 65)
    print("SELURUH DATASET YOUTUBE & INSTAGRAM BERHASIL DIPISAHKAN!")
    print("=" * 65)


if __name__ == "__main__":
    separate_platforms()
