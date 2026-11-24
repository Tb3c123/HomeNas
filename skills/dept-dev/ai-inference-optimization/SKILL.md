---
name: ai-inference-optimization
description: Optimize LLM and neural model serving via quantization (GGUF/AWQ/INT8), KV-cache management, continuous batching, and TTFT/TPS profiling.
metadata:
  model: inherit
  source: Orchestra-Research/AI-Research-SKILLs (MIT)
---

# AI Inference & Serving Optimization

## Use This Skill When
- Deploying LLMs or ML models locally (CPU/NAS/edge via `llama.cpp`/ONNX) or on GPU servers (`vLLM`/TensorRT-LLM).
- Reducing Time-To-First-Token (TTFT), memory footprint, or cost per million tokens.
- Selecting quantization formats, batching strategies, and context-window budgets.

## Core Principles
1. **Profile the Real Bottleneck First:**
   - **Prefill phase** (long prompts) is compute-bound → optimize with prefix caching, prompt compression, and chunked prefill.
   - **Decode phase** (token generation) is memory-bandwidth-bound → optimize with quantization, KV-cache compression, and continuous batching.
2. **Smart Quantization Trade-offs:**
   - Local CPU/RAM (`llama.cpp`/GGUF): prefer `Q4_K_M` or `Q5_K_M` (best quality-to-RAM ratio); avoid `< 4-bit` unless perplexity/task eval confirms minimal degradation.
   - GPU serving (`vLLM`): use FP8 (Hopper+) or AWQ/GPTQ INT4; always benchmark task accuracy before/after quantization.
3. **KV-Cache & Context Budgeting:** Cap `max_model_len` to realistic workload needs—oversized context reservations waste huge VRAM/RAM and starve concurrency. Enable PagedAttention and automatic prefix caching for shared system prompts.
4. **Serving Reliability & Latency Controls:** Configure continuous batching, request timeouts, bounded queue depth, streaming SSE responses, and graceful overload (`429`/`503`) instead of OOM crashes.
5. **Standard Benchmark Metrics:** Always measure **TTFT (p50/p95)**, **TPOT / tokens-per-second**, **peak RAM/VRAM**, and **task accuracy delta** under realistic concurrent load.

## Delivery Checklist
- Record hardware target, runtime version, quantization spec, and load-test latency/memory table.
- Verify graceful behavior when requests exceed max context length or concurrency cap.
