import { writable } from "svelte/store";

const dataElement = document.getElementById("donnees");

export const data = dataElement
  ? JSON.parse(document.getElementById("donnees").textContent)
  : {};

export const depute = writable(data.depute);
export const random = writable(true);
