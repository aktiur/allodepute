import { writable } from "svelte/store";

export const data = JSON.parse(document.getElementById("donnees").textContent);

export const depute = writable(data.depute);
export const random = writable(true);
