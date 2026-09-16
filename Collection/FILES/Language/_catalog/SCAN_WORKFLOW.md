# Language Library Scan Workflow

Root: `C:\Users\Admin\Documents\Collection\Data\Language`

## Current Layout

```text
Language\
  Glossika\
    Chinese\
    Japanese\
    Korean\
    _archives\
    _derived\
  _catalog\
  _tools\
```

Each course should follow this shape:

```text
<Provider>\
  <Language>\
    <Series>\
      <Book name>\
        <Book name>.pdf
        Audio\
```

Example:

```text
Glossika\
  Chinese\
    Business\
      Glossika Chinese Business 1\
        Glossika Chinese Business 1.pdf
        Audio\
```

## Scan Steps

1. Put new downloads under `Language\_incoming\<Provider>` first.
2. Run inventory:

   ```powershell
   python "C:\Users\Admin\Documents\Collection\Data\Language\_tools\language_library_organizer.py" scan
   ```

3. Add or update provider-specific rules in `_tools\language_library_organizer.py`.
4. Generate a dry-run move plan:

   ```powershell
   python "C:\Users\Admin\Documents\Collection\Data\Language\_tools\language_library_organizer.py" plan
   ```

5. Inspect the latest `move_plan_*.csv` and `conflicts_*.csv` in `_catalog`.
6. Apply only a conflict-free plan:

   ```powershell
   python "C:\Users\Admin\Documents\Collection\Data\Language\_tools\language_library_organizer.py" apply --plan "<latest move_plan json>"
   ```

## Future Providers

For Assimil, keep the same provider-first pattern:

```text
Assimil\
  Chinese\
    With Ease\
      Assimil Chinese With Ease\
        Assimil Chinese With Ease.pdf
        Audio\
```

Do not mix raw downloads with organized courses. Keep raw archives in `<Provider>\_archives` and generated files in `<Provider>\_derived`.
