/* ============================================================
   SPAM GUARD FOR SALESFORCE WEB-TO-LEAD FORMS
   Adds Google reCAPTCHA v2 ("I'm not a robot") plus a hidden
   honeypot field to every <form data-lead-guard>.

   The checkbox is only real protection once Salesforce enforces it:
   Setup > Web-to-Lead > Edit > "Require reCAPTCHA Verification",
   with an API key pair whose nickname equals SF_KEY_NAME below.
   Enforcement is org-wide, so EVERY page that posts to Web-to-Lead
   must load this script (contact, get-your-pdf, get-started, scorecard).

   Native forms: include this script BEFORE the page's own submit
   handlers so a blocked submit stops them from running.
   Script-submitted forms (scorecard): merge FTCLeadGuard.fields(form)
   into the POST body, then FTCLeadGuard.reset(form) after sending.
   ============================================================ */
(function () {
  var RECAPTCHA_SITE_KEY = "6Ld5sLsrAAAAAJ17ej0QxowttGdAy8RZeMJo3-K7"; // Google reCAPTCHA site "ftc website" (v2 checkbox, freethinkersconsulting.com)
  var SF_KEY_NAME = "FTC_Website"; // must match the reCAPTCHA API key pair nickname in Salesforce
  var SF_ORG_ID = "00Da500000I9TVx";
  var HONEYPOT_NAME = "hp_confirm_email"; // not a Lead field, so Salesforce ignores it

  var forms = [];

  function setup(form) {
    var settings = document.createElement("input");
    settings.type = "hidden";
    settings.name = "captcha_settings";
    form.appendChild(settings);

    // Off-screen field real visitors never see or tab into; bots that fill every input trip it.
    var trap = document.createElement("div");
    trap.setAttribute("aria-hidden", "true");
    trap.style.cssText = "position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden;";
    trap.innerHTML = '<label>Leave this empty<input type="text" name="' + HONEYPOT_NAME + '" tabindex="-1" autocomplete="off"></label>';
    form.appendChild(trap);

    var slot = form.querySelector(".lead-guard");
    if (!slot) {
      slot = document.createElement("div");
      slot.className = "lead-guard";
      var submit = form.querySelector('[type="submit"]');
      form.insertBefore(slot, submit);
    }
    slot.style.margin = slot.style.margin || "4px 0 20px";
    var widget = document.createElement("div");
    slot.appendChild(widget);
    var error = document.createElement("p");
    error.setAttribute("role", "alert");
    error.hidden = true;
    error.style.cssText = "color:#ff6b6b;font-size:.85rem;margin:8px 0 0;";
    slot.appendChild(error);

    var state = { form: form, settings: settings, widget: widget, error: error, widgetId: null, theme: slot.getAttribute("data-theme") || "dark" };
    forms.push(state);

    form.addEventListener("submit", function (e) {
      if (!check(form)) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    });
  }

  function stateFor(form) {
    for (var i = 0; i < forms.length; i++) if (forms[i].form === form) return forms[i];
    return null;
  }

  function response(state) {
    if (state.widgetId === null || !window.grecaptcha) return "";
    return window.grecaptcha.getResponse(state.widgetId);
  }

  // Salesforce's generated snippet keeps "ts" fresh until the checkbox is solved.
  function refreshTimestamps() {
    forms.forEach(function (state) {
      if (!response(state)) {
        state.settings.value = JSON.stringify({ keyname: SF_KEY_NAME, fallback: "true", orgId: SF_ORG_ID, ts: JSON.stringify(Date.now()) });
      }
    });
  }

  function check(form) {
    var state = stateFor(form);
    if (!state) return true;
    var trap = form.querySelector('[name="' + HONEYPOT_NAME + '"]');
    if (trap && trap.value) return false;
    if (!response(state)) {
      state.error.textContent = window.grecaptcha
        ? "Please tick “I’m not a robot” before sending."
        : "The spam check didn’t load. Please disable any ad blocker for this page and reload.";
      state.error.hidden = false;
      return false;
    }
    state.error.hidden = true;
    return true;
  }

  function fields(form) {
    var state = stateFor(form);
    if (!state) return {};
    return { captcha_settings: state.settings.value, "g-recaptcha-response": response(state) };
  }

  // Tokens are single-use; forms that stay on the page must reset before another submit.
  function reset(form) {
    var state = stateFor(form);
    if (state && state.widgetId !== null && window.grecaptcha) window.grecaptcha.reset(state.widgetId);
  }

  window.ftcLeadGuardRender = function () {
    forms.forEach(function (state) {
      state.widgetId = window.grecaptcha.render(state.widget, {
        sitekey: RECAPTCHA_SITE_KEY,
        theme: state.theme,
        callback: function () { state.error.hidden = true; }
      });
    });
  };

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll("form[data-lead-guard]"), setup);
    if (!forms.length) return;
    refreshTimestamps();
    setInterval(refreshTimestamps, 500);
    var s = document.createElement("script");
    s.src = "https://www.google.com/recaptcha/api.js?onload=ftcLeadGuardRender&render=explicit";
    s.async = true;
    s.defer = true;
    document.head.appendChild(s);
  }

  window.FTCLeadGuard = { check: check, fields: fields, reset: reset };
  init();
})();
