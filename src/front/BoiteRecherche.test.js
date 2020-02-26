import { render, fireEvent } from "@testing-library/svelte";

import BoiteRecherche from "./BoiteRecherche.svelte";

test("comporte bien une boite de texte", () => {
  const { queryByRole } = render(BoiteRecherche, { name: "Recherche" });

  const input = queryByRole("searchbox");

  expect(input).toBeInTheDocument();

  expect(input.labels[0].textContent).toEqual("Mon code postal");
});
