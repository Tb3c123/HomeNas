---
name: multimodal-vision-audio-ai
description: Design reliable multimodal pipelines across vision (VLM/OCR/layout), audio (ASR/Whisper/VAD), and cross-modal embeddings with bounded cost.
metadata:
  model: inherit
  source: Orchestra-Research/AI-Research-SKILLs (MIT)
---

# Multimodal AI (Vision, OCR & Audio)

## Use This Skill When
- Building document OCR/extraction, image understanding (VLM), or audio transcription (Whisper/ASR) pipelines.
- Indexing images, PDFs, or audio clips into cross-modal search or structured JSON outputs.
- Optimizing media preprocessing, chunking, and latency/token cost for multimodal inputs.

## Core Principles
1. **Right Tool Per Modality (Don't Over-Call VLMs):**
   - Digital text PDFs → deterministic text/table extractors first; escalate to VLM/OCR only for scanned pages, complex layouts, charts, or handwriting.
   - Audio → apply **VAD (Voice Activity Detection)** and resample to `16 kHz mono` before ASR (`faster-whisper`/Whisper) to skip silence and eliminate hallucinated loops.
2. **Resolution & Token Budgeting:** Downscale images to the minimum crisp resolution required (e.g., `1024–1568px` longest edge for document OCR) while preserving legible text; avoid sending raw 4K frames unnecessarily.
3. **Structured Extraction with Confidence & Provenance:** Enforce strict JSON schemas (Pydantic/Zod) with page number, bounding box, or timestamp (`start_s`, `end_s`) so humans can verify extracted fields quickly.
4. **Chunking Long Audio/Video Safely:** Split long streams at VAD pauses or scene boundaries with slight overlap (`1–2s`), deduplicate boundary words, and process chunks idempotently with temp files in `/tmp`.
5. **Multimodal Evaluation:** Measure domain-specific metrics—**CER/WER** (OCR/ASR), field-level exact match (document extraction), and Recall@K (CLIP/SigLIP cross-modal retrieval)—on noisy real-world samples.

## Delivery Checklist
- Validate MIME types, file size limits, and corrupt-media handling before invoking models.
- Clean up temporary decoded frames/WAV buffers immediately after processing.
