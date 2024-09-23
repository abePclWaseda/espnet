#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

train_set="train_clean_100"
valid_set="dev"
test_sets="test_clean test_other dev_clean dev_other"

asr_config=conf/tuning/train_asr_conformer_lr2e-3_warmup15k_amp_nondeterministic.yaml
lm_config=../lm1/conf/train_transformer_gpt2_notLSM.yaml
inference_config=conf/decode_asr.yaml

./asr.sh \
    --lang en \
    --ngpu 1 \
    --nj 8 \
    --gpu_inference true \
    --inference_nj 2 \
    --nbpe 5000 \
    --max_wav_duration 30 \
    --speed_perturb_factors "0.9 1.0 1.1" \
    --audio_format "flac.ark" \
    --feats_type raw \
    --lm_config "${lm_config}" \
    --asr_config "${asr_config}" \
    --inference_config "${inference_config}" \
    --train_set "${train_set}" \
    --valid_set "${valid_set}" \
    --test_sets "${test_sets}" \
    --lm_train_text "data/local/other_text/text" \
    --hugging_face_model_name_or_path "facebook/opt-125m" \
    --token_type "hugging_face" \
    --bpe_train_text "data/${train_set}/text" "$@"
