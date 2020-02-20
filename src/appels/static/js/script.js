const linkData = JSON.parse(document.getElementById("donnees").textContent);
const input = document.getElementById("inputcp");
const form = document.getElementById("form-cp");
const messageBox = document.getElementById("form-message");
const listeDeputes = document.getElementById("liste-deputes");
const tweets = document.getElementById("tweets");
const noTwitterMessage = document.getElementById("no-twitter");
const emailLink = document.getElementById("email-link");
const titre = document.getElementById("hasard-ou-choix");

const isMobile = window.matchMedia("only screen and (max-width: 760px)").matches;


/* GESTIONNAIRES D'EVENEMENTS */
document.querySelector(".depute_numero").addEventListener("click", function(e) {
    if (e.target.tagName === "A") {
      if (!isMobile) {
        e.preventDefault();
      } else {
        _paq.push(["trackEvent", "CliquerNumero", e.target.href])
      }
    }
});

document.getElementById("menu-argumentaires").addEventListener("click", function(e) {
  if (e.target.dataset.target) {
    _paq.push(["trackEvent", "OuvrirArgumentaire", e.target.dataset.target]);
  }
});

tweets.addEventListener("click", function(e) {
  if(e.target.dataset.tweet) {
    _paq.push(["trackEvent", "EnvoyerTweet", e.target.dataset.tweet]);
  }
});

form.addEventListener("submit", chercherDeputes);
for (let i = 0; i < 3; i++) {
  listeDeputes.children[i].addEventListener("click", changerDepute);
}

input.addEventListener("input", function() { input.setCustomValidity("");});

function montrerMessage(text) {
  messageBox.classList.remove("d-none");
  listeDeputes.classList.add("d-none");
  messageBox.textContent = text;
}

function afficherDeputes(deputes) {
  messageBox.classList.add("d-none");
  listeDeputes.classList.remove("d-none");

  for (let i = 0; i < 3; i++) {
    listeDeputes.children[i].dataset.depute = JSON.stringify(deputes[i]);
    const img = listeDeputes.children[i].querySelector(".img");
    const nameBox = listeDeputes.children[i].querySelector(".nom");

    nameBox.textContent = deputes[i].nom;
    img.style.backgroundImage = `var(--cadre), url(${deputes[i].image}`;
  }
}

function chercherDeputes(e) {
  e.preventDefault();
  const codePostal = input.value;

  if (!codePostal.match(/^[0-9]{5}$/)) {
    input.setCustomValidity("Indiquez un code postal français valide (5 chiffres)");
    return;
  } else {
    input.setCustomValidity("");
  }

  _paq.push(["trackEvent", "ChercheCodePostal", codePostal]);

  montrerMessage("Recherche...");
  fetch("/chercher/", {
    method: "POST", headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCookie('csrftoken')
    }, body: "code_postal=" + input.value
  }).then(function (res) {
    if (!res.ok) {
      return res.json().then(function (data) {
        montrerMessage(data.message)
      });
    }

    return res.json().then(function (d) {
      afficherDeputes(d.deputes);
    });
  }).catch(function (e) {
    return montrerMessage("Une erreur inconnue s'est produite.");
  });
}


function changerDepute(e) {
  e.preventDefault();
  const depute = JSON.parse(e.currentTarget.dataset.depute);

  _paq.push(["trackEvent", "ChoisitDepute", depute.code]);

  titre.textContent = `${depute.article_indefini} ${depute.titre} de mon choix`;

  assign(".depute_nom", depute.nom);
  assign(".depute_circonscription", depute.circonscription);
  assign(".depute_numero", depute.telephone);
  assign(".depute_article_demonstratif", `${depute.article_demonstratif} ${depute.titre}`)
  document.querySelector(".depute_image > div").style.backgroundImage = `var(--cadre), url(${depute.image}`;

  if (depute.twitter.length) {
    tweets.classList.remove("d-none");
    noTwitterMessage.classList.add("d-none");
    for (let i = 0; i < tweets.children.length; i++) {
      const a = tweets.children[i].querySelector("a");
      a.href = `https://twitter.com/intent/tweet?text=.@${depute.twitter}%20${linkData.tweets[i].quoted}&hashtags=allod%C3%A9put%C3%A9`;
    }
  } else {
    tweets.classList.add("d-none");
    noTwitterMessage.classList.remove("d-none");
  }
  emailLink.href = `mailto:${depute.email}${linkData.mailto_qs}`;
}


/* Fonctions utilitaires */
function assign(selector, text) {
  const elems = document.querySelectorAll(selector);
  for (let i = 0; i < elems.length; i++) {
    elems[i].innerHTML = text;
  }
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}