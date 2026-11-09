# Medical Billing Mathematical Framework & Cost-Sharing Formulas
## Technical Specification – Week 2 Billing Simulation

---

### 1. Fundamental Revenue Cycle Equations

The financial integrity of healthcare accounting relies on standard double-entry ledger reconciliation operating across two distinct accounting tiers:

#### Tier 1: Line-Level Adjudication Equation (Per Service Line)
For every medical service evaluated through a third-party payer contract:

$$\text{Gross Charge} = \text{Contractual Adjustment} + \text{Denied Amount} + \text{Payer Allowed Amount}$$

Where the **Payer Allowed Amount** represents the total enforceable reimbursement for the service:

$$\text{Payer Allowed Amount} = \text{Payer Paid} + \text{Patient Responsibility}$$

- **Covered / Approved Service:** $\text{Denied Amount} = \$0.00$. The gross charge is partitioned between contractual fee schedule write-off ($\Delta_{\text{contract}} = C_{\text{gross}} - A_{\text{allowed}}$) and allowable revenue ($A_{\text{allowed}}$).
- **Denied Service (CARC 50, 197, 18):** $A_{\text{allowed}} = \$0.00$, $\Delta_{\text{contract}} = \$0.00$, and $\text{Denied Amount} = C_{\text{gross}}$.

#### Tier 2: Cohort Master Reconciliation Equation (Practice Population)
Across the entire practice population, gross billed charges must account for all operational states, explicitly distinguishing pre-adjudication clearinghouse rejections from adjudicated claims:

$$\text{Total Gross Billed} = \text{Adjudicated Gross Charges} + \text{Clearinghouse Rejected Charges}$$
$$\$5,190.00 = \$4,820.00 + \$370.00$$

Where:
$$\begin{aligned}
\text{Adjudicated Gross } (\$4,820.00) &= \text{Allowed } (\$1,412.70) + \text{Contractual Adjustments } (\$1,322.30) + \text{Denied Charges } (\$2,085.00) \\
\text{Allowed Amount } (\$1,412.70) &= \text{Insurer Paid } (\$614.96) + \text{Patient Responsibility } (\$797.74) \\
\text{Patient Responsibility } (\$797.74) &= \text{Deductible } (\$498.00) + \text{Copays } (\$80.00) + \text{Coinsurance } (\$90.24) + \text{Self-Pay } (\$129.50)
\end{aligned}$$

**Resolution of the $370.00 Discrepancy:**
Claims rejected at clearinghouse intake prior to payer transmission (ENC-2010 $185.00 for missing policy ID; ENC-2014 $185.00 for unsigned progress note) total exactly **$370.00**. Because these claims were intercepted at the gateway via EDI 277CA (Status Category A7) and never underwent payer adjudication, they have $0.00 allowed amount and $0.00 contractual adjustments. Omitting them from gross billed reconciliation created an apparent $370.00 gap ($5,190.00 gross vs. $4,820.00 adjudicated sum). Isolating unadjudicated gateway rejections ($370.00) resolves the reconciliation completely to the penny.

---

### 2. Variables & Parameter Definitions

| Variable | Description | Source / Determinant |
| :--- | :--- | :--- |
| $C_{\text{gross}}$ | Gross Billed Charge | Facility or Practice Chargemaster (CDM) |
| $A_{\text{allowed}}$ | Payer Allowable Maximum | Contracted Fee Schedule between Payer and Provider |
| $\Delta_{\text{contract}}$ | Contractual Adjustment / Write-Off | Calculated: $C_{\text{gross}} - A_{\text{allowed}}$ on covered lines (CARC 45) |
| $\Delta_{\text{denied}}$ | Clinical / Administrative Denial | Non-covered service charge (CARC 50, 197, 18) |
| $\Delta_{\text{rejected}}$ | Clearinghouse Gateway Rejection | Unadjudicated pre-bill stop (CARC 16) |
| $D_{\text{rem}}$ | Patient Remaining Annual Deductible | Accumulated benefit year accumulator (EDI 271) |
| $D_{\text{applied}}$ | Deductible Applied to Service | Calculated portion of $A_{\text{allowed}}$ allocated to deductible (CARC 1) |
| $CP$ | Fixed Office Visit Copayment | Plan benefit design for service type (CARC 3) |
| $r_{\text{coin}}$ | Patient Coinsurance Rate (%) | Contract percentage (e.g., 20% for Medicare Part B) (CARC 2) |
| $CI$ | Calculated Coinsurance Amount | Calculated portion of post-deductible allowable (CARC 2) |
| $OOPM_{\text{rem}}$ | Remaining Out-of-Pocket Maximum | Maximum legal patient out-of-pocket cap per benefit year |
| $R_{\text{patient}}$ | Total Patient Responsibility | Total billed to patient on invoice |
| $P_{\text{payer}}$ | Net Payer Remittance | Cash disbursement paid to provider by health plan |


