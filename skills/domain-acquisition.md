# Domain Acquisition and Long-Term Registration

Use when researching, purchasing, transferring, renewing, or safeguarding internet domain registrations. Optimize **total cost of ownership and continuity**, not the promotional first-year price. This is provider-neutral; Cloudflare Registrar is one candidate, not a mandatory destination.

## Trigger and scope

Apply to a single name, TLD portfolio, or domain procurement policy. Never embed a particular customer's domain, availability result, live quote, account or contact details in this reusable skill. Keep current prices, policies and registry rules as separately verified evidence for the active task.

## Evidence before recommendation

1. Identify intended use, time horizon, acceptable TLDs, currency/tax jurisdiction, legal presence constraints, DNS hosting needs, ownership entity, and recovery requirements. Proceed with sensible explicit assumptions if preferences are unspecified.
2. Confirm the **exact full domain** via authoritative registrar/registry availability check immediately before purchase; web search, lack of a website, DNS/WHOIS absence or generic TLD price never proves availability.
3. Confirm whether the exact name is **standard, premium, reserved, unavailable or aftermarket**. Premium purchase and premium renewal can differ; aftermarket listing price is not the registration rate.
4. Inspect official registrar price/checkout/API for the exact name and TLD, noting date, source, currency, registration, renewal, transfer, restoration, ICANN/registry fees, taxes, discounts, restrictions and potential future increases. Favor registrar/registry and ICANN policy over comparison aggregators.
5. Confirm Cloudflare Registrar support **for registration and for transfer separately**; use its official TLD list and exact-domain registration/transfer eligibility checks. Cloudflare DNS availability alone does not imply Registrar support. API limitations may differ from dashboard eligibility.

## Compare acquisition strategies

Compute comparable total paid to reach a target expiration date, not merely a sum of annual headline rates:

- **Direct multi-year registration:** first-year registration rate plus additional-year rates, mandatory charges and applicable tax, subject to TLD term limits.
- **Promo registration then transfer:** discounted first year at registrar A + Cloudflare transfer fee (often adds one year) + further Cloudflare renewal years needed to reach the *same target expiry* + taxes and ancillary costs.
- **Remain with initial registrar:** promotional first-year charge + exact long-term renewal rates/fees, optionally paying multiple years upfront.
- **Alternative registrar:** compare its real renewal pricing, legal requirements, DNS flexibility, account security, support and exit fees rather than assuming Cloudflare is cheapest.

For each option report initial cash paid, total for target 5/10-year horizons, expiry achieved, included transfer-added years, assumptions and break-even. Do not double-count transfer years. Account for already-paid existing registration time on transfer; certain transfers may add **zero** years, especially for ccTLDs. Many gTLDs cap remaining registration term at ten years; actual limits are TLD-specific. Buying ahead locks prepaid term, **not** future registry renewal prices.

Cloudflare's 'at cost' means registry and applicable ICANN charges without Cloudflare markup; it does not imply low wholesale pricing. If a premium, registry eligibility, tax or payment detail is unknown, label the comparison provisional and do not invent exact savings.

## Transfer safety decision gate

Before recommending a registrar-to-registrar transfer, verify all:

- The TLD and exact domain are transferable to the destination and the gaining registrar supports that operation.
- The initial registration / previous transfer is outside any applicable 60-day lock; registrant contact changes can impose another lock. Apply actual registry/ICANN rules, not universal assumptions for ccTLDs.
- Check recent expiry/renewal: after a domain's expiration and renewal at the losing registrar, an early transfer can result in **no additional year** under registry rules; Cloudflare advises waiting at least 45 days after original expiry in that scenario.
- Existing DNS records (including MX, TXT/SPF, DKIM, DMARC, CAA, SRV), DNSSEC/DS and nameservers are inventoried and backed up. Cloudflare Registrar requires **Cloudflare authoritative DNS**, so confirm this is compatible before migrating.
- Ensure the destination account has verified email, usable payment method, accurate registrant information and eligibility for any country-code nexus/residency requirements.
- Confirm EPP/AuthInfo availability and registrar lock state. Handle authorization codes as secrets. Never expose tokens, auth codes, personal contact data or billing details in reports.
- Have tested rollback/recovery instructions for DNS cutover and a transfer-status check. DNS migration and registrar transfer are distinct operations; transfer alone does not necessarily move websites or email.

Cloudflare-specific sequence, **only when eligibility is confirmed**: add domain to Cloudflare DNS; copy and verify records; manage DNSSEC/DS safely before nameserver change; set Cloudflare-assigned nameservers; confirm zone Active; unlock at losing registrar; request short-lived EPP code; initiate transfer and approve notifications; verify new registrar, expiration, services, renewal settings, and re-enable DNSSEC appropriately. Cloudflare notes DNSSEC removal/propagation requirements before NS changes: follow current documentation to prevent DNS outages.

## Purchase and operational controls

Purchases, transfers, registrar changes, contact changes and multi-year renewals are chargeable or operationally consequential. Produce a dated **decision record and cost breakdown** first; require explicit authorized approval before executing payment or a transfer. Confirm final checkout totals immediately before the irreversible step. Cloudflare states registrar charges are generally non-refundable.

After completion: verify registry/registrar status and expiry (not just success UI); verify website, authoritative DNS, DNSSEC, email and critical service records; enable MFA, keep registrar account recovery contacts current, restrict API tokens, enable appropriate transfer/registry locks, record receipt and renewal date. Enable auto-renew where desired and monitor payment validity; auto-renew can fail. Maintain an independent advance renewal reminder and review registry/registrar price changes periodically. Never let a low first-year promotion displace renewal security.

## Output contract

Provide: (1) verification date and exact-name availability/premium status; (2) supported registration/transfer pathways; (3) TCO table at requested horizons with effective expiry and all fees; (4) restrictions and DNS/security impact; (5) recommended option with evidence and uncertainties; (6) explicit pre-purchase approval checkpoint; (7) post-transfer validation. If authoritative live verification is unavailable, say exactly what remains unverified and stop before purchase.

## Primary references to recheck

- Cloudflare Registrar overview: https://developers.cloudflare.com/registrar/
- Cloudflare registration: https://developers.cloudflare.com/registrar/get-started/register-domain/
- Cloudflare transfer procedure: https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/
- Cloudflare renewal: https://developers.cloudflare.com/registrar/account-options/renew-domains/
- Cloudflare Registrar API and exact-domain eligibility/pricing: https://developers.cloudflare.com/api/resources/registrar/
- Cloudflare supported TLD rules: https://www.cloudflare.com/tld-policies/
- ICANN transfer policy: https://www.icann.org/resources/pages/transfer-policy-2016-06-01-en

Treat all prices, TLD support and policy exceptions as time-sensitive; recheck sources for every procurement.
