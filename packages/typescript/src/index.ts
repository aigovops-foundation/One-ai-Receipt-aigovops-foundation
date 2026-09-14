/**
 * One Receipt — TypeScript contract for spec v0.2-draft.
 * Types only in this incubation release; a signing/verifying SDK (@one-receipt/sdk) is a
 * Phase-1 deliverable and must pass testkit/vectors before it may call itself conformant.
 */

export type SpecVersion = "0.2-draft";
export type Urn = `urn:one-receipt:${string}`;

export type AssuranceLevel = "OR-0" | "OR-1" | "OR-2" | "OR-3" | "OR-4" | "OR-5";

export type TransactionType =
  | "inference" | "tool-call" | "agent-delegation" | "human-review" | "output-delivery"
  | "policy-decision" | "challenge" | "review" | "remedy" | "incident" | "aggregate";

export type Boundary = "request-response" | "streaming-segment" | "agent-action" | "batch" | "aggregate";
export type ClockSource = "issuer" | "trusted-time-authority" | "qualified-time-stamp";
export type IssuerRole = "operator" | "delegate" | "reviewer" | "remediator" | "log-operator" | "assessor" | "registry-steward";
export type SignatureAlgorithm = "Ed25519" | "ES256" | "ML-DSA-65" | "Ed25519+ML-DSA-65";
export type CommitmentScheme = "salted-sha256" | "hmac-sha256" | "pedersen";

export type OmissionReason =
  | "not-applicable" | "not-collected" | "withheld-privacy" | "withheld-legal" | "withheld-security"
  | "unavailable-outage" | "deferred-to-parent" | "deferred-to-aggregate";

/** A commitment to content the receipt never carries. Plain hashes are not permitted. */
export interface Commitment { scheme: CommitmentScheme; value: string; salt_ref?: string }

export interface PrivacyProfile {
  profile: "content-free" | "commitment-only" | "authority-disclosable" | "consented-disclosure";
  commitment_scheme: "none" | CommitmentScheme;
  linkability_scope: "transaction" | "principal-session" | "none";
  metadata_minimization: boolean;
  reidentification_risk_assessment_ref?: string;
  disclosure_authority?: string[];
}

export interface PredicateManifestEntry { type: string; version: string; critical: boolean; omission_reason?: OmissionReason }

// ---- predicates (v1.0) -------------------------------------------------------------------
export interface TransactionPredicate {
  interface: "chat" | "api" | "voice" | "agent-to-agent" | "ide" | "browser-extension" | "embedded" | "commerce" | "batch" | "other";
  boundary_rule?: string;
  segment?: { index?: number; of?: number; batching_profile?: "per-turn" | "per-utterance" | "time-window" | "token-window" | "per-action"; window_ms?: number };
  id_carrier?: "response-header" | "message-metadata" | "spoken" | "transcript" | "git-trailer" | "device-store" | "cart-mandate" | "none";
  delegation_depth?: number;
  dropped_events_declared?: boolean;
}
export interface IdentityPredicate {
  principal_binding_mode: "none" | "pseudonymous" | "authenticated-ref" | "collective";
  principal_ref?: string; operator_id?: string;
  agent?: { id?: string; card_ref?: string; workload_identity?: "spiffe" | "web-bot-auth" | "oidc-workload" | "none" };
  model?: { ref?: string; version?: string; bom_ref?: string; weights_commitment?: Commitment };
  tool_ids?: string[];
}
export interface MandatePredicate {
  scheme: "plain-words-rule" | "ap2-intent" | "ap2-cart" | "mastercard-verifiable-intent" | "visa-tap" | "acp-allowance" | "oidc-consent" | "none";
  within_mandate: "yes" | "no" | "not-assessed";
  scope?: string; limits?: Record<string, unknown>; expiry?: string; mandate_commitment?: Commitment; mandate_ref?: string; community_authority_ref?: string;
}
export interface PolicyPredicate {
  policy_id: string; version: string;
  decision: "allow" | "constrain" | "hold" | "escalate" | "deny";
  enforcement_point: "pre-action" | "in-flight" | "post-action" | "review";
  policy_commitment?: Commitment; tier?: string;
  controls?: { id: string; vocabulary?: "ucid" | "overt" | "aiuc-1" | "aicm" | "iso-42001" | "nist-ai-rmf" | "local"; outcome: "pass" | "fail" | "skipped" | "error"; evidence_ref?: string }[];
  human_in_loop?: "none" | "notified" | "approved" | "overrode"; risk_class?: string; jurisdiction_refs?: string[];
}
export interface RuntimePredicate {
  content_included: false;
  input_commitment?: Commitment; output_commitment?: Commitment;
  counts?: { input_tokens?: number; output_tokens?: number; tool_calls?: number; latency_ms?: number };
  environment?: { attestation?: "none" | "rats-evidence" | "tee-quote" | "confidential-space" | "pcc"; attestation_ref?: string; region?: string };
  otel?: { trace_id?: string; span_id?: string };
  child_receipt_ids?: Urn[];
}
export interface ProvenanceDisclosurePredicate {
  ai_disclosed: boolean; output_kind: "text" | "code" | "image" | "audio" | "video" | "action" | "mixed" | "none";
  disclosure_channel?: "visible-text" | "spoken" | "header" | "manifest" | "label" | "none";
  manifest?: { scheme?: "c2pa" | "iptc" | "china-reference-number" | "none"; manifest_commitment?: Commitment; reference_number?: string };
  accessibility?: { languages?: string[]; formats?: ("plain-language" | "screen-reader" | "audio" | "large-print" | "sign-language")[] };
}
export interface WitnessPredicate {
  log_operator: { id: string; kind?: "scitt" | "rekor" | "merkle-append-only" | "other"; service_ref?: string };
  equivocation_status: "not-observed" | "suspected" | "confirmed";
  log_checkpoint?: { tree_size: number; root_hash: string; checkpoint_signature?: string };
  inclusion_proof?: { leaf_index: number; hashes: string[]; format?: "rfc6962" | "rfc9942-cose-receipt" };
  consistency_proof?: { from_tree_size?: number; hashes?: string[] };
  witnesses?: { id: string; observed_at: string; cosignature?: string }[];
  cross_log_anchor?: { log_id?: string; entry_ref?: string };
  observed_at?: string;
}
export interface ContestabilityPredicate {
  notice: { given: boolean; channel?: "in-interface" | "email" | "letter" | "spoken" | "none"; languages?: string[]; accessible_formats?: string[] };
  explanation: { available: boolean; ref?: string; kind?: "decision-summary" | "factors" | "counterfactual" | "policy-text" | "none"; legal_basis?: string[] };
  challenge: { available: boolean; route_ref?: string; deadline?: string; cost?: "free" | "fee" | "unknown"; representative_allowed?: boolean };
  human_review: { available: boolean; reviewer_authority?: "override" | "recommend" | "none"; reviewer_independent?: boolean; sla_hours?: number };
  remedy?: { types?: ("correction" | "reversal" | "deletion" | "compensation-referral" | "re-run-with-human" | "none")[]; collective_redress?: boolean; escalation_ref?: string };
  case_id?: string; outcome_receipt_ids?: Urn[];
}
export interface LegalEvidencePredicate {
  jurisdiction_profile: "EU-eIDAS-QTSA" | "US-FRE-901" | "CN-online-litigation" | "UK-CPR-PD57AD" | "generic";
  collection_method: string; collector_identity: string;
  timestamp_assurance: "issuer-clock" | "rfc3161" | "qualified-time-stamp" | "log-observed";
  chain_of_custody?: { holder: string; from: string; to?: string; transfer_receipt_id?: Urn }[];
  verifier_version?: string; evidence_export_manifest?: string; retention_until?: string;
}
export interface CommunityAuthorityExtension {
  authority_ref: string; consent_basis: "fpic" | "community-protocol" | "delegated" | "not-applicable";
  use_restrictions?: ("no-public-log" | "no-transfer" | "no-training" | "no-retention-beyond-purpose" | "community-review-required")[];
  stewardship_contact_ref?: string; review_required_before_disclosure?: boolean;
}