---

### 3. Step-by-Step Cost-Sharing Waterfall Engine

To eliminate duplicate liability and guarantee mathematical reconciliation down to the exact penny, cost-sharing allocations must follow a strict sequential order of operations:

```
                  [Payer Allowed Amount]
                             │
            ┌────────────────┴────────────────┐
            │ Plan Has Copay?                 │
            ├──────────────┬──────────────────┤
          [YES]           [NO]                │
            │              │                  │
    Deduct Copay           ▼                  │
    from Allowed:    Check Remaining          │
    Balance =        Deductible               │
    Allowed - Copay        │                  │
            │              │                  │
            └──────┬───────┘                  │
                   ▼                          │
        [Apply Deductible]                    │
        D_applied = min(Balance, D_rem)       │
                   │                          │
                   ▼                          │
         [Calculate Coinsurance]              │
         Post-Deductible Balance =            │
         Balance - D_applied                  │
         Coinsurance = Post-Bal * r_coin      │
                   │                          │
                   ▼                          │
         [Apply OOPM Cap]                     │
         Pt_Cost = Copay + D_applied + Coin   │
         Pt_Final = min(Pt_Cost, OOPM_rem)    │
                   │                          │
                   ▼                          │
         [Calculate Payer Paid]               │
         Payer_Paid = Allowed - Pt_Final      │
```

#### Step 1: Fixed Copayment Allocation
If the subscriber's benefit plan mandates a fixed copayment for outpatient office visits:
$$CP_{\text{applied}} = \min(CP, A_{\text{allowed}})$$
The remaining allowed balance subject to further cost-sharing is:
$$A_{\text{remaining}} = A_{\text{allowed}} - CP_{\text{applied}}$$

*Note:* In standard PPO and HMO commercial designs, office visits subject to a fixed copayment typically waive the deductible for the Evaluation and Management (E/M) service.

#### Step 2: Deductible Allocation
If the plan applies an annual calendar-year deductible:
$$D_{\text{applied}} = \min(A_{\text{remaining}}, D_{\text{rem}})$$
The updated remaining allowable balance after deductible is:
$$A_{\text{post-ded}} = A_{\text{remaining}} - D_{\text{applied}}$$
The patient's remaining annual deductible accumulator is simultaneously updated:
$$D_{\text{rem, new}} = \max(0, D_{\text{rem}} - D_{\text{applied}})$$

#### Step 3: Coinsurance Allocation
For plans with percentage cost-sharing (e.g., 80/20 PPO, Medicare Part B), coinsurance applies solely to the post-deductible allowable balance:
$$CI = A_{\text{post-ded}} \times r_{\text{coin}}$$

#### Step 4: Out-of-Pocket Maximum (OOPM) Cap Enforcement
The total preliminary patient liability is summed:
$$R_{\text{prelim}} = CP_{\text{applied}} + D_{\text{applied}} + CI$$
To protect the patient under Affordable Care Act (ACA) and ERISA statutory protections, this liability cannot exceed the patient's remaining out-of-pocket maximum:
$$R_{\text{patient}} = \min(R_{\text{prelim}}, OOPM_{\text{rem}})$$

If $R_{\text{prelim}} > OOPM_{\text{rem}}$, the excess is absorbed by the payer:
$$\Delta_{\text{oopm}} = R_{\text{prelim}} - OOPM_{\text{rem}}$$

