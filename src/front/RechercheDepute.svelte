<script>
  /* global __production__ */

  import BoiteRecherche from "./BoiteRecherche.svelte";
  import PhotoDepute from "./PhotoDepute.svelte";
  import { getCookie } from "./utils";
  import { captureException, trackAction } from "./tracking";
  import { depute, random } from "./stores";
  import { chercherCodePostal } from "./back";

  let loading = false;
  let deputes = [];
  let errorMessage = null;

  const chercher = async e => {
    const codePostal = e.detail.codePostal;

    loading = true;
    errorMessage = null;

    try {
      deputes = await chercherCodePostal(codePostal);
    } catch (e) {
      errorMessage = e.message;
    } finally {
      loading = false;
    }
  };

  const choisirDepute = e => {
    const dep = e.detail.depute;
    trackAction("ChoisirDepute", dep.code);
    depute.set(dep);
    random.set(false);
  };
</script>

<!--suppress JSUnresolvedVariable -->
<h5>je cherche un⋅e député⋅e près de chez moi</h5>
<div class="py-2">
  <BoiteRecherche on:recherche={chercher} />
</div>
{#if loading}
  <div class="alert alert-info" id="form-message">
    Recherche en cours &hellip;
  </div>
{:else if errorMessage !== null}
  <div class="alert alert-danger" id="form-message">{errorMessage}</div>
{:else if deputes.length > 0}
  <div class="row pb-5 text-center" id="liste-deputes">
    {#each deputes as dep, i}
      <div class="col-md-4 px-1">
        <PhotoDepute
          extraClasses="scale"
          depute={dep}
          i={i + 2}
          on:choix={choisirDepute} />
        <div class="mt-2">{dep.nom}</div>
      </div>
    {/each}
  </div>
{/if}
