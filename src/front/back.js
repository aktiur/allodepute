import { trackAction, captureException } from "./tracking";
import { getCookie } from "./utils";

const checkForErrors = async fetcher => {
  let res;
  try {
    res = await fetcher;
  } catch (e) {
    captureException(e);
    throw new Error(
      "Erreur réseau rencontrée pendant la recherche. On enquête !"
    );
  }

  let data;

  try {
    data = await res.json();
  } catch (e) {
    captureException(
      `Erreur ${res.status}: le serveur n'a pas renvoyé de JSON !`
    );
    throw new Error(
      "Erreur inconnue rencontrée pendant la recherche. On enquête !"
    );
  }

  if (!res.ok) {
    if (data && data.message) {
      throw new Error(data.message);
    } else {
      captureException(`Erreur ${res.status}: pas de cause indiquée`);
      throw new Error(
        "Erreur inconnue rencontrée pendant la recherche. On enquête !"
      );
    }
  }

  return data;
};

export const deputeAuHasard = async () => {
  trackAction("DemanderDeputeHasard");

  const data = await checkForErrors(fetch("/hasard/"));
  if (!data.depute) {
    captureException(`Erreur données : pas de propriété 'depute'`);
    throw new Error("Le serveur a renvoyé n'importe quoi.");
  }

  return data.depute;
};

export const chercherCodePostal = async codePostal => {
  trackAction("ChercheCodePostal", codePostal);

  const data = await checkForErrors(
    fetch("/chercher/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: `code_postal=${codePostal}`
    })
  );

  if (!data.deputes) {
    captureException(
      `Erreur données : pas de propriété 'deputes' (code postal ${codePostal})`
    );
    throw new Error("Le serveur a renvoyé n'importe quoi.");
  }

  return data.deputes;
};
