from __future__ import annotations

from datetime import date, datetime
import re
from typing import Any
from urllib.parse import urlparse

from ..models import FillPlan, FormField, FormSnapshot, digest


FORM_INSPECT_SCRIPT = r"""
(form) => {
  const CONTROL_SELECTOR =
    'input:not([type="hidden"]):not([type="submit"]):not([type="button"]),' +
    'textarea,select,[role="combobox"]';
  const controls = Array.from(form.querySelectorAll(CONTROL_SELECTOR))
    .filter(el => !el.disabled)
    .filter(el => el.getAttribute('aria-hidden') !== 'true')
    .filter(el => {
      const owner = el.closest('[role="combobox"]');
      return !owner || owner === el;
    })
    .filter(el => {
      const inputType = (el.getAttribute('type') || '').toLowerCase();
      return inputType === 'file' || el.getClientRects().length > 0;
    });

  function text(el) {
    return (el && (el.innerText || el.textContent) || '').replace(/\s+/g, ' ').trim();
  }
  function cssPath(el) {
    if (el.id) return '#' + CSS.escape(el.id);
    if (el.name) {
      const candidate = el.tagName.toLowerCase() + '[name="' +
        String(el.name).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"]';
      if (form.querySelectorAll(candidate).length === 1) return candidate;
    }
    const parts = [];
    let node = el;
    while (node && node !== form) {
      let index = 1;
      let sibling = node;
      while ((sibling = sibling.previousElementSibling)) {
        if (sibling.tagName === node.tagName) index += 1;
      }
      parts.unshift(node.tagName.toLowerCase() + ':nth-of-type(' + index + ')');
      node = node.parentElement;
    }
    return ':scope > ' + parts.join(' > ');
  }
  function directLabel(el) {
    const values = [];
    if (el.labels) values.push(...Array.from(el.labels).map(text));
    if (el.getAttribute('aria-label')) values.push(el.getAttribute('aria-label'));
    const labelled = (el.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean);
    values.push(...labelled.map(id => text(document.getElementById(id))));
    const fieldset = el.closest('fieldset');
    if (fieldset) {
      const legend = fieldset.querySelector(':scope > legend');
      if (legend) values.unshift(text(legend));
      const title = fieldset.querySelector(
        ':scope > .ashby-application-form-question-title,' +
        ':scope > label[class*="question-title"],:scope > label[class*="_required_"]'
      );
      if (title) values.unshift(text(title));
    }
    const question = el.closest(
      '.application-question,[data-field],.application-question,' +
      '.ashby-application-form-field'
    );
    if (question) {
      const title = question.querySelector(
        '.application-label .text,.application-label,' +
        '.ashby-application-form-question-title,[data-label],legend'
      );
      if (title) values.unshift(text(title));
    }
    const container = el.closest(
      '[data-field],.field,.application-field,.application-question,.ashby-application-form-field'
    );
    if (container) {
      const label = container.querySelector('label,legend,[data-label]');
      if (label) values.unshift(text(label));
    }
    if (el.placeholder) values.push(el.placeholder);
    if (el.name) values.push(el.name.replace(/[_-]+/g, ' '));
    return [...new Set(values.filter(Boolean))].join(' ').replace(/\s+/g, ' ').trim();
  }
  function optionLabel(el) {
    const values = [];
    if (el.labels) values.push(...Array.from(el.labels).map(text));
    if (el.getAttribute('aria-label')) values.push(el.getAttribute('aria-label'));
    const labelled = (el.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean);
    values.push(...labelled.map(id => text(document.getElementById(id))));
    return values.find(Boolean) || el.value || '';
  }
  function required(el, prompt) {
    const container = el.closest(
      'fieldset,[data-field],.field,.application-field,.application-question,' +
      '.ashby-application-form-field'
    );
    const marker = container ? text(container).slice(0, 500) : prompt;
    return !!el.required || el.getAttribute('aria-required') === 'true' ||
      (container && container.getAttribute('data-required') === 'true') ||
      !!(container && container.querySelector(
        '[class*="_required_"],.ashby-application-form-question-title[class*="required"]'
      )) ||
      /\brequired\b/i.test(marker) || /(^|\s)\*(?=\s|$)/.test(marker);
  }
  function radioPrompt(el) {
    const fieldset = el.closest('fieldset');
    if (fieldset) {
      const legend = fieldset.querySelector(':scope > legend');
      if (legend && text(legend)) return text(legend);
      const title = fieldset.querySelector(
        ':scope > .ashby-application-form-question-title,' +
        ':scope > label[class*="question-title"],:scope > label[class*="_required_"]'
      );
      if (title && text(title)) return text(title);
    }
    const question = el.closest('.application-question');
    if (question) {
      const title = question.querySelector('.application-label .text,.application-label');
      if (title && text(title)) return text(title);
    }
    const container = el.closest('[data-field],.field,.application-question');
    if (container) {
      const label = container.querySelector('label,legend,[data-label]');
      if (label && text(label)) return text(label);
    }
    return (el.name || el.id || 'radio question').replace(/[_-]+/g, ' ');
  }
  function currentValue(el, kind) {
    if (kind === 'file') {
      return {
        value: Array.from(el.files || []).map(file => file.name),
        observable: true
      };
    }
    if (kind === 'checkbox') return {value: !!el.checked, observable: true};
    if (kind === 'select') {
      const selected = el.options && el.selectedIndex >= 0
        ? el.options[el.selectedIndex] : null;
      return {
        value: selected && String(selected.value || '') !== '' ? text(selected) : '',
        observable: true
      };
    }
    if (kind === 'combobox' && typeof el.value === 'undefined') {
      const innerInput = el.querySelector('input:not([type="hidden"])');
      if (innerInput && typeof innerInput.value !== 'undefined') {
        return {value: String(innerInput.value), observable: true};
      }
      if (el.hasAttribute('data-value')) {
        return {value: el.getAttribute('data-value') || '', observable: true};
      }
      if (el.hasAttribute('aria-valuetext')) {
        return {value: el.getAttribute('aria-valuetext') || '', observable: true};
      }
      return {value: '', observable: false};
    }
    return typeof el.value === 'undefined'
      ? {value: '', observable: false}
      : {value: String(el.value), observable: true};
  }

  const output = [];
  const seenRadio = new Set();
  const seenCheckbox = new Set();
  for (const el of controls) {
    const inputType = (el.getAttribute('type') || '').toLowerCase();
    if (inputType === 'radio') {
      const group = el.name || el.id;
      if (seenRadio.has(group)) continue;
      seenRadio.add(group);
      const members = el.name
        ? Array.from(form.querySelectorAll('input[type="radio"][name="' +
            String(el.name).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"]'))
        : [el];
      const options = members.map(member => {
        const label = optionLabel(member);
        return {label, selector: cssPath(member)};
      });
      const prompt = radioPrompt(el);
      const selected = members.find(member => member.checked);
      output.push({
        key: group, prompt, kind: 'radio',
        required: members.some(member => required(member, prompt)),
        options: options.map(x => x.label),
        selector: cssPath(el),
        option_selectors: Object.fromEntries(options.map(x => [x.label, x.selector])),
        current_value: selected ? optionLabel(selected) : '',
        value_observable: true
      });
      continue;
    }
    if (inputType === 'checkbox' && el.name) {
      const members = Array.from(form.querySelectorAll(
        'input[type="checkbox"][name="' +
        String(el.name).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"]'
      )).filter(member => !member.disabled);
      if (members.length > 1) {
        if (seenCheckbox.has(el.name)) continue;
        seenCheckbox.add(el.name);
        const options = members.map(member => {
          const label = optionLabel(member);
          return {label, selector: cssPath(member)};
        });
        const prompt = radioPrompt(el);
        output.push({
          key: el.name, prompt, kind: 'checkbox-group',
          required: members.some(member => required(member, prompt)),
          options: options.map(x => x.label),
          selector: cssPath(el),
          option_selectors: Object.fromEntries(options.map(x => [x.label, x.selector])),
          current_value: members.filter(member => member.checked).map(optionLabel),
          value_observable: true
        });
        continue;
      }
    }
    const prompt = directLabel(el);
    const role = el.getAttribute('role');
    const kind = role === 'combobox' ? 'combobox'
      : el.tagName === 'SELECT' ? 'select'
      : el.tagName === 'TEXTAREA' ? 'textarea'
      : inputType === 'file' ? 'file'
      : inputType === 'checkbox' ? 'checkbox'
      : inputType || 'text';
    const options = el.tagName === 'SELECT'
      ? Array.from(el.options).map(option => text(option)).filter(Boolean)
      : [];
    const observed = currentValue(el, kind);
    output.push({
      key: el.id || el.name || cssPath(el),
      prompt,
      kind,
      required: required(el, prompt),
      options,
      selector: cssPath(el),
      option_selectors: {},
      current_value: observed.value,
      value_observable: observed.observable
    });
  }
  return output;
}
"""

