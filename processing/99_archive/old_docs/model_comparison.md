# Model Comparison: Original vs Modified

## Overview
This document compares the original model (`KLM_Original/Model.ipynb`) with the modified model (`KLM_Modified/Model.ipynb`).

## Key Differences

### 1. **Decision Variables**

#### Original Model:
```python
f = {}  # ULD-position assignment
w = {}  # Weight variables (continuous)
u = {}  # ULD activation
p = {}  # Item-ULD assignment
z = {}  # Item-ULD-position assignment
```

#### Modified Model:
```python
f = {}  # ULD-position assignment
u = {}  # ULD activation
p = {}  # Item-ULD assignment (only for non-BAX/BUP/T ULDs)
z = {}  # Item-ULD-position assignment
```

**Key Change**: Removed `w` variables and simplified `p` variable definition.

### 2. **Objective Functions**

#### Original Model (6 objectives):
1. **MAC optimization** (Priority 6)
2. **Volume preference** (Priority 5) - Place large items in PMC/PAG, small in AKE
3. **Minimize ULDs** (Priority 4)
4. **Minimize underutilization** (Priority 3) - Penalize ULDs with <20% volume utilization
5. **Minimize separation** (Priority 2) - Keep items with same prefix together
6. **BAX proximity** (Priority 1)

#### Modified Model (6 objectives):
1. **MAC optimization** (Priority 6) - **Same**
2. **Volume preference** (Priority 5) - **Same**
3. **Minimize ULDs** (Priority 4) - **Same**
4. **Maximize total volume** (Priority 3) - **NEW**: Maximize total volume utilization
5. **Minimize separation** (Priority 2) - **MODIFIED**: New SP variable approach
6. **BAX proximity** (Priority 1) - **Same**

### 3. **Separation Logic**

#### Original Model:
```python
# Simple penalty approach
separation_penalty = {}
for prefix, items in prefix_groups.items():
    for j in cargo.uld:
        separation_penalty[prefix, j.index] = m.addVar(vtype=GRB.BINARY)
        m.addConstr(quicksum(p[i.index, j.index] for i in items) <= len(items) * separation_penalty[prefix, j.index])
```

#### Modified Model:
```python
# New SP variable approach (LaTeX equations)
booking_groups = cargo.get_prefix_groups()
SP = m.addVars(booking_groups.keys(), vtype=GRB.BINARY, name="SP")

# Upper bound: SP = 0 if all items in same ULD
m.addConstr(quicksum(p[i.index, j.index] for i in items) <= len(items) + M * (1 - SP[b_i]))

# Lower bound: SP = 1 if items separated
m.addConstr(quicksum(p[i.index, j.index] for i in items) >= len(items) - M * SP[b_i])
```

### 4. **Constraints**

#### New Constraints in Modified Model:

1. **R11 - Minimum volume utilization**:
```python
alpha = 0.2
for j in cargo.uld:
    if j.isNeitherBAXnorBUPnorT:
        m.addConstr(quicksum(i.volume * p[i.index, j.index] for i in cargo.items) >= alpha * j.volume * u[j.index])
```

2. **R12 - Item placement constraint** (modified):
```python
# Original: for j in cargo.uld
# Modified: for j in cargo.uld if j.isNeitherBAXnorBUPnorT
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] for j in cargo.uld if j.isNeitherBAXnorBUPnorT) == 1)
```

3. **R30-R31 - Separation constraints** (NEW):
```python
for b_i, items in booking_groups.items():
    for j in cargo.uld:
        if j.isNeitherBAXnorBUPnorT:
            m.addConstr(quicksum(p[i.index, j.index] for i in items) <= len(items) + M * (1 - SP[b_i]))
            m.addConstr(quicksum(p[i.index, j.index] for i in items) >= len(items) - M * SP[b_i])
```

#### Removed Constraints in Modified Model:

1. **Weight variable constraints** (w_ijt related constraints) - No longer needed since w variables removed
2. **Underutilization penalty constraints** - Replaced by new objective function

### 5. **Variable Simplification**

#### Original Model:
- Used `w[i.index, j.index, t.index]` for weight tracking
- Required complex linearization constraints

#### Modified Model:
- Directly uses `i.weight * z[i.index, j.index, t.index]`
- Eliminates need for weight variable constraints
- Reduces model complexity

### 6. **Special Handling Constraints**

#### Original Model:
- More complex COL/CRT constraints with additional variables
- Separate constraints for different aircraft types

#### Modified Model:
- Simplified COL/CRT constraints
- Cleaner implementation for Boeing 777 vs 787/781

## Impact on Performance

### Advantages of Modified Model:
1. **Reduced complexity**: Fewer variables and constraints
2. **Better separation logic**: More mathematically sound approach
3. **Improved volume utilization**: New minimum utilization constraint
4. **Cleaner code**: Better organization and comments

### Potential Issues:
1. **Separation constraints**: May cause infeasibility in some cases
2. **MAC impact**: New constraints may limit MAC optimization flexibility

## Recommendations

1. **Test separation constraints**: Verify they work correctly with your data
2. **Monitor MAC values**: Compare MAC optimization between models
3. **Validate results**: Ensure both models produce feasible solutions
4. **Consider hybrid approach**: Use modified model with option to disable separation constraints

## Conclusion

The modified model represents a significant improvement in terms of:
- Mathematical rigor (better separation logic)
- Code organization
- Constraint efficiency
- Volume utilization

However, the new separation constraints may need careful tuning to avoid infeasibility issues while maintaining good MAC optimization. 