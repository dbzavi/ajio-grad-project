# Metric Decomposition: Wishlist to Purchase Conversion

> [!NOTE]
> **Objective (Sub-Phase 3.1):** Break down the macro business metric (`Wishlist → Purchase Conversion`) into observable leading indicators and the core user behaviors driving them.

## Macro Metric
**Wishlist to Purchase Conversion Rate:** The total percentage of items added to a wishlist that are eventually purchased by the user.

---

## 1. Leading Indicators (Quantitative Tracking)
To improve the macro metric, we must track and influence these leading indicators:

- **Wishlist to Cart Conversion Rate (%):** The primary funnel step. Measures the percentage of wishlisted items successfully migrated to the active shopping cart.
- **Time to Conversion (Days/Hours):** The average duration an item sits in the wishlist before being purchased. A shorter duration indicates higher conviction.
- **Wishlist Return Visits:** The number of times a user views a wishlisted item without taking action. High return visits imply intent but unresolved friction (e.g., waiting for a sale, unsure of fit).
- **Wishlist Abandonment/Removal Rate (%):** The percentage of items deleted from the wishlist without a purchase. High rates may indicate frustration, out-of-stock issues, or finding alternatives elsewhere.
- **Cart Abandonment of Wishlisted Items (%):** Items moved to the cart but never checked out. Often caused by sudden trust deficits (e.g., hidden fees, delivery paranoia) at the final step.

---

## 2. Behavioral Drivers (Qualitative Context)
Based on the AI Discovery Engine's analysis of 1,000+ reviews, the leading indicators above are actively blocked by the following user behaviors and fears:

1. **Sizing Uncertainty (The Conviction Blocker)**
   - *Impacts:* Wishlist to Cart %
   - *Behavior:* Users lack confidence in the brand's fit. Because they anticipate a painful return process, they leave the item in the wishlist indefinitely rather than risking a purchase.

2. **Logistics & Delivery Paranoia (The Checkout Blocker)**
   - *Impacts:* Cart Abandonment %
   - *Behavior:* Even if a user loves an item, past experiences with fake delivery attempts or delayed refunds cause them to hesitate at the final step. The wishlist becomes a "safe" bookmarking tool rather than a shopping tool.

3. **Price Monitoring (The Waiting Game)**
   - *Impacts:* Time to Conversion
   - *Behavior:* Users explicitly use the wishlist as a financial tracking mechanism, intentionally delaying purchase until they observe a price drop or promotional event.

4. **Visual Trust Deficit (The Expectation Gap)**
   - *Impacts:* Wishlist Return Visits
   - *Behavior:* Users repeatedly view items but hesitate because they fear the real product won't match the studio photography. They wait for social validation or external reviews before converting.

5. **Platform UI Limits (The Forced Abandonment)**
   - *Impacts:* Wishlist Removal Rate
   - *Behavior:* Artificial limits (e.g., maximum 70 wishlist items) force high-intent users to delete products prematurely just to save new ones, directly cannibalizing future potential sales.

---

## 3. Insight Mapping Matrix (Sub-Phase 3.2)
Below is the direct mapping of the quantified AI Discovery themes to their corresponding business metrics, prioritized by occurrence frequency.

| Rank | Quantified Theme (from Sub-Phase 2.3) | Mentions | Primary Metric Impacted | Secondary Metric Impacted |
|:---:|---|:---:|---|---|
| **1** | **Sizing Uncertainty & Return Friction** | 587 | Wishlist to Cart % (Drop) | Wishlist Return Visits (Spike) |
| **2** | **Logistics & Delivery Paranoia** | 385 | Cart Abandonment % (Spike) | Wishlist Removal Rate % (Spike) |
| **3** | **Price & Offer Wait** | 249 | Time to Conversion (Spike) | Wishlist Return Visits (Spike) |
| **4** | **Visual Trust Deficit** | 214 | Wishlist Return Visits (Spike) | Wishlist to Cart % (Drop) |
| **5** | **Platform UI/UX & Wishlist Limit** | 207 | Wishlist Removal Rate % (Spike) | Time to Conversion (Drop due to deletion) |

---

## 4. Target Opportunity Selection (Sub-Phase 3.3)

> [!IMPORTANT]
> **Chosen Focus Area:** Sizing Uncertainty & Return Friction

### Rationale & Strategic Justification
After cross-referencing the AI-quantified frictions against our business constraints (specifically: *no monetary incentives allowed*), **Sizing Uncertainty** emerges as the highest-potential product opportunity.

1. **Volume of Friction:** With 587 explicit mentions, it is overwhelmingly the #1 reason users abandon their wishlists. 
2. **Direct Funnel Impact:** Uncertainty around fit directly destroys the *Wishlist to Cart %* leading indicator. Users keep items indefinitely bookmarked because they lack the conviction to buy.
3. **UX vs Operational:** Unlike "Logistics Paranoia" (which is fundamentally a supply-chain issue) or "Price Wait" (which violates the monetary incentive constraint), sizing conviction can be solved almost entirely through innovative digital Product and UX interventions.
4. **Fear of Returns:** Users explicitly avoid purchasing because they dread the operational friction of the return process. If we can guarantee sizing confidence *before* checkout, we bypass this fear entirely.

By focusing our MVP on solving **Sizing Uncertainty**, we tackle the largest psychological blocker preventing users from migrating high-intent wishlist items into their carts.
