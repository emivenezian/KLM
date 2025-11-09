# 🔬 MASTER BUG MATRIX - All Benchmark Models

**Date:** October 28, 2025  
**Purpose:** Complete bug catalog across all benchmarks for systematic fixing

---

## 📊 **BUG PRESENCE BY MODEL**

| Bug # | Description | Puttaert | Baseline | Optimized_Actual | BAX_Fixed | Priority |
|-------|-------------|----------|----------|------------------|-----------|----------|
| **#1** | Compartment weights per-position | ❌ YES | ❌ YES | ❌ YES | ❌ YES | 🔥 CRITICAL |
| **#2** | Item assignment includes BAX/BUP/T | ❌ YES | ❌ YES | ✅ N/A | ❌ YES | 🔥 CRITICAL |
| **#3** | CRT/COL complex nested logic | ❌ YES | ✅ NO | ✅ NO | ❌ YES | 🔥 CRITICAL |
| **#4** | w variable linearization | ❌ YES | ✅ NO | ✅ NO | ❌ YES | ⚠️ HIGH |
| **#5** | Separation penalty suboptimal | ❌ YES | ❌ YES | ✅ N/A | ❌ YES | ⚠️ HIGH |
| **#6** | Objective hierarchy difference | ❌ YES | ❌ YES | ✅ OK | ❌ YES | 📊 DESIGN |
| **#7** | Big-M hardcoded | ❌ YES | ✅ N/A | ✅ N/A | ❌ YES | ⚠️ HIGH |
| **#8** | Position weight split | ❌ YES | ✅ NO | ✅ NO | ❌ YES | 📊 MEDIUM |
| **#9** | Multi-obj count mismatch | ⚠️ MAYBE | ✅ NO | ✅ NO | ✅ NO | 📊 MEDIUM |
| **#10** | COL/CRT per-position not compartment | ❌ YES | ❌ YES | ❌ YES | ❌ YES | 🔥 CRITICAL |
| **#11** | Multi-objective index wrong | ✅ NO | ❌ YES | ❌ YES | ✅ NO | ⚠️ HIGH |

---

## 🎯 **CRITICAL BUGS (MUST FIX)**

### **Bug #1: Compartment Weight Constraints** 🔥
**Present in:** ALL 4 models  
**Fix:** Change from `for t in loadlocations_C1:` to single constraint with sum over all t

### **Bug #2: Item Assignment**  🔥
**Present in:** Puttaert, Baseline, BAX_Fixed  
**Not applicable:** Optimized_Actual (W&B only)  
**Fix:** Add `if j.isNeitherBAXnorBUPnorT` filter to sum

### **Bug #3: CRT/COL Complex Logic** 🔥
**Present in:** Puttaert, BAX_Fixed  
**Not in:** Baseline, Optimized_Actual (simpler but still have Bug #10)  
**Fix:** Simplify to compartment-level binary with big-M

### **Bug #10: COL/CRT Per-Position** 🔥
**Present in:** ALL 4 models  
**Fix:** Change to compartment-level mutual exclusion with big-M

---

## ⚠️ **HIGH PRIORITY BUGS (SHOULD FIX)**

### **Bug #4: w Variable Linearization**
**Present in:** Puttaert, BAX_Fixed  
**Not in:** Baseline, Optimized_Actual  
**Fix:** Eliminate w variable, use i.weight * z directly

### **Bug #5: Separation Penalty**
**Present in:** Puttaert, Baseline, BAX_Fixed  
**Not applicable:** Optimized_Actual (W&B only)  
**Fix:** Upgrade to Y/Z counting system

### **Bug #7: Hardcoded Big-M**
**Present in:** Puttaert, BAX_Fixed  
**Not applicable:** Baseline, Optimized_Actual  
**Fix:** Use `M = max([i.weight for i in cargo.items])`

### **Bug #8: Position Weight Split**
**Present in:** Puttaert, BAX_Fixed  
**Not in:** Baseline, Optimized_Actual  
**Fix:** Combine into single constraint

### **Bug #11: Multi-Objective Index Wrong**
**Present in:** Baseline, Optimized_Actual  
**Not in:** Puttaert, BAX_Fixed  
**Fix:** Use sequential indices (0, 1, 2, ...) not (0, 5)

---

## 📋 **BUG COUNT BY MODEL**

| Model | Critical | High | Medium | Total | Complexity |
|-------|----------|------|--------|-------|------------|
| **Puttaert** | 4 | 4 | 1 | 9 | Most bugs |
| **Baseline** | 3 | 1 | 0 | 4 | Simpler (W&B separate) |
| **Optimized_Actual** | 2 | 1 | 0 | 3 | Simplest! |
| **BAX_Fixed** | 4 | 4 | 0 | 8 | Based on Puttaert |
| **DelgadoVenezian** | 0 | 0 | 0 | 0 | ✅ CORRECT |

---

## 🎯 **FIXING PRIORITY ORDER**

### **Phase A: Fix All CRITICAL Bugs (Correctness)**
1. **Bug #1:** Compartment weights (ALL 4 models)
2. **Bug #2:** Item assignment (Puttaert, Baseline, BAX_Fixed)
3. **Bug #10:** COL/CRT per-position (ALL 4 models)
4. **Bug #3:** CRT/COL complex logic (Puttaert, BAX_Fixed)

### **Phase B: Fix HIGH Priority Bugs (Efficiency/Quality)**
5. **Bug #11:** Multi-objective index (Baseline, Optimized_Actual)
6. **Bug #4:** w variable (Puttaert, BAX_Fixed)
7. **Bug #5:** Separation penalty (Puttaert, Baseline, BAX_Fixed)
8. **Bug #7:** Hardcoded Big-M (Puttaert, BAX_Fixed)
9. **Bug #8:** Position weight split (Puttaert, BAX_Fixed)

---

## 🚀 **RECOMMENDED FIX ORDER**

Since we want comparable benchmarks:

### **Option 1: Fix Critical Bugs Only (Minimum for Correctness)**
- Fix Bugs #1, #2, #10, #3
- Keep design differences (separation penalty, w variable, etc.)
- **Pros:** Minimal changes, preserves original model intent
- **Cons:** Still has efficiency differences

### **Option 2: Fix All Bugs (Maximum Comparability)** ← RECOMMENDED
- Fix all 11 bugs
- Make all models use same logic as DelgadoVenezian where applicable
- **Pros:** True apples-to-apples comparison
- **Cons:** More changes to original models

---

## 📋 **NEXT STEPS - WHICH APPROACH?**

**Before I start fixing, please confirm:**

1. **Fix critical bugs only** (#1, #2, #3, #10)?
2. **Fix all bugs** (#1-11 where applicable)?
3. **Custom selection** (you tell me which bugs to fix)?

**What do you prefer?** I recommend **Option 2** (fix all bugs) for true comparability.


