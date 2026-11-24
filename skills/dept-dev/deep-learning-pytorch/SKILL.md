---
name: deep-learning-pytorch
description: Architect, train, and debug PyTorch neural networks with explicit tensor shape contracts, numerical stability, mixed precision, and reproducibility.
metadata:
  model: inherit
  source: K-Dense-AI/scientific-agent-skills (MIT) + Orchestra-Research/AI-Research-SKILLs (MIT)
---

# Deep Learning & PyTorch Engineering

## Use This Skill When
- Implementing or modifying neural architectures (Transformers, CNNs, GNNs, MLPs) in PyTorch.
- Setting up training loops, learning-rate schedules, mixed precision, or checkpointing.
- Debugging vanishing/exploding gradients, NaN losses, GPU OOMs, or slow data loaders.

## Core Principles
1. **Explicit Shape & Device Contracts:** Document tensor shapes (`[B, T, D]`) in comments/assertions; avoid silent broadcasting bugs (e.g., `[B]` vs `[B, 1]` in loss functions) and keep device/dtype transfers explicit.
2. **Sanity-Check Before Full Training:**
   - **Overfit 1 tiny batch** (loss must drop near 0) to verify gradients, labels, and wiring.
   - Verify initial loss matches theoretical random baseline (e.g., $\ln(C)$ for $C$-class cross-entropy).
3. **Training Stability Defaults:**
   - Use `AdamW` with decoupled weight decay (exclude bias & LayerNorm/RMSNorm params), linear warmup + cosine decay, and gradient norm clipping (`clip_grad_norm_(params, 1.0)`).
   - Use `torch.amp.autocast(dtype=torch.bfloat16)` when supported (or `float16` + `GradScaler`); compute numerically sensitive reductions/losses in `float32`.
4. **Memory & Throughput Hygiene:** Use `torch.inference_mode()` during eval, `set_to_none=True` on `zero_grad`, `pin_memory=True` + tuned `num_workers` for `DataLoader`, and gradient accumulation/checkpointing when VRAM-bound.
5. **Reproducible Checkpoints:** Save model, optimizer, scheduler, epoch/step, config, and RNG states; log train/val loss, grad norm, and LR continuously.

## Delivery Checklist
- Pass 1-batch overfit smoke test and unit test forward/backward shapes on CPU/GPU.
- Confirm checkpoint save/resume reproduces identical loss trajectory.
