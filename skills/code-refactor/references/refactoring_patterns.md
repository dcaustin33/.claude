# Refactoring Patterns Reference

This document provides detailed examples of common refactoring patterns with before/after code samples.

## Table of Contents

1. [Extract Function](#extract-function)
2. [Consolidate Duplicate Conditionals](#consolidate-duplicate-conditionals)
3. [Replace Magic Numbers with Constants](#replace-magic-numbers-with-constants)
4. [Extract Helper Functions from Loops](#extract-helper-functions-from-loops)
5. [Reduce Nesting with Guard Clauses](#reduce-nesting-with-guard-clauses)
6. [Consolidate Similar Functions](#consolidate-similar-functions)
7. [Extract Method Object](#extract-method-object)
8. [Replace Conditional with Lookup Table](#replace-conditional-with-lookup-table)
9. [Comment Cleanup Patterns](#comment-cleanup-patterns)

---

## Extract Function

**When to use:** Code block appears 2+ times, or complex logic needs a descriptive name

### Python Example

**Before:**
```python
def process_orders(orders):
    for order in orders:
        # Calculate total
        subtotal = sum(item['price'] * item['quantity'] for item in order['items'])
        tax = subtotal * 0.08
        shipping = 10 if subtotal < 50 else 0
        total = subtotal + tax + shipping
        order['total'] = total
        
        # Validate
        if total < 0:
            raise ValueError("Invalid total")
        if not order['customer_email']:
            raise ValueError("Missing email")
        
        # Save
        database.save(order)

def create_invoice(order):
    # Calculate total (DUPLICATE)
    subtotal = sum(item['price'] * item['quantity'] for item in order['items'])
    tax = subtotal * 0.08
    shipping = 10 if subtotal < 50 else 0
    total = subtotal + tax + shipping
    
    return generate_pdf(order, total)
```

**After:**
```python
def calculate_order_total(order):
    """Calculate order total including tax and shipping"""
    subtotal = sum(item['price'] * item['quantity'] for item in order['items'])
    tax = subtotal * 0.08
    shipping = 10 if subtotal < 50 else 0
    return subtotal + tax + shipping

def validate_order(order):
    """Validate order has required fields and valid total"""
    if order['total'] < 0:
        raise ValueError("Invalid total")
    if not order['customer_email']:
        raise ValueError("Missing email")

def process_orders(orders):
    for order in orders:
        order['total'] = calculate_order_total(order)
        validate_order(order)
        database.save(order)

def create_invoice(order):
    total = calculate_order_total(order)
    return generate_pdf(order, total)
```

**Benefits:** Eliminated 15+ lines of duplication, improved testability, clearer intent

---

## Consolidate Duplicate Conditionals

**When to use:** Same conditional logic appears in multiple places

### JavaScript Example

**Before:**
```javascript
function getUserPermissions(user) {
    if (user.role === 'admin') {
        return ['read', 'write', 'delete', 'admin'];
    } else if (user.role === 'editor') {
        return ['read', 'write'];
    } else if (user.role === 'viewer') {
        return ['read'];
    } else {
        return [];
    }
}

function canDeletePost(user) {
    if (user.role === 'admin') {
        return true;
    } else if (user.role === 'editor') {
        return false;
    } else if (user.role === 'viewer') {
        return false;
    } else {
        return false;
    }
}

function getUserDashboard(user) {
    if (user.role === 'admin') {
        return 'admin_dashboard';
    } else if (user.role === 'editor') {
        return 'editor_dashboard';
    } else if (user.role === 'viewer') {
        return 'viewer_dashboard';
    } else {
        return 'default_dashboard';
    }
}
```

**After:**
```javascript
const ROLE_PERMISSIONS = {
    admin: ['read', 'write', 'delete', 'admin'],
    editor: ['read', 'write'],
    viewer: ['read'],
    default: []
};

const ROLE_DASHBOARDS = {
    admin: 'admin_dashboard',
    editor: 'editor_dashboard',
    viewer: 'viewer_dashboard',
    default: 'default_dashboard'
};

function getUserPermissions(user) {
    return ROLE_PERMISSIONS[user.role] || ROLE_PERMISSIONS.default;
}

function canDeletePost(user) {
    return getUserPermissions(user).includes('delete');
}

function getUserDashboard(user) {
    return ROLE_DASHBOARDS[user.role] || ROLE_DASHBOARDS.default;
}
```

**Benefits:** Reduced 40+ lines to 20, centralized role configuration, easier to add new roles

---

## Replace Magic Numbers with Constants

**When to use:** Numeric literals appear multiple times or lack clear meaning

### Java Example

**Before:**
```java
public class PricingCalculator {
    public double calculatePrice(int quantity) {
        double basePrice = quantity * 29.99;
        if (quantity > 10) {
            basePrice *= 0.9;
        }
        if (quantity > 50) {
            basePrice *= 0.85;
        }
        return basePrice * 1.08; // tax
    }
    
    public boolean isEligibleForDiscount(int quantity) {
        return quantity > 10;
    }
    
    public String getShippingSpeed(double orderTotal) {
        if (orderTotal > 100) {
            return "EXPRESS";
        }
        return "STANDARD";
    }
}
```

**After:**
```java
public class PricingCalculator {
    private static final double UNIT_PRICE = 29.99;
    private static final double TAX_RATE = 1.08;
    private static final int BULK_DISCOUNT_THRESHOLD = 10;
    private static final double BULK_DISCOUNT_RATE = 0.9;
    private static final int VOLUME_DISCOUNT_THRESHOLD = 50;
    private static final double VOLUME_DISCOUNT_RATE = 0.85;
    private static final double EXPRESS_SHIPPING_THRESHOLD = 100.0;
    
    public double calculatePrice(int quantity) {
        double basePrice = quantity * UNIT_PRICE;
        
        if (quantity > BULK_DISCOUNT_THRESHOLD) {
            basePrice *= BULK_DISCOUNT_RATE;
        }
        if (quantity > VOLUME_DISCOUNT_THRESHOLD) {
            basePrice *= VOLUME_DISCOUNT_RATE;
        }
        
        return basePrice * TAX_RATE;
    }
    
    public boolean isEligibleForDiscount(int quantity) {
        return quantity > BULK_DISCOUNT_THRESHOLD;
    }
    
    public String getShippingSpeed(double orderTotal) {
        if (orderTotal > EXPRESS_SHIPPING_THRESHOLD) {
            return "EXPRESS";
        }
        return "STANDARD";
    }
}
```

**Benefits:** Self-documenting code, easy to update values, no magic numbers

---

## Extract Helper Functions from Loops

**When to use:** Loop body is complex or performs multiple distinct operations

### Python Example

**Before:**
```python
def process_user_data(users):
    results = []
    for user in users:
        # Validate email
        if not user.get('email'):
            continue
        if '@' not in user['email']:
            continue
        if len(user['email']) < 5:
            continue
            
        # Normalize name
        name_parts = user['name'].split()
        if len(name_parts) >= 2:
            first = name_parts[0].strip().capitalize()
            last = ' '.join(name_parts[1:]).strip().capitalize()
            full_name = f"{first} {last}"
        else:
            full_name = user['name'].strip().capitalize()
        
        # Calculate score
        score = 0
        if user.get('verified'):
            score += 50
        if user.get('premium'):
            score += 30
        if len(user.get('posts', [])) > 10:
            score += 20
            
        results.append({
            'email': user['email'],
            'name': full_name,
            'score': score
        })
    return results
```

**After:**
```python
def is_valid_email(email):
    """Check if email meets basic validation criteria"""
    if not email:
        return False
    if '@' not in email:
        return False
    if len(email) < 5:
        return False
    return True

def normalize_name(raw_name):
    """Normalize user name to proper capitalization"""
    name_parts = raw_name.split()
    if len(name_parts) >= 2:
        first = name_parts[0].strip().capitalize()
        last = ' '.join(name_parts[1:]).strip().capitalize()
        return f"{first} {last}"
    return raw_name.strip().capitalize()

def calculate_user_score(user):
    """Calculate user engagement score based on various factors"""
    score = 0
    if user.get('verified'):
        score += 50
    if user.get('premium'):
        score += 30
    if len(user.get('posts', [])) > 10:
        score += 20
    return score

def process_user_data(users):
    results = []
    for user in users:
        if not is_valid_email(user.get('email')):
            continue
            
        results.append({
            'email': user['email'],
            'name': normalize_name(user['name']),
            'score': calculate_user_score(user)
        })
    return results
```

**Benefits:** 45 lines → 35 lines, much more readable loop, testable helper functions

---

## Reduce Nesting with Guard Clauses

**When to use:** Deep nesting (3+ levels) makes code hard to follow

### TypeScript Example

**Before:**
```typescript
function processPayment(order: Order): PaymentResult {
    if (order) {
        if (order.items && order.items.length > 0) {
            if (order.customer) {
                if (order.customer.paymentMethod) {
                    const total = calculateTotal(order);
                    if (total > 0) {
                        if (order.customer.balance >= total) {
                            order.customer.balance -= total;
                            return { success: true, message: "Payment processed" };
                        } else {
                            return { success: false, message: "Insufficient funds" };
                        }
                    } else {
                        return { success: false, message: "Invalid total" };
                    }
                } else {
                    return { success: false, message: "No payment method" };
                }
            } else {
                return { success: false, message: "No customer" };
            }
        } else {
            return { success: false, message: "Empty order" };
        }
    } else {
        return { success: false, message: "No order" };
    }
}
```

**After:**
```typescript
function processPayment(order: Order): PaymentResult {
    // Guard clauses handle invalid states early
    if (!order) {
        return { success: false, message: "No order" };
    }
    
    if (!order.items || order.items.length === 0) {
        return { success: false, message: "Empty order" };
    }
    
    if (!order.customer) {
        return { success: false, message: "No customer" };
    }
    
    if (!order.customer.paymentMethod) {
        return { success: false, message: "No payment method" };
    }
    
    const total = calculateTotal(order);
    if (total <= 0) {
        return { success: false, message: "Invalid total" };
    }
    
    if (order.customer.balance < total) {
        return { success: false, message: "Insufficient funds" };
    }
    
    // Happy path at the end with minimal nesting
    order.customer.balance -= total;
    return { success: true, message: "Payment processed" };
}
```

**Benefits:** Reduced max nesting from 7 to 1, easier to read, clear error cases

---

## Consolidate Similar Functions

**When to use:** Multiple functions differ only in parameters or minor logic

### Python Example

**Before:**
```python
def get_active_users():
    return db.query("SELECT * FROM users WHERE status = 'active'")

def get_inactive_users():
    return db.query("SELECT * FROM users WHERE status = 'inactive'")

def get_pending_users():
    return db.query("SELECT * FROM users WHERE status = 'pending'")

def get_admin_users():
    return db.query("SELECT * FROM users WHERE role = 'admin'")

def get_editor_users():
    return db.query("SELECT * FROM users WHERE role = 'editor'")
```

**After:**
```python
def get_users_by_status(status):
    """Get users filtered by status"""
    return db.query("SELECT * FROM users WHERE status = ?", (status,))

def get_users_by_role(role):
    """Get users filtered by role"""
    return db.query("SELECT * FROM users WHERE role = ?", (role,))

# Or even more general:
def get_users(filter_field=None, filter_value=None):
    """Get users with optional filtering"""
    if filter_field and filter_value:
        return db.query(
            f"SELECT * FROM users WHERE {filter_field} = ?",
            (filter_value,)
        )
    return db.query("SELECT * FROM users")
```

**Benefits:** Reduced 5 functions to 1-2, eliminated repetitive code

---

## Extract Method Object

**When to use:** Long function with many local variables that's hard to break down

### Java Example

**Before:**
```java
public Report generateSalesReport(Date startDate, Date endDate) {
    // 80+ lines of complex logic with many local variables
    List<Sale> sales = getSales(startDate, endDate);
    double totalRevenue = 0;
    Map<String, Double> revenueByProduct = new HashMap<>();
    Map<String, Integer> unitsByProduct = new HashMap<>();
    // ... many more local variables
    
    for (Sale sale : sales) {
        // Complex calculations
        totalRevenue += sale.getAmount();
        // ... many more lines
    }
    
    // More complex processing
    // ...
    
    return new Report(totalRevenue, revenueByProduct, unitsByProduct);
}
```

**After:**
```java
public Report generateSalesReport(Date startDate, Date endDate) {
    SalesReportGenerator generator = new SalesReportGenerator(startDate, endDate);
    return generator.generate();
}

private class SalesReportGenerator {
    private final Date startDate;
    private final Date endDate;
    private double totalRevenue = 0;
    private Map<String, Double> revenueByProduct = new HashMap<>();
    private Map<String, Integer> unitsByProduct = new HashMap<>();
    
    public SalesReportGenerator(Date startDate, Date endDate) {
        this.startDate = startDate;
        this.endDate = endDate;
    }
    
    public Report generate() {
        List<Sale> sales = getSales(startDate, endDate);
        processSales(sales);
        return buildReport();
    }
    
    private void processSales(List<Sale> sales) {
        for (Sale sale : sales) {
            processSale(sale);
        }
    }
    
    private void processSale(Sale sale) {
        totalRevenue += sale.getAmount();
        updateProductMetrics(sale);
    }
    
    private void updateProductMetrics(Sale sale) {
        String product = sale.getProduct();
        revenueByProduct.merge(product, sale.getAmount(), Double::sum);
        unitsByProduct.merge(product, sale.getQuantity(), Integer::sum);
    }
    
    private Report buildReport() {
        return new Report(totalRevenue, revenueByProduct, unitsByProduct);
    }
}
```

**Benefits:** Long function broken into cohesive, testable methods

---

## Replace Conditional with Lookup Table

**When to use:** Long if-else chains or switch statements with simple mappings

### JavaScript Example

**Before:**
```javascript
function getDiscountRate(customerType, orderAmount) {
    let discount = 0;
    
    if (customerType === 'gold') {
        if (orderAmount > 1000) {
            discount = 0.20;
        } else if (orderAmount > 500) {
            discount = 0.15;
        } else {
            discount = 0.10;
        }
    } else if (customerType === 'silver') {
        if (orderAmount > 1000) {
            discount = 0.15;
        } else if (orderAmount > 500) {
            discount = 0.10;
        } else {
            discount = 0.05;
        }
    } else if (customerType === 'bronze') {
        if (orderAmount > 1000) {
            discount = 0.10;
        } else {
            discount = 0.05;
        }
    } else {
        discount = 0;
    }
    
    return discount;
}
```

**After:**
```javascript
const DISCOUNT_RATES = {
    gold: [
        { threshold: 1000, rate: 0.20 },
        { threshold: 500, rate: 0.15 },
        { threshold: 0, rate: 0.10 }
    ],
    silver: [
        { threshold: 1000, rate: 0.15 },
        { threshold: 500, rate: 0.10 },
        { threshold: 0, rate: 0.05 }
    ],
    bronze: [
        { threshold: 1000, rate: 0.10 },
        { threshold: 0, rate: 0.05 }
    ]
};

function getDiscountRate(customerType, orderAmount) {
    const tiers = DISCOUNT_RATES[customerType];
    if (!tiers) return 0;
    
    const tier = tiers.find(t => orderAmount >= t.threshold);
    return tier ? tier.rate : 0;
}
```

**Benefits:** 30+ lines → 10 lines, data-driven, easy to modify rates

---

## Comment Cleanup Patterns

### Remove Obvious Comments

**Before:**
```python
# Increment counter
counter += 1

# Loop through users
for user in users:
    # Get user name
    name = user.name
    # Print name
    print(name)

# Return result
return result
```

**After:**
```python
counter += 1

for user in users:
    name = user.name
    print(name)

return result
```

### Keep Valuable Comments

**Good comments explain WHY, not WHAT:**

```python
# Using binary search because the list is sorted and can be very large (millions of items)
index = binary_search(sorted_list, target)

# Retry logic: API occasionally returns 429, but succeeds on retry
# Historical data shows 3 retries is sufficient for 99.9% of cases
for attempt in range(3):
    response = api_call()
    if response.status_code != 429:
        break
    time.sleep(2 ** attempt)  # Exponential backoff

# IMPORTANT: This must run before database commit to maintain data consistency
# See ticket #1234 for context on why this ordering matters
validate_constraints()
db.commit()
```

### Update Outdated Comments

**Before:**
```javascript
// TODO: Add error handling (status: outdated - completed in v2.0)
function processData(data) {
    try {
        return transform(data);
    } catch (error) {
        handleError(error);
    }
}
```

**After:**
```javascript
function processData(data) {
    try {
        return transform(data);
    } catch (error) {
        handleError(error);
    }
}
```

---

## Quick Reference: When to Extract a Function

Extract a function when:
- ✅ Code block appears 2+ times
- ✅ Complex logic needs a descriptive name
- ✅ Function is getting too long (>50 lines)
- ✅ Code block has a clear, singular purpose
- ✅ Logic could be tested independently
- ✅ Nesting is deep (>3 levels)

Don't extract when:
- ❌ Used only once and simple
- ❌ Would require passing many parameters (>4)
- ❌ Extraction would obscure rather than clarify
- ❌ The extraction is purely mechanical without improving understanding
