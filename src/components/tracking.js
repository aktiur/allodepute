import * as Sentry from "@sentry/browser";

export const trackAction = __production__
  ? (...args) => {
      window._paq.push(["trackEvent", ...args]);
      Sentry.addBreadcrumb({
        category: "UserAction",
        message: `${args[0]}: ${args[1]}`,
        level: Sentry.Severity.Info
      });
    }
  : (...args) => console.log("trackAction", ...args);

export const captureException = e =>
  __production__ ? Sentry.captureException(e) : console.log(e);