export interface Predicates {
  transaction?: TransactionPredicate; identity?: IdentityPredicate; mandate?: MandatePredicate; policy?: PolicyPredicate;
  runtime?: RuntimePredicate; "provenance-disclosure"?: ProvenanceDisclosurePredicate; witness?: WitnessPredicate;
  contestability?: ContestabilityPredicate; "legal-evidence"?: LegalEvidencePredicate; "community-authority"?: CommunityAuthorityExtension;
  [custom: string]: unknown;
}

// ---- envelope ----------------------------------------------------------------------------
export interface OneReceiptEnvelope {
  spec_version: SpecVersion;
  receipt_id: Urn; transaction_id: Urn; event_id: Urn;
  parent_receipt_ids?: Urn[]; root_receipt_id: Urn;
  transaction_type: TransactionType; sequence: number; boundary: Boundary;
  started_at: string; ended_at: string; issued_at: string; clock_source: ClockSource;
  issuer: { id: string; key_id: string; role: IssuerRole; key_discovery?: "did-web" | "did-key" | "jwks" | "x509" | "scitt-issuer" | "out-of-band" };
  assurance_level: AssuranceLevel;
  privacy_profile: PrivacyProfile;
  predicate_manifest: PredicateManifestEntry[];
  predicates: Predicates;
  limitations: string[];
  extensions?: Record<string, unknown>;
  signature: {
    algorithm: SignatureAlgorithm; canonicalization: "JCS" | "CBOR-CDE"; key_id: string; value: string;
    countersignatures?: { algorithm: SignatureAlgorithm; key_id: string; role: "log-operator" | "witness" | "time-authority" | "reviewer" | "assessor"; value: string }[];
  };
}

/** What a verifier returns. `verified_level` is what the verifier could substantiate, never what was claimed. */
export interface VerificationResult {
  valid: boolean;
  claimed_level: AssuranceLevel | null;
  verified_level: AssuranceLevel | null;
  checks: Record<string, boolean | null>;
  errors: string[];
  warnings: string[];
  limitations: string[];
}

export interface GraphVerificationResult {
  valid: boolean;
  receipts: Record<string, VerificationResult>;
  graph_errors: string[];
  weakest_verified_level: AssuranceLevel | null;
  limitations: string[];
}

export const CRITICAL_PREDICATES = ["transaction", "policy", "runtime", "contestability"] as const;
export const LEVELS: readonly AssuranceLevel[] = ["OR-0", "OR-1", "OR-2", "OR-3", "OR-4", "OR-5"];
