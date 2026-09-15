/**
 * Model Budget Guard for Pi
 *
 * Goals:
 * - Show the price metadata Pi has for every available model.
 * - Query live subscription quota where the provider exposes a usable account endpoint.
 * - Fail closed for providers configured as `free-only` (OpenCode Zen by default).
 * - Keep "API-equivalent price" separate from "what this account is actually billed".
 *
 * Pi 0.85+.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

type Cost = {
	input?: number;
	output?: number;
	cacheRead?: number;
	cacheWrite?: number;
};

type ModelLike = {
	provider: string;
	id: string;
	name?: string;
	baseUrl?: string;
	cost?: Cost;
};

type ProviderPolicy = {
	enabled?: boolean;
	mode?: "allow" | "free-only";
	allow?: string[];
	deny?: string[];
	billing?: "subscription" | "free-tier-unverified" | "api" | "unknown";
};

type GuardConfig = {
	failClosed?: boolean;
	showStartupSummary?: boolean;
	fallbackOrder?: string[];
	fallback?: { provider: string; model: string };
	providers?: Record<string, ProviderPolicy>;
};

type UsageSection = {
	provider: string;
	title: string;
	lines: string[];
	ok: boolean;
};

const DEFAULT_CONFIG: Required<Pick<GuardConfig, "failClosed" | "showStartupSummary" | "fallbackOrder">> & GuardConfig = {
	failClosed: true,
	showStartupSummary: true,
	fallbackOrder: ["openai-codex", "xai", "github-copilot", "google", "opencode"],
	providers: {
		"openai-codex": { mode: "allow", billing: "subscription" },
		xai: { mode: "allow", billing: "subscription" },
		"github-copilot": { mode: "allow", billing: "subscription" },
		google: { mode: "allow", billing: "free-tier-unverified" },
		opencode: { mode: "free-only", billing: "api" },
	},
};

const WIDGET_KEY = "model-budget-guard";
let redirecting = false;
let lastProviderHeaders = new Map<string, Record<string, string>>();

function mergeConfig(base: GuardConfig, extra: GuardConfig): GuardConfig {
	return {
		...base,
		...extra,
		fallbackOrder: extra.fallbackOrder ?? base.fallbackOrder,
		fallback: extra.fallback ?? base.fallback,
		providers: {
			...(base.providers ?? {}),
			...(extra.providers ?? {}),
		},
	};
}

function loadJson(path: string): GuardConfig | undefined {
	if (!existsSync(path)) return undefined;
	try {
		return JSON.parse(readFileSync(path, "utf8")) as GuardConfig;
	} catch {
		return undefined;
	}
}

function loadConfig(cwd: string): GuardConfig {
	let cfg: GuardConfig = DEFAULT_CONFIG;
	const globalPath = join(homedir(), ".pi", "agent", "model-budget-guard.json");
	const projectPath = join(cwd, ".pi", "model-budget-guard.json");
	for (const path of [globalPath, projectPath]) {
		const next = loadJson(path);
		if (next) cfg = mergeConfig(cfg, next);
	}
	return cfg;
}

function wildcardMatch(value: string, pattern: string): boolean {
	const escaped = pattern.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*").replace(/\?/g, ".");
	return new RegExp(`^${escaped}$`, "i").test(value);
}

function matchAny(model: ModelLike, patterns: string[] | undefined): boolean {
	if (!patterns?.length) return false;
	const full = `${model.provider}/${model.id}`;
	return patterns.some((p) => wildcardMatch(model.id, p) || wildcardMatch(full, p));
}

function zeroCost(model: ModelLike): boolean {
	if (!model.cost) return false;
	const values = [model.cost.input, model.cost.output, model.cost.cacheRead, model.cost.cacheWrite];
	return values.every((v) => Number(v ?? 0) === 0);
}

function policyFor(config: GuardConfig, provider: string): ProviderPolicy {
	return config.providers?.[provider] ?? { mode: "allow", billing: "unknown" };
}

function allowed(model: ModelLike, config: GuardConfig): { ok: boolean; reason?: string } {
	const rule = policyFor(config, model.provider);
	if (rule.enabled === false) return { ok: false, reason: `${model.provider} is disabled` };
	if (matchAny(model, rule.deny)) return { ok: false, reason: "denied by model policy" };
	if (rule.allow?.length && !matchAny(model, rule.allow)) return { ok: false, reason: "not in allowlist" };
	if (rule.mode === "free-only") {
		if (!model.cost && config.failClosed !== false) {
			return { ok: false, reason: "provider is free-only and price metadata is missing (fail-closed)" };
		}
		if (model.cost && !zeroCost(model)) {
			return { ok: false, reason: "provider is free-only and Pi price metadata is non-zero" };
		}
	}
	return { ok: true };
}

function fmtMoney(n: unknown): string {
	const v = Number(n);
	if (!Number.isFinite(v)) return "?";
	if (v === 0) return "$0";
	if (v < 0.01) return `$${v.toFixed(4)}`;
	return `$${v.toFixed(2)}`;
}

function fmtRate(model: ModelLike): string {
	const c = model.cost;
	if (!c) return "price unknown";
	if (zeroCost(model)) return "FREE";
	return `in ${fmtMoney(c.input)}/M · out ${fmtMoney(c.output)}/M · cache ${fmtMoney(c.cacheRead)}/M`;
}

function fmtReset(value: unknown): string | undefined {
	if (value == null) return undefined;
	let d: Date | undefined;
	if (typeof value === "number") d = new Date(value > 10_000_000_000 ? value : value * 1000);
	else if (typeof value === "string") {
		const n = Number(value);
		if (Number.isFinite(n) && value.trim() !== "") d = new Date(n > 10_000_000_000 ? n : n * 1000);
		else {
			const parsed = new Date(value);
			if (!Number.isNaN(parsed.getTime())) d = parsed;
		}
	}
	if (!d || Number.isNaN(d.getTime())) return undefined;
	return d.toLocaleString();
}

function durationLabel(seconds: unknown, fallback: string): string {
	const s = Number(seconds);
	if (!Number.isFinite(s) || s <= 0) return fallback;
	if (Math.abs(s - 18_000) < 120) return "5h";
	if (Math.abs(s - 604_800) < 600) return "week";
	if (s < 3600) return `${Math.round(s / 60)}m`;
	if (s < 86_400) return `${Math.round(s / 3600)}h`;
	return `${Math.round(s / 86_400)}d`;
}

function pickNumber(obj: Record<string, unknown>, keys: string[]): number | undefined {
	for (const key of keys) {
		const raw = obj[key];
		if (raw == null || raw === "") continue;
		const v = Number(raw);
		if (Number.isFinite(v)) return v;
	}
	return undefined;
}

function pickString(obj: Record<string, unknown>, keys: string[]): string | undefined {
	for (const key of keys) {
		const v = obj[key];
		if (typeof v === "string" && v.trim()) return v;
	}
	return undefined;
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
	return value && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, unknown>) : undefined;
}

async function fetchJson(url: string, headers: Record<string, string>, timeoutMs = 10_000): Promise<Record<string, unknown>> {
	const controller = new AbortController();
	const timer = setTimeout(() => controller.abort(), timeoutMs);
	try {
		const response = await fetch(url, {
			method: "GET",
			headers,
			redirect: "error",
			signal: controller.signal,
		});
		const text = await response.text();
		if (!response.ok) throw new Error(`HTTP ${response.status}`);
		if (text.length > 1_000_000) throw new Error("response too large");
		const parsed = JSON.parse(text) as unknown;
		const rec = asRecord(parsed);
		if (!rec) throw new Error("invalid JSON object");
		return rec;
	} finally {
		clearTimeout(timer);
	}
}

async function authForProvider(ctx: any, provider: string) {
	const model = (ctx.modelRegistry.getAvailable() as ModelLike[]).find((m) => m.provider === provider);
	if (!model) throw new Error("no available model");
	const auth = await ctx.modelRegistry.getApiKeyAndHeaders(model as any);
	if (!auth.ok) throw new Error(auth.error || "auth unavailable");
	return {
		model,
		token: auth.apiKey as string | undefined,
		headers: (auth.headers ?? {}) as Record<string, string>,
		baseUrl: (auth.baseUrl ?? model.baseUrl) as string | undefined,
		oauth: Boolean(ctx.modelRegistry.isUsingOAuth(model as any)),
	};
}

function safeHeaders(base: Record<string, string> | undefined): Record<string, string> {
	const out: Record<string, string> = {};
	for (const [k, v] of Object.entries(base ?? {})) {
		if (typeof v === "string") out[k] = v;
	}
	return out;
}

function windowLine(label: string, window: Record<string, unknown>): string | undefined {
	const used = pickNumber(window, ["used_percent", "usedPercent"]);
	const remaining = pickNumber(window, ["percent_left", "percent_remaining", "remaining_percent", "remainingPercentage"]);
	const pctLeft = remaining ?? (used == null ? undefined : Math.max(0, 100 - used));
	if (pctLeft == null) return undefined;
	const reset = fmtReset(window.reset_at ?? window.reset_time_ms ?? window.resetAt ?? window.reset_at_utc);
	return `${label}: ${pctLeft.toFixed(1)}% left${reset ? ` · reset ${reset}` : ""}`;
}

async function codexUsage(ctx: any): Promise<UsageSection> {
	const provider = "openai-codex";
	try {
		const auth = await authForProvider(ctx, provider);
		if (!auth.oauth || !auth.token) throw new Error("not using ChatGPT subscription OAuth");
		const headers = {
			...safeHeaders(auth.headers),
			Authorization: `Bearer ${auth.token}`,
			Accept: "application/json",
			"OpenAI-Beta": "codex-1",
		};
		const data = await fetchJson("https://chatgpt.com/backend-api/wham/usage", headers);
		const lines: string[] = [];
		const plan = pickString(data, ["plan_type", "planType"]);
		if (plan) lines.push(`plan: ${plan}`);
		const rl = asRecord(data.rate_limit ?? data.rate_limits);
		if (rl) {
			const primary = asRecord(rl.primary_window ?? rl.five_hour);
			const secondary = asRecord(rl.secondary_window ?? rl.weekly);
			if (primary) {
				const line = windowLine(durationLabel(primary.limit_window_seconds, "primary"), primary);
				if (line) lines.push(line);
			}
			if (secondary) {
				const line = windowLine(durationLabel(secondary.limit_window_seconds, "secondary"), secondary);
				if (line) lines.push(line);
			}
		}
		const additional = Array.isArray(data.additional_rate_limits) ? data.additional_rate_limits : [];
		for (const item of additional) {
			const rec = asRecord(item);
			if (!rec) continue;
			const nested = asRecord(rec.rate_limit ?? rec.window) ?? rec;
			const label = pickString(rec, ["label", "name", "rate_limit_name", "model"]) ?? "extra";
			const line = windowLine(label, nested);
			if (line) lines.push(line);
		}
		const credits = asRecord(data.credits);
		if (credits) {
			const balance = pickNumber(credits, ["balance", "remaining", "amount"]);
			if (balance != null) lines.push(`credits: ${fmtMoney(balance)}`);
		}
		if (!lines.length) lines.push("quota endpoint responded, but no recognized counters were returned");
		lines.push("billing: ChatGPT subscription allowance, not OpenAI API token billing");
		return { provider, title: "OpenAI Codex", lines, ok: true };
	} catch (error) {
		return { provider, title: "OpenAI Codex", lines: [`unavailable: ${error instanceof Error ? error.message : String(error)}`], ok: false };
	}
}

async function copilotUsage(ctx: any): Promise<UsageSection> {
	const provider = "github-copilot";
	try {
		const auth = await authForProvider(ctx, provider);
		if (!auth.token) throw new Error("token unavailable");
		const data = await fetchJson("https://api.github.com/copilot_internal/user", {
			Authorization: `token ${auth.token}`,
			Accept: "application/json",
			"X-GitHub-Api-Version": "2025-05-01",
			"User-Agent": "GitHubCopilotCLI/pi-model-budget-guard",
			"Copilot-Integration-Id": "copilot-cli",
		});
		const lines: string[] = [];
		const plan = pickString(data, ["copilot_plan", "plan"]);
		if (plan) lines.push(`plan: ${plan}`);
		const reset = fmtReset(data.quota_reset_date_utc ?? data.quota_reset_date);
		const snapshots = asRecord(data.quota_snapshots);
		if (snapshots) {
			for (const [name, raw] of Object.entries(snapshots)) {
				const q = asRecord(raw);
				if (!q) continue;
				if (q.unlimited === true) {
					lines.push(`${name}: unlimited${reset ? ` · reset ${reset}` : ""}`);
					continue;
				}
				const total = pickNumber(q, ["entitlement", "entitlement_requests", "entitlementRequests", "total"]);
				const remaining = pickNumber(q, ["remaining", "quota_remaining", "remaining_requests", "remainingRequests"]);
				const pct = pickNumber(q, ["percent_remaining", "remaining_percentage", "remainingPercentage"]);
				if (total != null || remaining != null || pct != null) {
					const amount = total != null && remaining != null ? `${remaining}/${total} left` : pct != null ? `${pct.toFixed(1)}% left` : `${remaining ?? "?"} left`;
					const overage = q.overage_permitted === true ? " · WARNING overage permitted" : "";
					lines.push(`${name}: ${amount}${reset ? ` · reset ${reset}` : ""}${overage}`);
				}
			}
		}
		if (!lines.length) lines.push("quota endpoint responded, but no recognized counters were returned");
		lines.push("billing: Copilot plan quota/credits; check GitHub billing if overage is enabled");
		return { provider, title: "GitHub Copilot", lines, ok: true };
	} catch (error) {
		return { provider, title: "GitHub Copilot", lines: [`unavailable: ${error instanceof Error ? error.message : String(error)}`], ok: false };
	}
}

function findUserId(data: Record<string, unknown>): string | undefined {
	return pickString(data, ["userId", "user_id", "id", "sub"]);
}

async function xaiUsage(ctx: any): Promise<UsageSection> {
	const provider = "xai";
	try {
		const auth = await authForProvider(ctx, provider);
		if (!auth.oauth || !auth.token) throw new Error("not using xAI subscription OAuth");
		const common = {
			Authorization: `Bearer ${auth.token}`,
			Accept: "application/json",
			"X-XAI-Token-Auth": "xai-grok-cli",
			"x-grok-client-mode": "cli",
		};
		const user = await fetchJson("https://cli-chat-proxy.grok.com/v1/user?include=subscription", common);
		const userId = findUserId(user);
		if (!userId) throw new Error("xAI identity response had no userId");
		const data = await fetchJson("https://cli-chat-proxy.grok.com/v1/billing?format=credits", {
			...common,
			"x-userid": userId,
		});
		const config = asRecord(data.config) ?? data;
		const lines: string[] = [];
		const tier = pickString(user, ["subscriptionTier", "subscription_tier", "plan"]);
		if (tier) lines.push(`plan: ${tier}`);
		const used = pickNumber(config, ["creditUsagePercent", "credit_usage_percent"]);
		const period = asRecord(config.currentPeriod ?? config.current_period);
		const reset = fmtReset(period?.end ?? config.billingPeriodEnd ?? config.billing_period_end);
		if (used != null) lines.push(`unified pool: ${Math.max(0, 100 - used).toFixed(1)}% left${reset ? ` · reset ${reset}` : ""}`);
		else if (reset) lines.push(`unified pool: remaining % not published · reset ${reset}`);
		const onDemandCap = pickNumber(asRecord(config.onDemandCap ?? config.on_demand_cap) ?? {}, ["val", "value", "amount"]);
		const onDemandUsed = pickNumber(asRecord(config.onDemandUsed ?? config.on_demand_used) ?? {}, ["val", "value", "amount"]);
		if (onDemandCap != null || onDemandUsed != null) lines.push(`on-demand: ${fmtMoney(onDemandUsed ?? 0)} used of ${fmtMoney(onDemandCap ?? 0)}`);
		const prepaid = pickNumber(asRecord(config.prepaidBalance ?? config.prepaid_balance) ?? {}, ["val", "value", "amount"]);
		if (prepaid != null) lines.push(`prepaid balance: ${fmtMoney(prepaid)}`);
		if (!lines.length) lines.push("billing endpoint responded, but no recognized counters were returned");
		lines.push("billing: Grok/X subscription pool; API-key team billing is a different system");
		return { provider, title: "xAI", lines, ok: true };
	} catch (error) {
		return { provider, title: "xAI", lines: [`unavailable: ${error instanceof Error ? error.message : String(error)}`], ok: false };
	}
}

function googleUsage(ctx: any, config: GuardConfig): UsageSection {
	const provider = "google";
	const models = (ctx.modelRegistry.getAvailable() as ModelLike[]).filter((m) => m.provider === provider);
	const freeMeta = models.filter(zeroCost).length;
	const headerHints = lastProviderHeaders.get(provider);
	const lines = [
		"exact remaining RPM/TPM/RPD is not exposed through a Gemini API-key response counter",
		"rate limits are project + model scoped; use Google AI Studio > Dashboard > Rate limits/Usage for the authoritative live counters",
		`Pi catalog: ${models.length} available model(s), ${freeMeta} with $0 price metadata`,
		`guard: ${policyFor(config, provider).mode ?? "allow"}; billing status cannot be verified from the API key alone`,
	];
	if (headerHints) {
		const relevant = Object.entries(headerHints).filter(([k]) => /rate|quota|limit/i.test(k));
		if (relevant.length) lines.push(`last response quota headers: ${relevant.map(([k, v]) => `${k}=${v}`).join(", ")}`);
	}
	return { provider, title: "Google Gemini", lines, ok: true };
}

function opencodeUsage(ctx: any, config: GuardConfig): UsageSection {
	const provider = "opencode";
	const models = (ctx.modelRegistry.getAvailable() as ModelLike[]).filter((m) => m.provider === provider);
	const free = models.filter(zeroCost);
	const paid = models.filter((m) => !zeroCost(m));
	const mode = policyFor(config, provider).mode ?? "allow";
	return {
		provider,
		title: "OpenCode Zen",
		ok: true,
		lines: [
			`policy: ${mode}${mode === "free-only" ? " (paid/unknown-price models are hard-blocked)" : ""}`,
			`catalog: ${free.length} FREE allowed · ${paid.length} paid/unknown ${mode === "free-only" ? "blocked" : "available"}`,
			"Zen free-model request allowance is not published as a stable remaining counter; model availability/rate-limit errors are the practical boundary",
			"billing risk under free-only policy: $0 model token price; still disable Zen auto-reload in the OpenCode console as a second safety layer",
		],
	};
}

function sessionCostLines(ctx: any): string[] {
	let total = 0;
	let input = 0;
	let output = 0;
	const byModel = new Map<string, number>();
	for (const entry of ctx.sessionManager.getEntries() as any[]) {
		const message = entry?.message ?? entry?.data?.message;
		if (!message || message.role !== "assistant") continue;
		const usage = message.usage ?? {};
		input += Number(usage.input ?? usage.inputTokens ?? 0) || 0;
		output += Number(usage.output ?? usage.outputTokens ?? 0) || 0;
		const cost = Number(usage.cost?.total ?? 0) || 0;
		total += cost;
		const model = message.model ?? "?";
		byModel.set(model, (byModel.get(model) ?? 0) + cost);
	}
	const top = [...byModel.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5);
	return [
		`Pi session estimate: ${fmtMoney(total)} API-equivalent · tokens in ${input.toLocaleString()} / out ${output.toLocaleString()}`,
		...(top.length ? [`top model estimates: ${top.map(([m, c]) => `${m} ${fmtMoney(c)}`).join(" · ")}`] : []),
		"Note: subscription provider cost metadata is an API-equivalent estimate, not an extra charge to your subscription.",
	];
}

function modelLines(ctx: any, config: GuardConfig, providerFilter?: string): string[] {
	const models = (ctx.modelRegistry.getAvailable() as ModelLike[])
		.filter((m) => !providerFilter || m.provider === providerFilter)
		.sort((a, b) => a.provider.localeCompare(b.provider) || a.id.localeCompare(b.id));
	const lines: string[] = ["MODEL POLICY + PRICE (USD per 1M tokens)"];
	let currentProvider = "";
	for (const model of models) {
		if (model.provider !== currentProvider) {
			currentProvider = model.provider;
			const rule = policyFor(config, currentProvider);
			lines.push("", `[${currentProvider}] mode=${rule.mode ?? "allow"} billing=${rule.billing ?? "unknown"}`);
		}
		const verdict = allowed(model, config);
		lines.push(`${verdict.ok ? "ALLOW" : "BLOCK"}  ${model.id}  | ${fmtRate(model)}${verdict.reason ? ` | ${verdict.reason}` : ""}`);
	}
	if (models.length === 0) lines.push("No available models matched.");
	return lines;
}

function policyLines(ctx: any, config: GuardConfig): string[] {
	const models = ctx.modelRegistry.getAvailable() as ModelLike[];
	const providers = [...new Set(models.map((m) => m.provider))].sort();
	const lines = ["MODEL BUDGET GUARD POLICY"];
	for (const provider of providers) {
		const rule = policyFor(config, provider);
		const providerModels = models.filter((m) => m.provider === provider);
		const blocked = providerModels.filter((m) => !allowed(m, config).ok).length;
		lines.push(`${provider}: ${rule.mode ?? "allow"} · billing=${rule.billing ?? "unknown"} · ${providerModels.length - blocked} allowed / ${blocked} blocked`);
	}
	lines.push("", "Config: ~/.pi/agent/model-budget-guard.json or <project>/.pi/model-budget-guard.json");
	return lines;
}

function findFallback(ctx: any, config: GuardConfig, previous?: ModelLike): ModelLike | undefined {
	const available = ctx.modelRegistry.getAvailable() as ModelLike[];
	if (previous && allowed(previous, config).ok) return previous;
	if (config.fallback) {
		const exact = available.find((m) => m.provider === config.fallback!.provider && m.id === config.fallback!.model);
		if (exact && allowed(exact, config).ok) return exact;
	}
	for (const provider of config.fallbackOrder ?? DEFAULT_CONFIG.fallbackOrder) {
		const candidate = available.find((m) => m.provider === provider && allowed(m, config).ok);
		if (candidate) return candidate;
	}
	return available.find((m) => allowed(m, config).ok);
}

async function enforceModel(pi: ExtensionAPI, ctx: any, model: ModelLike, previous?: ModelLike): Promise<boolean> {
	const config = loadConfig(ctx.cwd);
	const verdict = allowed(model, config);
	if (verdict.ok) return true;
	if (redirecting) return false;
	const fallback = findFallback(ctx, config, previous);
	if (!fallback) {
		ctx.ui.notify(`BLOCKED ${model.provider}/${model.id}: ${verdict.reason}. No safe fallback is available.`, "error");
		return false;
	}
	redirecting = true;
	try {
		const success = await pi.setModel(fallback as any);
		if (!success) {
			ctx.ui.notify(`BLOCKED ${model.provider}/${model.id}; failed to switch to safe fallback.`, "error");
			return false;
		}
		ctx.ui.notify(`BLOCKED ${model.provider}/${model.id}: ${verdict.reason}. Switched to ${fallback.provider}/${fallback.id}.`, "warning");
		return false;
	} finally {
		redirecting = false;
	}
}

async function showUsage(ctx: any) {
	const config = loadConfig(ctx.cwd);
	ctx.ui.setWidget(WIDGET_KEY, ["Checking provider quota..."], { placement: "aboveEditor" });
	const results = await Promise.all([codexUsage(ctx), copilotUsage(ctx), xaiUsage(ctx)]);
	results.push(googleUsage(ctx, config), opencodeUsage(ctx, config));
	const lines: string[] = ["AI QUOTA + BILLING SNAPSHOT", ...sessionCostLines(ctx)];
	for (const section of results) {
		lines.push("", `${section.ok ? "OK" : "WARN"} ${section.title}`);
		for (const line of section.lines) lines.push(`  ${line}`);
	}
	ctx.ui.setWidget(WIDGET_KEY, lines, { placement: "aboveEditor" });
}

export default function modelBudgetGuard(pi: ExtensionAPI) {
	pi.on("session_start", async (_event, ctx) => {
		const config = loadConfig(ctx.cwd);
		if (ctx.model) await enforceModel(pi, ctx, ctx.model as ModelLike);
		if (config.showStartupSummary) {
			const opencodeModels = (ctx.modelRegistry.getAvailable() as ModelLike[]).filter((m) => m.provider === "opencode");
			const free = opencodeModels.filter((m) => allowed(m, config).ok).length;
			const blocked = opencodeModels.length - free;
			ctx.ui.setStatus("model-budget", `guard: Zen ${free} free / ${blocked} blocked`);
		}
	});

	pi.on("model_select", async (event, ctx) => {
		await enforceModel(pi, ctx, event.model as ModelLike, event.previousModel as ModelLike | undefined);
	});

	pi.on("after_provider_response", async (event, ctx) => {
		if (!ctx.model) return;
		lastProviderHeaders.set(ctx.model.provider, { ...(event.headers as Record<string, string>) });
	});

	pi.registerCommand("ai-usage", {
		description: "Show live quota/billing snapshot for Codex, Copilot, xAI plus Gemini/Zen safety status",
		handler: async (_args, ctx) => {
			await showUsage(ctx);
		},
	});

	pi.registerCommand("ai-models", {
		description: "Show Pi model prices and whether each model is allowed by the budget guard",
		handler: async (args, ctx) => {
			const provider = args.trim() || undefined;
			ctx.ui.setWidget(WIDGET_KEY, modelLines(ctx, loadConfig(ctx.cwd), provider), { placement: "aboveEditor" });
		},
	});

	pi.registerCommand("ai-policy", {
		description: "Show active model budget policy",
		handler: async (_args, ctx) => {
			ctx.ui.setWidget(WIDGET_KEY, policyLines(ctx, loadConfig(ctx.cwd)), { placement: "aboveEditor" });
		},
	});

	pi.registerCommand("ai-budget-clear", {
		description: "Clear the model budget/usage widget",
		handler: async (_args, ctx) => {
			ctx.ui.setWidget(WIDGET_KEY, undefined);
		},
	});
}
