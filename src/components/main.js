import * as Sentry from "@sentry/browser";

if (__production__) {
  Sentry.init({
    dsn: "https://453a04d3822e40af9cbd2c7ab68013f4@sentry.io/2717092",
    beforeSend(event, hint) {
      // Check if it is an exception, and if so, show the report dialog
      if (event.exception) {
        Sentry.showReportDialog({ eventId: event.event_id });
      }
      return event;
    }
  });
}

import RechercheDepute from "./RechercheDepute.svelte";
import DeputeActif from "./DeputeActif.svelte";
import Tweets from "./Tweets.svelte";
import Email from "./Email.svelte";
import Appel from "./Appel.svelte";
import { mountComponent } from "./utils";
import { trackAction } from "./tracking";

mountComponent(DeputeActif, "depute-actif");
mountComponent(RechercheDepute, "recherche-depute");
mountComponent(Tweets, "tweets");
mountComponent(Email, "email");
mountComponent(Appel, "appel");

document
  .getElementById("menu-argumentaires")
  .addEventListener("click", function(e) {
    if (e.target.dataset.target) {
      trackAction("OuvrirArgumentaire", e.target.dataset.target);
    }
  });