#### Step 5: Net Payer Remittance Calculation
The net cash amount paid by the insurer to the provider is:
$$P_{\text{payer}} = A_{\text{allowed}} - R_{\text{patient}}$$

---

### 4. Mathematical Identity Proof (Zero Double-Counting)

#### Theorem:
Under all normal adjudication conditions, the sum of insurance payment and patient responsibility identically equals the contractual allowable amount:
$$P_{\text{payer}} + R_{\text{patient}} \equiv A_{\text{allowed}}$$

#### Algebraic Proof:
1. From Step 5: $P_{\text{payer}} = A_{\text{allowed}} - R_{\text{patient}}$
2. Rearranging terms: $P_{\text{payer}} + R_{\text{patient}} = (A_{\text{allowed}} - R_{\text{patient}}) + R_{\text{patient}} = A_{\text{allowed}}$
3. Adding Contractual Adjustment $\Delta_{\text{contract}} = C_{\text{gross}} - A_{\text{allowed}}$ to both sides:
   $$\Delta_{\text{contract}} + P_{\text{payer}} + R_{\text{patient}} = (C_{\text{gross}} - A_{\text{allowed}}) + A_{\text{allowed}} = C_{\text{gross}}$$
4. $\mathbb{Q.E.D.}$

This mathematical invariant prevents any double-counting or unallocated revenue across every processed encounter in the simulation.

---

### 5. Adjudication Rules for Special Edge Cases

#### Case A: In-Network Administrative Denial (CARC 197 / CARC 50 / CARC 18)
* **Trigger:** Absence of mandatory pre-authorization or specialist referral (CARC 197), failure of medical necessity documentation (CARC 50), or duplicate billing (CARC 18).
* **Network Status:** Participating / In-Network Provider Contract.
* **Legal/Contractual Constraint:** In-network provider agreements forbid balance-billing patients for provider administrative errors.
* **Formulas Applied:**
  $$A_{\text{allowed}} = \$0.00$$
  $$P_{\text{payer}} = \$0.00$$
  $$R_{\text{patient}} = \$0.00 \quad \text{(Held pending administrative appeal; patient held harmless)}$$
  $$\Delta_{\text{contract}} = \$0.00 \quad \text{(Fee schedule contractual write-offs apply only to covered lines)}$$
  $$\Delta_{\text{denied}} = C_{\text{gross}} \quad \text{(Gross charge classified as payer denial)}$$

#### Case B: Service Downcoding / Level Reduction (CARC 150)
* **Trigger:** Provider bills high-complexity service (e.g., CPT 99215 @ $395.00 gross, $230.00 allowed), but clinical documentation only supports moderate complexity (CPT 99213 @ $115.00 allowed).
* **Formulas Applied:**
  $$A_{\text{adjudicated}} = A_{\text{downcoded}} = \$115.00$$
  $$\Delta_{\text{contract}} = C_{\text{gross}} - A_{\text{downcoded}} = \$395.00 - \$115.00 = \$280.00$$
  $$R_{\text{patient}} = \text{CostSharing}(A_{\text{downcoded}})$$
  $$P_{\text{payer}} = A_{\text{downcoded}} - R_{\text{patient}}$$

#### Case C: Pre-Submission Clearinghouse Rejection (EDI 277CA STC: A7 / CARC 16)
* **Trigger:** Missing subscriber policy ID (ENC-2010) or missing clinician electronic signature (ENC-2014).
* **Formulas Applied:**
  * Claim is intercepted at the clearinghouse gateway via EDI 277CA (Status Category Code STC: A7) and placed in `Rejected – Resubmission Required` status.
  * In practice management systems, these front-end stops are mapped to CARC 16 workqueues for staff correction.
  * No ERA 835 is generated; claim remains unadjudicated by the health plan.
  * No contractual write-off or patient balance billing occurs until corrections are completed and retransmitted.
  $$P_{\text{payer}} = \$0.00, \quad R_{\text{patient}} = \$0.00, \quad \Delta_{\text{contract}} = \$0.00, \quad \Delta_{\text{rejected}} = C_{\text{gross}}$$

