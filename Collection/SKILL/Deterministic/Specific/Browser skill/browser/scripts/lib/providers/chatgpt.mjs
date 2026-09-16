// ChatGPT adapter DATA — stub until Phase 6. Only the allowlisted host and entry URL are fixed.
export const id = 'chatgpt';
export const implemented = false;
export const phase = 'phase-6';
export const entryUrl = 'https://chatgpt.com/';
export const hosts = Object.freeze(['chatgpt.com']);
export const rules = Object.freeze([]);
export const composer = Object.freeze([]);
export const send = Object.freeze([]);
export const generationStarted = Object.freeze([]);
export const assistantMessage = Object.freeze([]);
export const userMessage = Object.freeze([]);
export const artifactHints = Object.freeze([]);
export const notificationRegions = Object.freeze({ toast_css: '[role="status"], [role="alert"]', banner_css: '' });
export function parseResetTime() { return null; }
export function nextLocalTime() { return null; }
