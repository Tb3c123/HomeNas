---
name: time-series-forecasting
description: Build leakage-free time-series forecasts, seasonal decomposition, and anomaly detectors using walk-forward validation and baselines.
metadata:
  model: inherit
  source: K-Dense-AI/scientific-agent-skills (MIT)
---

# Time-Series Forecasting & Anomaly Detection

## Use This Skill When
- Forecasting demand, telemetry, thermal/resource metrics, or financial/sensor series.
- Detecting anomalies, changepoints, or drift in temporal streams.
- Designing temporal cross-validation without future data leakage.

## Core Principles
1. **Strict Temporal Integrity (Zero Look-Ahead Leakage):**
   - Never use random train/test splits or standard K-fold CV on time series.
   - Use **walk-forward / expanding-window** or **rolling-origin** validation; fit scalers, imputers, and lag encoders strictly inside each training fold.
   - Verify all exogenous features are actually known at forecast time $t$ (no future aggregates).
2. **Beat Simple Baselines First:** Always benchmark against **Naive** ($\hat{y}_{t+h} = y_t$) and **Seasonal Naive** ($\hat{y}_{t+h} = y_{t+h-m}$) before introducing ARIMA/ETS, Prophet, GBDT with lags, or neural forecasters.
3. **Diagnostic Exploration:** Inspect frequency, missing timestamps, timezone/DST shifts, trend + seasonality decomposition (STL), stationarity (ADF/KPSS), and ACF/PACF before model selection.
4. **Right Metrics & Uncertainty:**
   - Prefer scale-independent **MASE** or **sMAPE** / **MAE** / **RMSE** (avoid MAPE when values approach zero).
   - Output **prediction intervals** (quantiles / conformal prediction) alongside point forecasts so downstream decisions account for uncertainty.
5. **Anomaly Detection Hygiene:** Combine robust rolling baselines (median + MAD / STL residuals) with persistence/cooldown thresholds to prevent noisy single-spike false alerts.

## Delivery Checklist
- Confirm zero future-feature leakage across all lag/rolling/target-encoding transforms.
- Report out-of-sample walk-forward metrics against Seasonal Naive baseline.