#### Case D: Self-Pay / Uninsured Patient
* **Trigger:** No third-party insurance coverage on file.
* **Formulas Applied:**
  $$A_{\text{allowed}} = C_{\text{gross}} \times (1 - \text{Discount Rate}) = \$185.00 \times (1 - 0.30) = \$129.50$$
  $$P_{\text{payer}} = \$0.00$$
  $$\Delta_{\text{contract}} = \$185.00 - \$129.50 = \$55.50 \quad \text{(Prompt-pay financial discount)}$$
  $$R_{\text{patient}} = A_{\text{allowed}} = \$129.50$$

---

### 6. Worked Numerical Examples from Simulation Cohort

#### Example 1: High Deductible HDHP Office Visit (ENC-2004)
* **Patient:** Sophia Chen | **Plan:** Cigna HDHP
* **CPT:** 99213 (Established Patient Level 3)
* **Deductible Status:** $2,500.00 Annual Deductible, $850.00 Remaining.
* **Parameters:** Gross = $185.00, Allowed = $112.00, Copay = $0, Deductible Remaining = $850.00.
* **Calculation:**
  1. $\Delta_{\text{contract}} = \$185.00 - \$112.00 = \$73.00$
  2. $D_{\text{applied}} = \min(\$112.00, \$850.00) = \$112.00$
  3. $A_{\text{post-ded}} = \$112.00 - \$112.00 = \$0.00$
  4. $CI = \$0.00 \times 10\% = \$0.00$
  5. $R_{\text{patient}} = \$112.00$
  6. $P_{\text{payer}} = \$112.00 - \$112.00 = \$0.00$
* **Verification:** $\$0.00 \text{ (Ins)} + \$112.00 \text{ (Pt)} = \$112.00 \text{ (Allowed)}$. $\checkmark$

#### Example 2: Medicare Part B 80/20 Coinsurance (ENC-2002)
* **Patient:** Eleanor Vance | **Plan:** Medicare Part B
* **CPT:** 99214 ($275.00 gross, $138.50 allowed), 36415 ($20.00 gross, $12.00 allowed). Total Gross = $295.00, Total Allowed = $150.50.
* **Deductible Status:** $240.00 Annual Deductible, Met ($0.00 Remaining).
* **Parameters:** Gross = $295.00, Allowed = $150.50, Copay = $0, Deductible Remaining = $0.00, Coinsurance = 20%.
* **Calculation:**
  1. $\Delta_{\text{contract}} = \$295.00 - \$150.50 = \$144.50$
  2. $D_{\text{applied}} = \$0.00$
  3. $CI = \$150.50 \times 20\% = \$30.10$
  4. $R_{\text{patient}} = \$30.10$
  5. $P_{\text{payer}} = \$150.50 - \$30.10 = \$120.40$
* **Verification:** $\$120.40 \text{ (Ins)} + \$30.10 \text{ (Pt)} = \$150.50 \text{ (Allowed)}$. $\checkmark$

#### Example 3: In-Network HMO Referral Denial (ENC-2008)
* **Patient:** Maria Santos | **Plan:** Aetna HMO
* **CPT:** 99204 (New Patient Level 4 - Specialist Visit)
* **Adjudication:** Missing specialist referral on file $\rightarrow$ CARC 197 Denial.
* **Parameters:** Gross = $360.00, Allowed = $0.00.
* **Calculation:**
  1. $A_{\text{allowed}} = \$0.00$
  2. $P_{\text{payer}} = \$0.00$
  3. $R_{\text{patient}} = \$0.00$ (In-network administrative hold; patient protected)
  4. $\Delta_{\text{contract}} = \$0.00$ (Fee schedule write-off not applied to denied claim)
  5. $\Delta_{\text{denied}} = \$360.00$ (Categorized as payer denial)
* **Verification:** $\$0.00 \text{ (Ins)} + \$0.00 \text{ (Pt)} = \$0.00 \text{ (Allowed)}$. $\checkmark$
* **Ledger Invariant:** $\Delta_{\text{contract}} (\$0.00) + \Delta_{\text{denied}} (\$360.00) + A_{\text{allowed}} (\$0.00) = C_{\text{gross}} (\$360.00)$. $\checkmark$