CONFIRMATION_PATTERNS = (
    ("thank_you_for_applying", r"\bthank you for (?:applying|your application)\b"),
    (
        "application_submitted",
        r"\b(?:your )?application (?:has been |was )?(?:successfully )?submitted\b",
    ),
    (
        "application_received",
        r"\b(?:we (?:have|'ve) )?received your application\b|"
        r"\byour application (?:has been |was )?received\b",
    ),
)


def _validated_temporal_value(kind: str, value: Any) -> str:
    text = str(value)
    try:
        if kind == "date":
            if date.fromisoformat(text).isoformat() != text:
                raise ValueError
        elif kind == "month":
            if (
                not re.fullmatch(r"\d{4}-(?:0[1-9]|1[0-2])", text)
                or int(text[:4]) < 1
            ):
                raise ValueError
        elif kind == "datetime-local":
            if not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?",
                text,
            ):
                raise ValueError
            parsed = datetime.fromisoformat(text)
            if parsed.tzinfo is not None:
                raise ValueError
    except ValueError as exc:
        raise RuntimeError(
            f"Refusing invalid {kind} value; expected a browser-native ISO value"
        ) from exc
    return text


class BaseAdapter:
    ats = "unknown"
    form_selectors: tuple[str, ...] = ("form",)
    submit_selectors: tuple[str, ...] = ('button[type="submit"]', 'input[type="submit"]')

    def prepare(self, page: Any) -> None:
        """Navigate from a description view to the hosted application view."""
        return None

    def find_form(self, page: Any) -> Any:
        for selector in self.form_selectors:
            candidates = page.locator(selector)
            visible = [
                candidates.nth(index)
                for index in range(candidates.count())
                if candidates.nth(index).is_visible()
            ]
            if len(visible) == 1:
                return visible[0]
            if len(visible) > 1:
                matching = [
                    candidate
                    for candidate in visible
                    if candidate.locator('input[type="email"],input[name*="email" i]').count()
                ]
                if len(matching) == 1:
                    return matching[0]
                raise RuntimeError(f"Ambiguous application form: {len(visible)} visible matches")
        raise RuntimeError("Application form not found")

    def inspect(self, page: Any, url: str, captcha: bool) -> FormSnapshot:
        form = self.find_form(page)
        raw = form.evaluate(FORM_INSPECT_SCRIPT)
        fields = [FormField.from_dict(value) for value in raw]
        if not fields:
            raise RuntimeError("Application form contains no inspectable fields")
        for field in fields:
            if field.kind != "combobox" or field.options:
                continue
            locator = form.locator(field.selector)
            if locator.count() != 1 or not locator.is_visible():
                continue
            try:
                # Modern ATS combobox choices are usually mounted in a portal only
                # after the control is opened.  Snapshot the visible choices now so
                # policy can require one exact match instead of approving a value
                # that may fail (or match ambiguously) during fill.
                locator.click(timeout=2500)
                page.wait_for_timeout(150)
                option_locator = page.locator('[role="option"]:visible')
                values: list[str] = []
                for index in range(min(option_locator.count(), 500)):
                    option = option_locator.nth(index)
                    label = (
                        option.get_attribute("aria-label")
                        or option.inner_text(timeout=1000)
                        or ""
                    ).strip()
                    if label and label not in values:
                        values.append(label)
                field.options = values
            except Exception:
                # A non-inspectable dynamic control remains optionless and is
                # deliberately blocked by policy.
                field.options = []
            finally:
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
        return FormSnapshot(ats=self.ats, url=url, fields=fields, captcha=captcha)

    def fill(self, page: Any, plan: FillPlan) -> None:
        form = self.find_form(page)
        for action in plan.actions:
            locator = form.locator(action.option_selector or action.selector)
            if locator.count() != 1:
                raise RuntimeError(
                    f"Field selector is no longer unique for {action.prompt!r}"
                )
            if action.kind in {
                "text",
                "email",
                "tel",
                "url",
                "textarea",
                "number",
                "date",
                "month",
                "datetime-local",
            }:
                value = (
                    _validated_temporal_value(action.kind, action.value)
                    if action.kind in {"date", "month", "datetime-local"}
                    else str(action.value)
                )
                locator.fill(value)
            elif action.kind == "file":
                locator.set_input_files(str(action.value))
            elif action.kind == "select":
                locator.select_option(label=str(action.value))
            elif action.kind == "radio":
                locator.check()
            elif action.kind == "checkbox":
                if not isinstance(action.value, bool):
                    raise RuntimeError(
                        f"Checkbox answer is not a boolean for {action.prompt!r}"
                    )
                locator.set_checked(action.value)
            elif action.kind == "checkbox-group":
                locator.check()
            elif action.kind == "combobox":
                locator.click()
                option = page.get_by_role("option", name=str(action.value), exact=True)
                if option.count() != 1:
                    raise RuntimeError(
                        f"Combobox option is not an exact unique match for {action.prompt!r}"
                    )
                option.click()
            else:
                raise RuntimeError(f"Unsupported control kind: {action.kind}")

    def native_form_valid(self, page: Any) -> bool:
        return bool(
            self.find_form(page).evaluate(
                """(root) => {
                  if (typeof root.checkValidity === 'function') return root.checkValidity();
                  return Array.from(root.querySelectorAll('input,textarea,select')).every(
                    element => typeof element.checkValidity !== 'function' ||
                               element.checkValidity()
                  );
                }"""
            )
        )

    def submit_locator(self, page: Any) -> Any:
        form = self.find_form(page)
        found = []
        for selector in self.submit_selectors:
            locators = form.locator(selector)
            found.extend(
                locators.nth(index)
                for index in range(locators.count())
                if locators.nth(index).is_visible()
            )
            if found:
                break
        if len(found) != 1:
            raise RuntimeError(f"Expected one visible submit control, found {len(found)}")
        return found[0]

    @staticmethod
    def _submit_control_fingerprint(control: Any) -> str:
        identity = control.evaluate(
            """(el) => {
              const root = el.closest('form,[role="tabpanel"]') || document.body;
              const parts = [];
              let node = el;
              while (node && node !== root) {
                let index = 1;
                let sibling = node;
                while ((sibling = sibling.previousElementSibling)) {
                  if (sibling.tagName === node.tagName) index += 1;
                }
                parts.unshift(node.tagName.toLowerCase() + ':nth-of-type(' + index + ')');
                node = node.parentElement;
              }
              return {
                path: ':scope > ' + parts.join(' > '),
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                name: el.getAttribute('name') || '',
                type: el.getAttribute('type') || '',
                text: (el.innerText || el.value || el.textContent || '')
                  .replace(/\\s+/g, ' ').trim(),
                aria_label: el.getAttribute('aria-label') || '',
                title: el.getAttribute('title') || '',
                form_action: el.formAction || el.getAttribute('formaction') || '',
                form_method: el.formMethod || el.getAttribute('formmethod') || '',
                owner_form_action: el.form ? el.form.action : '',
                owner_form_method: el.form ? el.form.method : ''
              };
            }"""
        )
        if not isinstance(identity, dict) or not identity.get("tag"):
            raise RuntimeError("Submit control identity could not be observed")
        return digest(identity)

    def submit_fingerprint(self, page: Any, *, require_enabled: bool = False) -> str:
        locator = self.submit_locator(page)
        if not locator.is_visible():
            raise RuntimeError("Submit control is not visible")
        if require_enabled and not locator.is_enabled():
            raise RuntimeError("Submit control is not enabled")
        return self._submit_control_fingerprint(locator)

    def submit_control_for_click(
        self, page: Any, expected_fingerprint: str
    ) -> Any:
        """Return the exact observed enabled node, not a locator that can re-resolve."""
        locator = self.submit_locator(page)
        handle = locator.element_handle()
        if handle is None:
            raise RuntimeError("Submit control node could not be observed")
        if not handle.is_visible() or not handle.is_enabled():
            raise RuntimeError("Submit control is not visibly enabled")
        if self._submit_control_fingerprint(handle) != expected_fingerprint:
            raise RuntimeError(
                "Visible submit control changed before click; final click prohibited"
            )
        return handle

    def confirmation_state(self, page: Any) -> dict[str, Any]:
        body = page.locator("body").inner_text(timeout=5000)
        signals = {
            name: len(re.findall(pattern, body, flags=re.I))
            for name, pattern in CONFIRMATION_PATTERNS
        }
        url = str(page.url)
        return {"url": url, "signals": signals}

    def confirmed(
        self, page: Any, before_state: dict[str, Any] | None
    ) -> bool:
        after = self.confirmation_state(page)
        before = before_state or {"url": "", "signals": {}}
        before_signals = before.get("signals", {})
        new_signal = any(
            count > int(before_signals.get(name, 0))
            for name, count in after["signals"].items()
        )
        before_url = str(before.get("url", ""))
        after_url = str(after.get("url", ""))
        path = urlparse(after_url).path.lower()
        new_success_url = (
            after_url != before_url
            and re.search(
                r"(?:^|/)(?:thank-?you|confirmation|"
                r"application-(?:submitted|received)|success)(?:/|$)",
                path,
            )
            is not None
        )
        return new_signal or new_success_url
