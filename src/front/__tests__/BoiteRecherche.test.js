import { render, fireEvent } from "@testing-library/svelte";

import BoiteRecherche from "../BoiteRecherche.svelte";

test("comporte bien une boite de texte et un bouton", () => {
  const { queryByRole } = render(BoiteRecherche, {});

  const input = queryByRole("searchbox");
  const button = queryByRole("button");

  expect(input).toBeInTheDocument();
  expect(button).toBeInTheDocument();

  expect(input.labels[0].textContent).toEqual("Mon code postal");
});

test("appelle le gestionnaire d'événement", async () => {
  let codePostal = null;
  const { queryByRole, component } = render(BoiteRecherche, {});

  component.$on("recherche", e => (codePostal = e.detail.codePostal));

  const input = queryByRole("searchbox");
  const submit = queryByRole("button");

  input.value = "75013";
  await fireEvent.click(submit);

  expect(codePostal).toEqual("75013");
});

test("n'autorise que des valeurs qui ressemblent à des codes postaux", async () => {
  let codePostal = null;
  const { queryByRole } = render(BoiteRecherche, {});

  const input = queryByRole("searchbox");
  const submit = queryByRole("button");

  input.value = "caca";
  await fireEvent.click(submit);

  expect(codePostal).toBeNull();
  expect(input).toBeInvalid();

  await fireEvent.input(input);
  expect(input).toBeValid();
});
