# Value Added Solutions (VAS)

Last updated: July 2026
Status: Draft for review
Use stage: Master Content Brief

## Product Definition

Value Added Solutions (VAS) are engagement tools that complement Smart E-Vouchers across acquisition, event engagement, retention, and reactivation workflows.

VAS currently includes:

- On-us Form
- Voucher Pack
- Lucky Draw

## Role in the On-us Product System

VAS should be understood as campaign mechanics around the Smart E-Voucher. They help marketers create the participation moment before, during, or after voucher issuance.

Examples:

- On-us Form creates the data capture or registration moment.
- Voucher Pack packages multiple rewards into one distribution experience.
- Lucky Draw creates a gamified reward allocation moment.

The Smart E-Voucher remains the core reward and redemption mechanism.

## On-us Form

On-us Form is an interactive form module used for data capture, lead generation, surveys, event registration, and incentive-linked submissions.

Key capabilities:

- Branded form interface
- Multilingual configuration
- Survey or lead capture
- Instant Smart E-Voucher issuance upon form submission
- UTM and participation tracking
- Deduplication and basic fraud-control mechanisms, where configured
- Lead origin or incoming channel tracking
- Duplicate entry control
- Contact information validation against marketer-provided data, where configured
- Flexible question setup, with user experience considered when deciding length

Best use cases:

- Lead acquisition
- Survey incentive
- Event registration
- Public campaign participation

Usage notes:

- There is no fixed maximum number of form questions in the FAQ context, but the AI should not recommend overly long forms. Keep the form length aligned with the campaign objective and expected conversion friction.
- On-us Form can support multiple languages when the campaign needs localization.
- Rewards can be delivered after the user qualifies through form submission, depending on campaign rules and verification setup.
- Do not describe On-us Form as a full CRM. It is a lead capture and campaign participation module around Smart E-Voucher issuance.

## Voucher Pack

Voucher Pack is a unified link or package that gives users access to multiple Smart E-Vouchers or reward options in one place.

Key capabilities:

- Multiple vouchers in one package
- Local and cross-border voucher mix
- Marketer-funded and merchant-funded offers
- Suitable for high-volume distribution
- Multiple expiry dates, depending on reward setup
- Flexible reward combinations, including multi-merchant vouchers and vouchers of different values or categories

Best use cases:

- Events
- MICE
- Seasonal campaigns
- Corporate rewards
- Multi-stage campaign rewards

## Lucky Draw

Lucky Draw is a gamified reward mechanic for events, annual dinners, employee engagement, and high-participation campaigns.

Key capabilities:

- Branded lucky draw experience
- Prize tier allocation
- Instant Smart E-Voucher distribution
- Entry validation
- High engagement format for offline or hybrid events
- Custom prize wheel branding or in-house visual design
- Pre-set algorithm for distributing rewards from a marketer-defined prize pool
- Verification code or entry validation mechanism, depending on campaign setup
- Prize allocation settings that can be configured around campaign objectives

Best use cases:

- Corporate annual events
- Employee appreciation
- On-site activations
- Gamified marketing campaigns

## Positioning Rule

VAS should be positioned as supporting engagement workflows, not as a separate business unrelated to Smart E-Vouchers.

## Proof Point Boundary

If the AI wants to use a conversion uplift number for On-us Form, it must check `proof_points.md` or request human confirmation first.

Do not write:

```text
On-us Form always drives 85% higher conversion.
```

unless the exact claim is approved for the specific content.
