# Plan: Configure Automatic Model Fallback in Hermes Agent

## Goal
Configure automatic provider failover in Hermes Agent so that if the local 9router custom provider (`http://localhost:20128/v1`) runs out of tokens or encounters a rate limit (429) or connection error, Hermes automatically falls back to a secondary provider (e.g., OpenRouter).

## Current context / assumptions
- Primary model: `Reasoning` on custom provider `http://localhost:20128/v1` (9router).
- Configuration file: `C:\Users\Admin\AppData\Local\hermes\config.yaml`.
- Currently, `fallback_model` is commented out in `config.yaml`, meaning no automatic failover is active.
- The user wants to know how failover behaves and needs a robust configuration in place to handle token exhaustion or provider errors.

## Architecture / proposed approach
1. Define a fallback provider and model block in `C:\Users\Admin\AppData\Local\hermes\config.yaml` using the `fallback_model` key (e.g., pointing to OpenRouter with a reliable model like `anthropic/claude-sonnet-4`).
2. Verify the configuration syntax and validate the fallback chain using Hermes CLI commands (`hermes fallback list`).
3. Document how error triggers (429, 503, 529, connection errors) invoke the fallback chain.

## Step-by-step tasks

### Task 1: Update `config.yaml` to enable fallback model
- **File path**: `C:\Users\Admin\AppData\Local\hermes\config.yaml`
- **Action**: Add or uncomment the `fallback_model` configuration block.
- **Code snippet**:
  ```yaml
  fallback_model:
    provider: openrouter
    model: anthropic/claude-sonnet-4
  ```
- **Verification**: Run `hermes fallback list` via terminal and ensure it shows OpenRouter as the fallback provider.

### Task 2: Verify CLI Fallback Integration
- **Command**: `hermes fallback list`
- **Expected Output**:
  ```
  Fallback provider chain:
    1. openrouter / anthropic/claude-sonnet-4
  ```

## Tests / validation
- Run `hermes fallback list` to verify that the fallback model is correctly loaded and parsed from `config.yaml`.
- Inspect logs during a simulated rate limit or test error handling behavior if applicable.

## Risks, tradeoffs, and open questions
- **API Keys**: Ensure `OPENROUTER_API_KEY` is correctly set in the environment or `.env` if OpenRouter is chosen as the fallback provider, otherwise fallback authentication will fail.
- **Cost**: Fallback to commercial cloud providers (like OpenRouter/Anthropic) may incur costs if the local 9router free/unlimited tier is exhausted.
