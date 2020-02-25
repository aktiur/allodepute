/* global __production__ */

export function assign(selector, text) {
  const elems = document.querySelectorAll(selector);
  for (let i = 0; i < elems.length; i++) {
    elems[i].innerHTML = text;
  }
}

export function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export async function writeToClipboard(text) {
  const result = await navigator.permissions.query({ name: "clipboard-write" });
  if (result.state === "granted" || result.state === "prompt") {
    navigator.clipboard.writeText(text);
  }
}

export function mountComponent(component, id, options) {
  if (typeof options === "undefined") {
    options = {};
  }
  const node = document.getElementById(id);
  while (node.firstChild) {
    node.removeChild(node.lastChild);
  }

  return new component({ target: node, ...options });
}

export const isMobile = () =>
  window.matchMedia("only screen and (max-width: 760px)").matches;
